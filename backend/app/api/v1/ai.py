"""
AI健康助手接口
POST /ai/chat - AI健康助手对话
GET /ai/history - AI对话历史
GET /ai/sessions - 会话列表
DELETE /ai/history/{session_id} - 删除会话历史
POST /ai/new-session - 创建新会话
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
import uuid
import logging

from app.database import get_db
from app.models.user import User, UserHealthProfile
from app.models.system import AIChatRecord
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.services.ai_service import AIHealthAssistant

router = APIRouter(prefix="/ai", tags=["AI助手"])
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """对话请求"""
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    session_id: Optional[str] = Field(None, description="会话ID，不传则创建新会话")


class ChatResponse(BaseModel):
    """对话响应"""
    session_id: str
    reply: str


def calculate_bmi(height: Optional[Decimal], weight: Optional[Decimal]) -> tuple:
    """计算BMI及分类"""
    if not height or not weight or float(height) <= 0:
        return None, None, None
    
    height_m = float(height) / 100
    bmi = float(weight) / (height_m ** 2)
    
    BMI_CATEGORIES = [
        (18.5, "偏瘦", "建议适当增加营养摄入，注意蛋白质补充"),
        (24, "正常", "体重健康，继续保持良好的生活习惯"),
        (28, "偏胖", "建议控制饮食，增加运动量"),
        (float('inf'), "肥胖", "建议在专业指导下制定减重计划"),
    ]
    
    for threshold, category, advice in BMI_CATEGORIES:
        if bmi < threshold:
            return round(bmi, 1), category, advice
    
    return round(bmi, 1), "肥胖", "建议在专业指导下制定减重计划"


def calculate_age(birthday: Optional[date]) -> Optional[int]:
    """计算年龄"""
    if not birthday:
        return None
    today = date.today()
    age = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age


def build_user_context(user: User, health_profile: Optional[UserHealthProfile]) -> dict:
    """构建丰富的用户上下文信息"""
    context = {}
    
    # 基本信息
    age = calculate_age(user.birthday)
    if age:
        context["年龄"] = age
    
    gender_map = {0: "未知", 1: "男", 2: "女"}
    if user.gender:
        context["性别"] = gender_map.get(user.gender, "未知")
    
    if user.height:
        context["身高"] = f"{user.height}cm"
    
    if user.weight:
        context["体重"] = f"{user.weight}kg"
    
    # BMI 计算
    bmi, bmi_category, bmi_advice = calculate_bmi(user.height, user.weight)
    if bmi:
        context["BMI"] = bmi
        context["BMI分类"] = bmi_category
        context["BMI建议"] = bmi_advice
    
    # 健康档案信息
    if health_profile:
        # 健康目标
        goal_map = {
            "lose_weight": "减脂瘦身",
            "gain_muscle": "增肌塑形",
            "keep_fit": "保持健康",
            "improve_sleep": "改善睡眠",
            "reduce_stress": "减压放松",
        }
        if health_profile.health_goal:
            context["健康目标"] = goal_map.get(health_profile.health_goal, health_profile.health_goal)
        
        if health_profile.target_weight:
            context["目标体重"] = f"{health_profile.target_weight}kg"
        
        # 慢性病史
        if health_profile.chronic_diseases and len(health_profile.chronic_diseases) > 0:
            context["慢性病史"] = ", ".join(health_profile.chronic_diseases)
        else:
            context["慢性病史"] = "无"
        
        # 过敏食物
        if health_profile.allergies and len(health_profile.allergies) > 0:
            context["过敏食物"] = ", ".join(health_profile.allergies)
        else:
            context["过敏食物"] = "无"
        
        # 伤病情况
        if health_profile.has_injury and health_profile.injury_description:
            context["伤病情况"] = health_profile.injury_description
        
        # 饮食习惯
        diet_map = {
            "balanced": "均衡饮食",
            "vegetarian": "素食",
            "low_carb": "低碳水",
            "high_protein": "高蛋白",
            "light": "清淡饮食",
        }
        if health_profile.diet_habit:
            context["饮食习惯"] = diet_map.get(health_profile.diet_habit, health_profile.diet_habit)
        
        # 运动偏好
        if health_profile.preferred_sports and len(health_profile.preferred_sports) > 0:
            sports_map = {
                "running": "跑步",
                "swimming": "游泳",
                "cycling": "骑行",
                "yoga": "瑜伽",
                "gym": "健身房",
                "ball": "球类运动",
                "walking": "散步",
            }
            sports = [sports_map.get(s, s) for s in health_profile.preferred_sports]
            context["运动偏好"] = ", ".join(sports)
        
        if health_profile.daily_exercise_minutes:
            context["每日运动目标"] = f"{health_profile.daily_exercise_minutes}分钟"
    
    return context


@router.post("/chat")
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """AI健康助手对话
    
    支持上下文对话，自动记录对话历史，基于用户健康档案提供个性化建议。
    """
    # 生成或使用已有的会话ID
    session_id = data.session_id or str(uuid.uuid4())[:8]
    
    logger.info(f"用户 {current_user.id} 发起AI对话，会话: {session_id}")
    
    # 获取用户健康档案
    health_result = await db.execute(
        select(UserHealthProfile).where(UserHealthProfile.user_id == current_user.id)
    )
    health_profile = health_result.scalar_one_or_none()
    
    # 构建丰富的用户上下文
    context = build_user_context(current_user, health_profile)
    
    logger.info(f"用户上下文: {context}")
    
    # 获取历史对话作为上下文（最近10轮，即20条消息）
    history_result = await db.execute(
        select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == session_id
        ).order_by(desc(AIChatRecord.created_at)).limit(20)
    )
    history_records = history_result.scalars().all()
    history_records = list(reversed(history_records))  # 按时间正序
    
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


@router.post("/new-session")
async def create_new_session(
    current_user: User = Depends(get_current_user),
):
    """创建新会话
    
    返回一个新的会话ID，用于开始新的对话。
    """
    session_id = str(uuid.uuid4())[:8]
    return success(data={
        "session_id": session_id,
    })


@router.get("/sessions")
async def get_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话列表
    
    返回用户所有的AI对话会话，按最后消息时间倒序排列。
    """
    from sqlalchemy import distinct
    
    # 获取所有会话ID
    session_query = select(distinct(AIChatRecord.session_id)).where(
        AIChatRecord.user_id == current_user.id
    )
    session_result = await db.execute(session_query)
    session_ids = [row[0] for row in session_result.fetchall()]
    
    items = []
    for sid in session_ids:
        # 获取每个会话的最后一条消息和第一条消息
        last_msg_query = select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == sid
        ).order_by(desc(AIChatRecord.created_at)).limit(1)
        
        last_msg_result = await db.execute(last_msg_query)
        last_msg = last_msg_result.scalar_one_or_none()
        
        first_msg_query = select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id,
            AIChatRecord.session_id == sid,
            AIChatRecord.role == "user"
        ).order_by(AIChatRecord.created_at).limit(1)
        
        first_msg_result = await db.execute(first_msg_query)
        first_msg = first_msg_result.scalar_one_or_none()
        
        if last_msg:
            # 获取会话消息数
            count = (await db.execute(
                select(func.count()).select_from(AIChatRecord).where(
                    AIChatRecord.user_id == current_user.id,
                    AIChatRecord.session_id == sid
                )
            )).scalar()
            
            # 使用第一条用户消息作为会话标题
            title = first_msg.content if first_msg else last_msg.content
            title = title[:30] + "..." if len(title) > 30 else title
            
            items.append({
                "session_id": sid,
                "title": title,
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


@router.get("/history")
async def get_history(
    session_id: Optional[str] = Query(None, description="会话ID，不传则获取会话列表"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取AI对话历史
    
    如果传入session_id，返回该会话的所有消息；否则返回会话列表。
    """
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
        # 获取会话列表（兼容旧接口）
        from sqlalchemy import distinct
        
        session_query = select(distinct(AIChatRecord.session_id)).where(
            AIChatRecord.user_id == current_user.id
        )
        session_result = await db.execute(session_query)
        session_ids = [row[0] for row in session_result.fetchall()]
        
        items = []
        for sid in session_ids:
            last_msg_query = select(AIChatRecord).where(
                AIChatRecord.user_id == current_user.id,
                AIChatRecord.session_id == sid
            ).order_by(desc(AIChatRecord.created_at)).limit(1)
            
            last_msg_result = await db.execute(last_msg_query)
            last_msg = last_msg_result.scalar_one_or_none()
            
            if last_msg:
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
        
        items.sort(key=lambda x: x["last_time"] or "", reverse=True)
        
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
    """删除会话历史
    
    删除指定会话的所有消息记录。
    """
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
    
    logger.info(f"用户 {current_user.id} 删除会话 {session_id}，共 {len(records)} 条消息")
    
    return success(message="删除成功")


@router.delete("/history")
async def clear_all_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空所有对话历史
    
    删除用户的所有AI对话记录。
    """
    result = await db.execute(
        select(AIChatRecord).where(
            AIChatRecord.user_id == current_user.id
        )
    )
    records = result.scalars().all()
    
    count = len(records)
    for record in records:
        await db.delete(record)
    
    await db.commit()
    
    logger.info(f"用户 {current_user.id} 清空所有对话历史，共 {count} 条消息")
    
    return success(message=f"已清空 {count} 条对话记录")
