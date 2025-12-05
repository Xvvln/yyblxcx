"""
健康筛查相关模型
"""
from datetime import datetime, time
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Time, Text, Numeric, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class HealthScreening(Base):
    """健康筛查记录表"""
    __tablename__ = "health_screenings"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 基础数据
    height: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="身高(cm)")
    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="体重(kg)")
    bmi: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True, comment="BMI")
    
    # 体征数据
    heart_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="心率")
    blood_pressure_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="收缩压")
    blood_pressure_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="舒张压")
    body_temperature: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1), nullable=True, comment="体温")
    blood_sugar: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True, comment="血糖")
    
    # 图像数据
    face_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="面部照片")
    body_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="体态照片")
    
    # 问卷数据
    questionnaire_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="问卷数据")
    
    # 分析结果
    risk_level: Mapped[str] = mapped_column(
        Enum("low", "medium", "high", name="risk_level_enum"),
        default="low",
        index=True,
        comment="风险等级"
    )
    risk_tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="风险标签")
    
    # AI 建议
    ai_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="AI综合建议")
    diet_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="饮食建议")
    exercise_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="运动建议")
    lifestyle_suggestion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="生活方式建议")
    
    # 商品推荐
    recommended_products: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="推荐商品ID列表")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


class HealthReminder(Base):
    """健康提醒设置表"""
    __tablename__ = "health_reminders"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    reminder_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True, comment="提醒类型")
    reminder_time: Mapped[time] = mapped_column(Time, nullable=False, comment="提醒时间")
    content: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="提醒内容")
    repeat_days: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="重复日期[1-7]")
    is_enabled: Mapped[int] = mapped_column(Integer, default=1, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
























