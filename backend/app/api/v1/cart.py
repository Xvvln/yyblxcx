"""
购物车接口
GET /cart - 购物车列表
POST /cart - 添加购物车
PUT /cart/{id} - 修改数量
DELETE /cart/{id} - 删除商品
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.cart import Cart
from app.models.shop import Product
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/cart", tags=["购物车"])


class CartAdd(BaseModel):
    """添加购物车"""
    product_id: int = Field(..., description="商品ID")
    spec_id: Optional[str] = Field(None, description="规格ID")
    quantity: int = Field(1, ge=1, description="数量")


class CartUpdate(BaseModel):
    """更新购物车"""
    quantity: int = Field(..., ge=1, description="数量")
    is_selected: Optional[int] = Field(None, ge=0, le=1, description="是否选中")


@router.get("/count")
async def get_cart_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取购物车商品数量"""
    from sqlalchemy import func
    result = await db.execute(
        select(func.count()).select_from(Cart).where(Cart.user_id == current_user.id)
    )
    count = result.scalar() or 0
    return success(data={"count": count})


@router.get("")
async def get_cart_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取购物车列表"""
    result = await db.execute(
        select(Cart).where(Cart.user_id == current_user.id).order_by(Cart.created_at.desc())
    )
    carts = result.scalars().all()
    
    # 获取商品信息
    product_ids = [c.product_id for c in carts]
    if product_ids:
        products_result = await db.execute(select(Product).where(Product.id.in_(product_ids)))
        products = {p.id: p for p in products_result.scalars().all()}
    else:
        products = {}
    
    # 检查是否会员
    is_member = current_user.member_level > 0
    
    items = []
    total_amount = 0
    selected_amount = 0
    
    for c in carts:
        product = products.get(c.product_id)
        if not product:
            continue
        
        # 计算价格
        price = float(product.member_price) if is_member and product.member_price else float(product.current_price)
        subtotal = price * c.quantity
        
        # 检查库存
        is_valid = product.is_on_sale == 1 and product.stock >= c.quantity
        
        item = {
            "id": c.id,
            "product_id": c.product_id,
            "spec_id": c.spec_id,
            "quantity": c.quantity,
            "is_selected": c.is_selected,
            "product": {
                "name": product.name,
                "image": product.images[0] if product.images else None,
                "price": price,
                "original_price": float(product.original_price),
                "stock": product.stock,
                "is_on_sale": product.is_on_sale,
            },
            "subtotal": subtotal,
            "is_valid": is_valid,
        }
        items.append(item)
        
        total_amount += subtotal
        if c.is_selected == 1 and is_valid:
            selected_amount += subtotal
    
    return success(data={
        "list": items,
        "total_amount": round(total_amount, 2),
        "selected_amount": round(selected_amount, 2),
        "total_count": len(items)
    })


@router.post("")
async def add_to_cart(
    data: CartAdd,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加商品到购物车"""
    # 检查商品是否存在
    product_result = await db.execute(
        select(Product).where(Product.id == data.product_id, Product.is_on_sale == 1)
    )
    product = product_result.scalar_one_or_none()
    
    if not product:
        return error(404, "商品不存在或已下架")
    
    if product.stock < data.quantity:
        return error(400, "库存不足")
    
    # 检查购物车是否已有该商品
    cart_result = await db.execute(
        select(Cart).where(
            Cart.user_id == current_user.id,
            Cart.product_id == data.product_id,
            Cart.spec_id == data.spec_id
        )
    )
    existing = cart_result.scalar_one_or_none()
    
    if existing:
        # 更新数量
        new_quantity = existing.quantity + data.quantity
        if new_quantity > product.stock:
            return error(400, "库存不足")
        existing.quantity = new_quantity
    else:
        # 新增购物车记录
        cart = Cart(
            user_id=current_user.id,
            product_id=data.product_id,
            spec_id=data.spec_id,
            quantity=data.quantity,
            is_selected=1
        )
        db.add(cart)
    
    await db.commit()
    
    return success(message="添加成功")


@router.put("/{cart_id}")
async def update_cart(
    cart_id: int,
    data: CartUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新购物车"""
    result = await db.execute(
        select(Cart).where(Cart.id == cart_id, Cart.user_id == current_user.id)
    )
    cart = result.scalar_one_or_none()
    
    if not cart:
        return error(404, "购物车记录不存在")
    
    # 检查库存
    product_result = await db.execute(select(Product).where(Product.id == cart.product_id))
    product = product_result.scalar_one_or_none()
    
    if product and data.quantity > product.stock:
        return error(400, "库存不足")
    
    cart.quantity = data.quantity
    if data.is_selected is not None:
        cart.is_selected = data.is_selected
    
    await db.commit()
    
    return success(message="更新成功")


@router.delete("/{cart_id}")
async def delete_cart(
    cart_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除购物车商品"""
    result = await db.execute(
        select(Cart).where(Cart.id == cart_id, Cart.user_id == current_user.id)
    )
    cart = result.scalar_one_or_none()
    
    if not cart:
        return error(404, "购物车记录不存在")
    
    await db.delete(cart)
    await db.commit()
    
    return success(message="删除成功")


