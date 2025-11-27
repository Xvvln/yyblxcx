"""
系统管理相关模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Admin(Base):
    """管理员表"""
    __tablename__ = "admins"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像")
    role: Mapped[str] = mapped_column(String(20), default="admin", comment="角色")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态: 0禁用 1正常")
    last_login_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="最后登录时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class AdminLog(Base):
    """管理员操作日志表"""
    __tablename__ = "admin_logs"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="管理员ID")
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="操作")
    target_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="目标类型")
    target_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="目标ID")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="操作内容")
    ip: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="IP地址")
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="User Agent")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


class Notification(Base):
    """系统通知表"""
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="类型")
    related_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="关联类型")
    related_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="关联ID")
    is_read: Mapped[int] = mapped_column(Integer, default=0, comment="是否已读")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


class Banner(Base):
    """轮播图表"""
    __tablename__ = "banners"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="标题")
    image_url: Mapped[str] = mapped_column(String(255), nullable=False, comment="图片")
    link_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="链接类型")
    link_value: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="链接值")
    position: Mapped[str] = mapped_column(String(50), default="home", index=True, comment="位置")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    is_active: Mapped[int] = mapped_column(Integer, default=1, index=True, comment="是否启用")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="开始时间")
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="结束时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = "system_configs"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    config_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="配置键")
    config_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="配置值")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="描述")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class File(Base):
    """文件管理表"""
    __tablename__ = "files"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True, comment="上传用户ID")
    file_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="原始文件名")
    file_path: Mapped[str] = mapped_column(String(255), nullable=False, comment="存储路径")
    file_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="文件类型")
    file_size: Mapped[int] = mapped_column(Integer, default=0, comment="文件大小(字节)")
    mime_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="MIME类型")
    module: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True, comment="模块")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


class AIChatRecord(Base):
    """AI对话记录表"""
    __tablename__ = "ai_chat_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    session_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="会话ID")
    role: Mapped[str] = mapped_column(String(20), nullable=False, comment="角色: user/assistant")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    tokens_used: Mapped[int] = mapped_column(Integer, default=0, comment="消耗token数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")

