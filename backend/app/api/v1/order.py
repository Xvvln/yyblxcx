"""
订单接口
POST /order - 创建订单
GET /order/list - 订单列表
GET /order/{id} - 订单详情
POST /order/{id}/pay - 发起支付
POST /order/{id}/cancel - 取消订单
POST /order/{id}/confirm - 确认收货
POST /order/{id}/review - 提交评价
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.cart import Cart
from app.models.shop import Product, ProductReview
from app.models.order import Order, OrderItem
from app.models.coupon import UserCoupon, Coupon
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.utils.helpers import generate_order_no

router = APIRouter(prefix="/order", tags=["订单"])


class OrderItemCreate(BaseModel):
    """订单商品项"""
    product_id: int
    spec_id: Optional[str] = None
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    """创建订单"""
    items: List[OrderItemCreate] = Field(..., min_length=1)
    address_id: int = Field(..., description="收货地址ID")
    coupon_id: Optional[int] = Field(None, description="优惠券ID")
    remark: Optional[str] = Field(None, description="订单备注")


class ReviewCreate(BaseModel):
    """提交评价"""
    rating: int = Field(..., ge=1, le=5, description="评分")
    content: Optional[str] = Field(None, description="评价内容")
    images: Optional[List[str]] = Field(None, description="评价图片")
    is_anonymous: int = Field(0, ge=0, le=1, description="是否匿名")


@router.post("")
async def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建订单"""
    from app.models.user import UserAddress
    
    # 获取收货地址
    addr_result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == data.address_id,
            UserAddress.user_id == current_user.id
        )
    )
    address = addr_result.scalar_one_or_none()
    if not address:
        return error(400, "收货地址不存在")
    
    # 检查是否会员
    is_member = current_user.member_level > 0
    
    # 获取商品信息并计算金额
    total_amount = Decimal("0")
    order_items = []
    
    for item in data.items:
        product_result = await db.execute(
            select(Product).where(Product.id == item.product_id, Product.is_on_sale == 1)
        )
        product = product_result.scalar_one_or_none()
        
        if not product:
            return error(400, f"商品ID {item.product_id} 不存在或已下架")
        
        if product.stock < item.quantity:
            return error(400, f"商品 {product.name} 库存不足")
        
        # 计算价格
        price = product.member_price if is_member and product.member_price else product.current_price
        subtotal = price * item.quantity
        total_amount += subtotal
        
        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": price,
            "spec_id": item.spec_id,
        })
    
    # 计算优惠
    discount_amount = Decimal("0")
    if data.coupon_id:
        coupon_result = await db.execute(
            select(UserCoupon, Coupon).join(Coupon).where(
                UserCoupon.id == data.coupon_id,
                UserCoupon.user_id == current_user.id,
                UserCoupon.status == "unused"
            )
        )
        row = coupon_result.fetchone()
        
        if row:
            user_coupon, coupon = row
            if total_amount >= coupon.min_amount:
                if coupon.type == "fixed":
                    discount_amount = coupon.value
                else:  # percent
                    discount_amount = total_amount * coupon.value / 100
                    if coupon.max_discount:
                        discount_amount = min(discount_amount, coupon.max_discount)
    
    # 计算实付金额
    pay_amount = max(total_amount - discount_amount, Decimal("0"))
    
    # 生成订单号
    order_no = generate_order_no()
    
    # 创建订单
    order = Order(
        order_no=order_no,
        user_id=current_user.id,
        total_amount=total_amount,
        pay_amount=pay_amount,
        discount_amount=discount_amount,
        coupon_id=data.coupon_id,
        receiver_name=address.receiver_name,
        receiver_phone=address.receiver_phone,
        receiver_address=f"{address.province}{address.city}{address.district}{address.detail}",
        remark=data.remark,
        status="pending",
    )
    db.add(order)
    await db.flush()  # 获取订单ID
    
    # 创建订单明细
    for item_data in order_items:
        product = item_data["product"]
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            product_image=product.images[0] if product.images else None,
            spec_name=None,  # 可扩展规格名称
            price=item_data["price"],
            quantity=item_data["quantity"],
        )
        db.add(order_item)
        
        # 扣减库存
        product.stock -= item_data["quantity"]
    
    # 更新优惠券状态
    if data.coupon_id and discount_amount > 0:
        user_coupon.status = "used"
        user_coupon.used_time = datetime.now()
        user_coupon.order_id = order.id
    
    # 清除购物车中的已下单商品
    product_ids = [item.product_id for item in data.items]
    cart_result = await db.execute(
        select(Cart).where(
            Cart.user_id == current_user.id,
            Cart.product_id.in_(product_ids)
        )
    )
    for cart in cart_result.scalars().all():
        await db.delete(cart)
    
    await db.commit()
    await db.refresh(order)
    
    return success(
        data={
            "order_id": order.id,
            "order_no": order.order_no,
            "pay_amount": float(pay_amount)
        },
        message="订单创建成功"
    )


