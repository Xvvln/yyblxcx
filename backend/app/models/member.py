"""
会员相关模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MemberOrder(Base):
    """会员购买记录表"""
    __tablename__ = "member_orders"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, comment="订单号")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    member_type: Mapped[str] = mapped_column(
        Enum("month", "year", "lifetime", name="member_type_enum"),
        nullable=False,
        comment="套餐类型"
    )
    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="原价")
    pay_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="实付金额")
    pay_type: Mapped[Optional[str]] = mapped_column(
        Enum("wechat", "alipay", name="member_pay_type_enum"),
        nullable=True,
        comment="支付方式"
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "cancelled", name="member_order_status_enum"),
        default="pending",
        index=True,
        comment="状态"
    )
    expire_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="会员到期时间")
    pay_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="支付时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")


