"""
私聊接口
GET /message/conversations - 会话列表
GET /message/history/{user_id} - 聊天记录
POST /message/send - 发送消息
POST /message/read/{conversation_id} - 标记已读
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_, or_
from datetime import datetime
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.message import Conversation, Message
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/message", tags=["私聊"])


class MessageSend(BaseModel):
    """发送消息"""
    receiver_id: int = Field(..., description="接收者ID")
    content: str = Field(..., min_length=1, max_length=1000, description="消息内容")
    msg_type: str = Field("text", description="消息类型: text/image/voice")


@router.get("/conversations")
async def get_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话列表"""
    # 查询用户相关的会话
    count_query = select(func.count()).select_from(Conversation).where(
        or_(
            Conversation.user_a_id == current_user.id,
            Conversation.user_b_id == current_user.id
        )
    )
    total = (await db.execute(count_query)).scalar()
    
    query = select(Conversation).where(
        or_(
            Conversation.user_a_id == current_user.id,
            Conversation.user_b_id == current_user.id
        )
    ).order_by(desc(Conversation.last_message_time)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    conversations = result.scalars().all()
    
    # 获取对方用户信息
    other_user_ids = []
    for c in conversations:
        other_id = c.user_b_id if c.user_a_id == current_user.id else c.user_a_id
        other_user_ids.append(other_id)
    
    users = {}
    if other_user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(other_user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    # 获取最后一条消息
    last_messages = {}
    if conversations:
        msg_ids = [c.last_message_id for c in conversations if c.last_message_id]
        if msg_ids:
            msgs_result = await db.execute(select(Message).where(Message.id.in_(msg_ids)))
            last_messages = {m.id: m for m in msgs_result.scalars().all()}
    
    items = []
    for c in conversations:
        other_id = c.user_b_id if c.user_a_id == current_user.id else c.user_a_id
        other_user = users.get(other_id)
        unread = c.user_a_unread if c.user_a_id == current_user.id else c.user_b_unread
        last_msg = last_messages.get(c.last_message_id) if c.last_message_id else None
        
        items.append({
            "id": c.id,
            "user": {
                "id": other_user.id if other_user else None,
                "nickname": other_user.nickname if other_user else "未知用户",
                "avatar": other_user.avatar if other_user else None,
            },
            "last_message": last_msg.content if last_msg else None,
            "last_message_time": c.last_message_time.strftime("%Y-%m-%d %H:%M:%S") if c.last_message_time else None,
            "unread_count": unread,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/history/{user_id}")
async def get_chat_history(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取与某用户的聊天记录"""
    # 查找或创建会话
    result = await db.execute(
        select(Conversation).where(
            or_(
                and_(Conversation.user_a_id == current_user.id, Conversation.user_b_id == user_id),
                and_(Conversation.user_a_id == user_id, Conversation.user_b_id == current_user.id)
            )
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        return paginate([], 0, page, page_size)
    
    # 查询消息
    count_query = select(func.count()).select_from(Message).where(
        Message.conversation_id == conversation.id
    )
    total = (await db.execute(count_query)).scalar()
    
    query = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(desc(Message.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    items = []
    for m in messages:
        items.append({
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "msg_type": m.msg_type,
            "is_read": m.is_read,
            "is_mine": m.sender_id == current_user.id,
            "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else None,
        })
    
    # 反转列表，按时间正序
    items.reverse()
    
    return paginate(items, total, page, page_size)


@router.post("/send")
async def send_message(
    data: MessageSend,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送消息"""
    if data.receiver_id == current_user.id:
        return error(400, "不能给自己发消息")
    
    # 检查接收者是否存在
    receiver_result = await db.execute(select(User).where(User.id == data.receiver_id))
    receiver = receiver_result.scalar_one_or_none()
    
    if not receiver:
        return error(404, "用户不存在")
    
    # 查找或创建会话
    # 确保 user_a_id < user_b_id 以保持唯一性
    user_a_id = min(current_user.id, data.receiver_id)
    user_b_id = max(current_user.id, data.receiver_id)
    
    result = await db.execute(
        select(Conversation).where(
            Conversation.user_a_id == user_a_id,
            Conversation.user_b_id == user_b_id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        conversation = Conversation(
            user_a_id=user_a_id,
            user_b_id=user_b_id,
        )
        db.add(conversation)
        await db.flush()
    
    # 创建消息
    message = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        receiver_id=data.receiver_id,
        content=data.content,
        msg_type=data.msg_type,
    )
    db.add(message)
    await db.flush()
    
    # 更新会话
    conversation.last_message_id = message.id
    conversation.last_message_time = datetime.now()
    
    # 更新未读数
    if current_user.id == user_a_id:
        conversation.user_b_unread += 1
    else:
        conversation.user_a_unread += 1
    
    await db.commit()
    
    return success(data={"id": message.id}, message="发送成功")


@router.post("/read/{conversation_id}")
async def mark_read(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """标记会话已读"""
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            or_(
                Conversation.user_a_id == current_user.id,
                Conversation.user_b_id == current_user.id
            )
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        return error(404, "会话不存在")
    
    # 清除未读数
    if conversation.user_a_id == current_user.id:
        conversation.user_a_unread = 0
    else:
        conversation.user_b_unread = 0
    
    # 标记消息已读
    await db.execute(
        Message.__table__.update().where(
            Message.conversation_id == conversation_id,
            Message.receiver_id == current_user.id,
            Message.is_read == 0
        ).values(is_read=1)
    )
    
    await db.commit()
    
    return success(message="标记已读成功")




















