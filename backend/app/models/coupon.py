"""
优惠券相关模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Numeric, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Coupon(Base):
    """优惠券模板表"""
    __tablename__ = "coupons"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="优惠券名称")
    type: Mapped[str] = mapped_column(
        Enum("fixed", "percent", name="coupon_type_enum"),
        nullable=False,
        comment="类型: fixed固定金额 percent百分比"
    )
    value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="优惠值")
    min_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), comment="最低消费金额")
    max_discount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="最大优惠金额")
    
    # 发放数量
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, comment="发放总量")
    used_count: Mapped[int] = mapped_column(Integer, default=0, comment="已使用数量")
    
    # 有效期
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="开始时间")
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True, comment="结束时间")
    
    # 适用范围
    applicable_products: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="适用商品ID列表")
    applicable_categories: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="适用分类ID列表")
    
    is_active: Mapped[int] = mapped_column(Integer, default=1, index=True, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class UserCoupon(Base):
    """用户优惠券表"""
    __tablename__ = "user_coupons"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    coupon_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="优惠券ID")
    status: Mapped[str] = mapped_column(
        Enum("unused", "used", "expired", name="user_coupon_status_enum"),
        default="unused",
        index=True,
        comment="状态"
    )
    used_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="使用时间")
    order_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="使用订单ID")
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="领取时间")


