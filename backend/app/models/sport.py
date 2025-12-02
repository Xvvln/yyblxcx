"""
运动相关模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SportRecord(Base):
    """运动记录表"""
    __tablename__ = "sport_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 运动信息
    sport_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="运动类型")
    sport_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="运动名称")
    duration: Mapped[int] = mapped_column(Integer, nullable=False, comment="时长(分钟)")
    distance: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="距离(米)")
    calories: Mapped[int] = mapped_column(Integer, default=0, comment="消耗卡路里")
    
    # 配速心率
    avg_pace: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="平均配速(分钟/公里)")
    avg_heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="平均心率")
    max_heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="最大心率")
    elevation_gain: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2), nullable=True, comment="累计爬升(米)")
    
    # GPS轨迹（暂缓后端存储）
    gps_track: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="GPS轨迹数据")
    
    # 其他信息
    weather: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="天气")
    feeling: Mapped[int] = mapped_column(Integer, default=3, comment="运动感受 1-5")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")
    course_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="课程ID")
    
    # 积分
    coins_earned: Mapped[int] = mapped_column(Integer, default=0, comment="获得运动币")
    
    # 时间
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="开始时间")
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="结束时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class SportGoal(Base):
    """运动目标表"""
    __tablename__ = "sport_goals"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    goal_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="目标类型")
    target_value: Mapped[int] = mapped_column(Integer, nullable=False, comment="目标值")
    current_value: Mapped[int] = mapped_column(Integer, default=0, comment="当前值")
    unit: Mapped[str] = mapped_column(String(20), nullable=False, comment="单位")
    period: Mapped[str] = mapped_column(String(20), nullable=False, comment="周期: daily/weekly/monthly")
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="开始日期")
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="结束日期")
    is_completed: Mapped[int] = mapped_column(Integer, default=0, comment="是否完成")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")















