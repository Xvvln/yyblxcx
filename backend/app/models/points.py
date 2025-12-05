"""
积分任务相关模型
"""
from datetime import datetime, date
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CoinRecord(Base):
    """积分变动记录表"""
    __tablename__ = "coin_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    coin_type: Mapped[str] = mapped_column(
        Enum("sport", "food", name="coin_type_enum"),
        nullable=False,
        index=True,
        comment="积分类型"
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="变动数量(正增负减)")
    balance: Mapped[int] = mapped_column(Integer, nullable=False, comment="变动后余额")
    source: Mapped[str] = mapped_column(String(50), nullable=False, comment="来源类型")
    source_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="来源ID")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="描述")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


class CheckinRecord(Base):
    """打卡记录表"""
    __tablename__ = "checkin_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    checkin_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="打卡日期")
    sport_coins_earned: Mapped[int] = mapped_column(Integer, default=0, comment="获得运动币")
    food_coins_earned: Mapped[int] = mapped_column(Integer, default=0, comment="获得膳食币")
    is_continuous: Mapped[int] = mapped_column(Integer, default=0, comment="是否连续打卡")
    continuous_days: Mapped[int] = mapped_column(Integer, default=1, comment="连续天数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class DailyTask(Base):
    """每日任务配置表"""
    __tablename__ = "daily_tasks"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="任务名称")
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="任务描述")
    task_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="任务类型")
    target_value: Mapped[int] = mapped_column(Integer, default=1, comment="目标值")
    reward_coin_type: Mapped[str] = mapped_column(
        Enum("sport", "food", name="reward_coin_type_enum"),
        nullable=False,
        comment="奖励积分类型"
    )
    reward_amount: Mapped[int] = mapped_column(Integer, nullable=False, comment="奖励数量")
    is_active: Mapped[int] = mapped_column(Integer, default=1, index=True, comment="是否启用")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class UserTaskRecord(Base):
    """用户任务完成记录表"""
    __tablename__ = "user_task_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="任务ID")
    task_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="任务日期")
    current_value: Mapped[int] = mapped_column(Integer, default=0, comment="当前进度")
    is_completed: Mapped[int] = mapped_column(Integer, default=0, comment="是否完成")
    is_claimed: Mapped[int] = mapped_column(Integer, default=0, comment="是否已领取奖励")
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="完成时间")
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="领取时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
























