"""
饮食相关模型
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Date, Text, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FoodRecord(Base):
    """饮食记录表"""
    __tablename__ = "food_records"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 餐次信息
    meal_type: Mapped[str] = mapped_column(
        Enum("breakfast", "lunch", "dinner", "snack", name="meal_type_enum"),
        nullable=False,
        index=True,
        comment="餐次类型"
    )
    record_date: Mapped[date] = mapped_column(Date, nullable=False, index=True, comment="记录日期")
    
    # 食物信息
    food_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="食物名称")
    food_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="食物图片")
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 2), nullable=True, comment="份量(克)")
    
    # 营养信息
    calories: Mapped[int] = mapped_column(Integer, default=0, comment="热量(大卡)")
    protein: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="蛋白质(克)")
    carbs: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="碳水(克)")
    fat: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="脂肪(克)")
    fiber: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="膳食纤维(克)")
    
    # AI识别（暂缓实现）
    is_ai_recognized: Mapped[int] = mapped_column(Integer, default=0, comment="是否AI识别")
    ai_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2), nullable=True, comment="AI识别置信度")
    
    # 积分
    coins_earned: Mapped[int] = mapped_column(Integer, default=0, comment="获得膳食币")
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class FoodLibrary(Base):
    """食物库表"""
    __tablename__ = "food_library"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, comment="食物名称")
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True, comment="食物分类")
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="食物图片")
    
    # 每100克营养成分
    calories: Mapped[int] = mapped_column(Integer, default=0, comment="热量(大卡/100g)")
    protein: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="蛋白质(克/100g)")
    carbs: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="碳水(克/100g)")
    fat: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="脂肪(克/100g)")
    fiber: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0.00"), comment="膳食纤维(克/100g)")
    
    serving_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="标准份量描述")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")




















