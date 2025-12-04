"""
私信相关模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Conversation(Base):
    """会话表"""
    __tablename__ = "conversations"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_a_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户A")
    user_b_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户B")
    last_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="最后消息ID")
    last_message_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True, comment="最后消息时间")
    user_a_unread: Mapped[int] = mapped_column(Integer, default=0, comment="用户A未读数")
    user_b_unread: Mapped[int] = mapped_column(Integer, default=0, comment="用户B未读数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class Message(Base):
    """私信消息表"""
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="会话ID")
    sender_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="发送者ID")
    receiver_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="接收者ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    msg_type: Mapped[str] = mapped_column(
        Enum("text", "image", "voice", name="msg_type_enum"),
        default="text",
        comment="消息类型"
    )
    is_read: Mapped[int] = mapped_column(Integer, default=0, comment="是否已读")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")



















