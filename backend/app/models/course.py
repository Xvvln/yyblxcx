"""
课程相关模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Course(Base):
    """课程表"""
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="课程标题")
    subtitle: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="副标题")
    cover_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图")
    video_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="视频地址")
    
    # 课程信息
    duration: Mapped[int] = mapped_column(Integer, default=0, comment="时长(分钟)")
    difficulty: Mapped[str] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="difficulty_enum"),
        default="beginner",
        index=True,
        comment="难度"
    )
    sport_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True, comment="运动类型")
    calories: Mapped[int] = mapped_column(Integer, default=0, comment="预估消耗卡路里")
    equipment: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="所需器材")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="课程描述")
    
    # 教练信息
    coach_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="教练名称")
    coach_avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="教练头像")
    
    # 统计信息
    play_count: Mapped[int] = mapped_column(Integer, default=0, comment="播放次数")
    collect_count: Mapped[int] = mapped_column(Integer, default=0, comment="收藏次数")
    
    # 状态
    is_free: Mapped[int] = mapped_column(Integer, default=1, comment="是否免费")
    is_recommend: Mapped[int] = mapped_column(Integer, default=0, index=True, comment="是否推荐")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态: 0下架 1上架")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class UserCourseCollect(Base):
    """用户课程收藏表"""
    __tablename__ = "user_course_collects"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    course_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="课程ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")



















