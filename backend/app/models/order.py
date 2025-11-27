"""
订单相关模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, Numeric, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, comment="订单号")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 金额
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="商品总额")
    pay_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="实付金额")
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), comment="优惠金额")
    freight_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), comment="运费")
    
    # 优惠券
    coupon_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, comment="优惠券ID")
    
    # 支付信息
    pay_type: Mapped[Optional[str]] = mapped_column(
        Enum("wechat", "alipay", "balance", "coins", name="pay_type_enum"),
        nullable=True,
        comment="支付方式"
    )
    
    # 订单状态
    status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "shipped", "received", "completed", "cancelled", "refunding", "refunded",
             name="order_status_enum"),
        default="pending",
        index=True,
        comment="订单状态"
    )
    
    # 收货信息
    receiver_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="收货人姓名")
    receiver_phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="收货人电话")
    receiver_address: Mapped[str] = mapped_column(String(300), nullable=False, comment="收货地址")
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="订单备注")
    
    # 时间节点
    pay_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="支付时间")
    ship_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="发货时间")
    receive_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="收货时间")
    
    # 物流信息
    tracking_company: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="物流公司")
    tracking_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="物流单号")
    
    # 评价状态
    is_reviewed: Mapped[int] = mapped_column(Integer, default=0, comment="是否已评价")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """订单明细表"""
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.id"), nullable=False, index=True, comment="订单ID")
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="商品ID")
    product_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="商品名称")
    product_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="商品图片")
    spec_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="规格名称")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="单价")
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, comment="数量")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="items")