@router.get("/list")
async def get_order_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: Optional[str] = Query(None, description="订单状态"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取订单列表"""
    conditions = [Order.user_id == current_user.id]
    if status:
        conditions.append(Order.status == status)
    
    # 查询总数
    count_query = select(func.count()).select_from(Order).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询订单
    query = select(Order).where(*conditions).order_by(
        desc(Order.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    items = []
    for o in orders:
        # 获取订单商品
        items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id == o.id)
        )
        order_items = items_result.scalars().all()
        
        items.append({
            "id": o.id,
            "order_no": o.order_no,
            "status": o.status,
            "total_amount": float(o.total_amount),
            "pay_amount": float(o.pay_amount),
            "items": [{
                "product_id": i.product_id,
                "product_name": i.product_name,
                "product_image": i.product_image,
                "price": float(i.price),
                "quantity": i.quantity,
            } for i in order_items],
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })
    
    return paginate(items, total, page, page_size)


@router.get("/{order_id}")
async def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取订单详情"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    # 获取订单商品
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order_items = items_result.scalars().all()
    
    data = {
        "id": order.id,
        "order_no": order.order_no,
        "status": order.status,
        "total_amount": float(order.total_amount),
        "pay_amount": float(order.pay_amount),
        "discount_amount": float(order.discount_amount),
        "freight_amount": float(order.freight_amount),
        "pay_type": order.pay_type,
        "receiver_name": order.receiver_name,
        "receiver_phone": order.receiver_phone,
        "receiver_address": order.receiver_address,
        "remark": order.remark,
        "tracking_company": order.tracking_company,
        "tracking_no": order.tracking_no,
        "is_reviewed": order.is_reviewed,
        "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S") if order.pay_time else None,
        "ship_time": order.ship_time.strftime("%Y-%m-%d %H:%M:%S") if order.ship_time else None,
        "receive_time": order.receive_time.strftime("%Y-%m-%d %H:%M:%S") if order.receive_time else None,
        "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "items": [{
            "id": i.id,
            "product_id": i.product_id,
            "product_name": i.product_name,
            "product_image": i.product_image,
            "spec_name": i.spec_name,
            "price": float(i.price),
            "quantity": i.quantity,
        } for i in order_items],
    }
    
    return success(data=data)


@router.post("/{order_id}/pay")
async def pay_order(
    order_id: int,
    pay_type: str = Query("wechat", description="支付方式"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发起支付
    
    TODO: 暂缓实现
    原因: 需要微信商户号、API密钥
    当前: 直接返回模拟支付成功
    """
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status != "pending":
        return error(400, "订单状态不允许支付")
    
    # 模拟支付成功
    order.status = "paid"
    order.pay_type = pay_type
    order.pay_time = datetime.now()
    
    # 更新商品销量
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    for item in items_result.scalars().all():
        product_result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = product_result.scalar_one_or_none()
        if product:
            product.sales_count += item.quantity
    
    await db.commit()
    
    return success(
        data={
            "order_id": order.id,
            "status": "paid",
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S")
        },
        message="模拟支付成功"
    )


@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status not in ["pending"]:
        return error(400, "订单状态不允许取消")
    
    # 恢复库存
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    for item in items_result.scalars().all():
        product_result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = product_result.scalar_one_or_none()
        if product:
            product.stock += item.quantity
    
    # 恢复优惠券
    if order.coupon_id:
        coupon_result = await db.execute(
            select(UserCoupon).where(UserCoupon.id == order.coupon_id)
        )
        user_coupon = coupon_result.scalar_one_or_none()
        if user_coupon:
            user_coupon.status = "unused"
            user_coupon.used_time = None
            user_coupon.order_id = None
    
    order.status = "cancelled"
    await db.commit()
    
    return success(message="订单已取消")


@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """确认收货"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status != "shipped":
        return error(400, "订单状态不允许确认收货")
    
    order.status = "received"
    order.receive_time = datetime.now()
    await db.commit()
    
    return success(message="确认收货成功")


@router.post("/{order_id}/review")
async def review_order(
    order_id: int,
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交评价"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status not in ["received", "completed"]:
        return error(400, "订单状态不允许评价")
    
    if order.is_reviewed == 1:
        return error(400, "订单已评价")
    
    # 获取订单商品
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    
    # 为每个商品创建评价
    for item in items_result.scalars().all():
        review = ProductReview(
            product_id=item.product_id,
            user_id=current_user.id,
            order_id=order.id,
            rating=data.rating,
            content=data.content,
            images=data.images,
            is_anonymous=data.is_anonymous,
        )
        db.add(review)
    
    order.is_reviewed = 1
    order.status = "completed"
    await db.commit()
    
    return success(message="评价成功")


