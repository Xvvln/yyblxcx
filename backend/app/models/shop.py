"""
商城相关模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Text, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductCategory(Base):
    """商品分类表"""
    __tablename__ = "product_categories"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="分类名称")
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True, comment="父分类ID")
    icon: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="分类图标")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    is_active: Mapped[int] = mapped_column(Integer, default=1, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class Product(Base):
    """商品表"""
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    category_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="商品名称")
    subtitle: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="副标题")
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="商品图片列表")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="商品描述")
    
    # 价格
    original_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="原价")
    current_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="现价")
    member_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment="会员价")
    
    # 库存销量
    stock: Mapped[int] = mapped_column(Integer, default=0, comment="库存")
    sales_count: Mapped[int] = mapped_column(Integer, default=0, comment="销量")
    
    # 标签
    suitable_tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="适用人群标签")
    health_tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="健康标签")
    
    # 规格
    specs: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="规格选项")
    
    # 状态
    is_recommend: Mapped[int] = mapped_column(Integer, default=0, index=True, comment="是否推荐")
    is_on_sale: Mapped[int] = mapped_column(Integer, default=1, index=True, comment="是否上架")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class ProductReview(Base):
    """商品评价表"""
    __tablename__ = "product_reviews"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="商品ID")
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    order_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="订单ID")
    rating: Mapped[int] = mapped_column(Integer, nullable=False, comment="评分 1-5")
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="评价内容")
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="评价图片")
    is_anonymous: Mapped[int] = mapped_column(Integer, default=0, comment="是否匿名")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态: 0隐藏 1显示")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


class ProductCollect(Base):
    """商品收藏表"""
    __tablename__ = "product_collects"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="商品ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")


