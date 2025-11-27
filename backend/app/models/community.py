"""
社区相关模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Post(Base):
    """社区动态表"""
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="动态内容")
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="图片列表")
    video_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="视频地址")
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True, comment="话题ID")
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="位置")
    
    # 统计
    view_count: Mapped[int] = mapped_column(Integer, default=0, comment="浏览量")
    like_count: Mapped[int] = mapped_column(Integer, default=0, comment="点赞数")
    comment_count: Mapped[int] = mapped_column(Integer, default=0, comment="评论数")
    share_count: Mapped[int] = mapped_column(Integer, default=0, comment="分享数")
    
    # 状态
    is_top: Mapped[int] = mapped_column(Integer, default=0, comment="是否置顶")
    is_essence: Mapped[int] = mapped_column(Integer, default=0, comment="是否精华")
    status: Mapped[int] = mapped_column(Integer, default=1, index=True, comment="状态: 0删除 1正常 2审核中")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class PostComment(Base):
    """动态评论表"""
    __tablename__ = "post_comments"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="动态ID")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="评论用户ID")
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True, comment="父评论ID")
    reply_to_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="回复用户ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="评论内容")
    like_count: Mapped[int] = mapped_column(Integer, default=0, comment="点赞数")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态: 0删除 1正常")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class PostLike(Base):
    """动态点赞表"""
    __tablename__ = "post_likes"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="动态ID")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class Topic(Base):
    """话题表"""
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="话题名称")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="话题描述")
    cover_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图")
    post_count: Mapped[int] = mapped_column(Integer, default=0, comment="动态数量")
    participant_count: Mapped[int] = mapped_column(Integer, default=0, comment="参与人数")
    is_hot: Mapped[int] = mapped_column(Integer, default=0, index=True, comment="是否热门")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class UserFollow(Base):
    """用户关注关系表"""
    __tablename__ = "user_follows"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    follow_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="被关注用户ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")

