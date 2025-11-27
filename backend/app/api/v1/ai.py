"""
AI健康助手接口
POST /ai/chat - AI健康助手对话
GET /ai/history - AI对话历史
DELETE /ai/history/{session_id} - 删除会话历史
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

from app.database import get_db
from app.models.user import User, UserHealthProfile
from app.models.system import AIChatRecord
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.services.ai_service import AIHealthAssistant

router = APIRouter(prefix="/ai", tags=["AI助手"])


class ChatRequest(BaseModel):
    """对话请求"""
    message: str = Field(..., min_length=1, max_length=1000, description="用户消息")
    session_id: Optional[str] = Field(None, description="会话ID，不传则创建新会话")


class ChatResponse(BaseModel):
    """对话响应"""
    session_id: str
    reply: str


@router.post("/chat")
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """AI健康助手对话"""
    # 生成或使用已有的会话ID
    session_id = data.session_id or str(uuid.uuid4())[:8]
    
    # 获取用户健康档案作为上下文
    health_result = await db.execute(
        select(UserHealthProfile).where(UserHealthProfile.user_id == current_user.id)
    )
    health_profile = health_result.scalar_one_or_none()
    
    context = {
        "身高": f"{current_user.height}cm" if current_user.height else "未知",
        "体重": f"{current_user.weight}kg" if current_user.weight else "未知",
    }
    if health_profile:
        context.update({
            "健康目标": health_profile.health_goal or "未知",
            "慢性病史": ", ".join(health_profile.chronic_diseases) if health_profile.chronic_diseases else "无",
            "过敏食物": ", ".join(health_profile.allergies) if health_profile.allergies else "无",
        })
    
    # 获取历史对话作为上下文（最近5轮）
    history_result = await db.execute(
        select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == session_id
        ).order_by(desc(AIChatRecord.created_at)).limit(10)
    )
    history_records = history_result.scalars().all()
    history_records.reverse()  # 按时间正序
    
    history = []
    for record in history_records:
        history.append({
            "role": record.role,
            "content": record.content
        })
    
    # 保存用户消息
    user_message = AIChatRecord(
        user_id=current_user.id,
        session_id=session_id,
        role="user",
        content=data.message,
    )
    db.add(user_message)
    
    # 调用AI服务
    ai_assistant = AIHealthAssistant()
    reply = await ai_assistant.chat(
        user_message=data.message,
        context=context,
        history=history
    )
    
    # 保存AI回复
    ai_message = AIChatRecord(
        user_id=current_user.id,
        session_id=session_id,
        role="assistant",
        content=reply,
    )
    db.add(ai_message)
    
    await db.commit()
    
    return success(data={
        "session_id": session_id,
        "reply": reply,
    })


@router.get("/history")
async def get_history(
    session_id: Optional[str] = Query(None, description="会话ID，不传则获取会话列表"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取AI对话历史"""
    if session_id:
        # 获取指定会话的消息
        conditions = [
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == session_id
        ]
        
        count_query = select(func.count()).select_from(AIChatRecord).where(*conditions)
        total = (await db.execute(count_query)).scalar()
        
        query = select(AIChatRecord).where(*conditions).order_by(
            AIChatRecord.created_at
        ).offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        records = result.scalars().all()
        
        items = []
        for r in records:
            items.append({
                "id": r.id,
                "role": r.role,
                "content": r.content,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
            })
        
        return paginate(items, total, page, page_size)
    
    else:
        # 获取会话列表
        # 按session_id分组，获取每个会话的最后一条消息
        from sqlalchemy import distinct
        
        # 获取所有会话ID
        session_query = select(distinct(AIChatRecord.session_id)).where(
            AIChatRecord.user_id == current_user.id
        )
        session_result = await db.execute(session_query)
        session_ids = [row[0] for row in session_result.fetchall()]
        
        items = []
        for sid in session_ids:
            # 获取每个会话的最后一条消息
            last_msg_query = select(AIChatRecord).where(
                AIChatRecord.user_id == current_user.id,
                AIChatRecord.session_id == sid
            ).order_by(desc(AIChatRecord.created_at)).limit(1)
            
            last_msg_result = await db.execute(last_msg_query)
            last_msg = last_msg_result.scalar_one_or_none()
            
            if last_msg:
                # 获取会话消息数
                count = (await db.execute(
                    select(func.count()).select_from(AIChatRecord).where(
                        AIChatRecord.user_id == current_user.id,
                        AIChatRecord.session_id == sid
                    )
                )).scalar()
                
                items.append({
                    "session_id": sid,
                    "message_count": count,
                    "last_message": last_msg.content[:50] + "..." if len(last_msg.content) > 50 else last_msg.content,
                    "last_time": last_msg.created_at.strftime("%Y-%m-%d %H:%M:%S") if last_msg.created_at else None,
                })
        
        # 按最后消息时间排序
        items.sort(key=lambda x: x["last_time"] or "", reverse=True)
        
        # 分页
        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        items = items[start:end]
        
        return paginate(items, total, page, page_size)


@router.delete("/history/{session_id}")
async def delete_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除会话历史"""
    # 删除该会话的所有消息
    result = await db.execute(
        select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == session_id
        )
    )
    records = result.scalars().all()
    
    if not records:
        return error(404, "会话不存在")
    
    for record in records:
        await db.delete(record)
    
    await db.commit()
    
    return success(message="删除成功")


