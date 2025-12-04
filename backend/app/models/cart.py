"""
购物车模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cart(Base):
    """购物车表"""
    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="用户ID")
    product_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True, comment="商品ID")
    spec_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="规格ID")
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="数量")
    is_selected: Mapped[int] = mapped_column(Integer, default=1, comment="是否选中")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")



















