"""
订单管理接口
GET /order/list - 订单列表
GET /order/{id} - 订单详情
POST /order/{id}/ship - 发货
POST /order/{id}/refund - 退款处理
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.system import Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/order", tags=["订单管理"])


class ShipRequest(BaseModel):
    """发货请求"""
    tracking_company: str = Field(..., min_length=1, max_length=50, description="快递公司")
    tracking_no: str = Field(..., min_length=1, max_length=50, description="快递单号")


class RefundRequest(BaseModel):
    """退款请求"""
    refund_amount: Optional[float] = Field(None, description="退款金额，不填则全额退款")
    reason: Optional[str] = Field(None, max_length=200, description="退款原因")


@router.get("/list")
async def get_order_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_no: Optional[str] = Query(None, description="订单号"),
    status: Optional[str] = Query(None, description="订单状态"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取订单列表"""
    conditions = []
    
    if order_no:
        conditions.append(Order.order_no.like(f"%{order_no}%"))
    
    if status:
        conditions.append(Order.status == status)
    
    if start_date:
        conditions.append(Order.created_at >= datetime.strptime(start_date, "%Y-%m-%d"))
    
    if end_date:
        conditions.append(Order.created_at < datetime.strptime(end_date, "%Y-%m-%d"))
    
    # 查询总数
    count_query = select(func.count()).select_from(Order)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Order)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(Order.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([o.user_id for o in orders]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    items = []
    for o in orders:
        user = users.get(o.user_id)
        items.append({
            "id": o.id,
            "order_no": o.order_no,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
            },
            "total_amount": float(o.total_amount),
            "pay_amount": float(o.pay_amount),
            "discount_amount": float(o.discount_amount) if o.discount_amount else 0,
            "status": o.status,
            "pay_type": o.pay_type,
            "receiver_name": o.receiver_name,
            "receiver_phone": o.receiver_phone,
            "tracking_company": o.tracking_company,
            "tracking_no": o.tracking_no,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else None,
            "pay_time": o.pay_time.strftime("%Y-%m-%d %H:%M:%S") if o.pay_time else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/{order_id}")
async def get_order_detail(
    order_id: int,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取订单详情"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    # 获取用户信息
    user_result = await db.execute(select(User).where(User.id == order.user_id))
    user = user_result.scalar_one_or_none()
    
    # 获取订单项
    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order_id)
    )
    order_items = items_result.scalars().all()
    
    items = []
    for item in order_items:
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_image": item.product_image,
            "spec_name": item.spec_name,
            "price": float(item.price),
            "quantity": item.quantity,
        })
    
    return success(data={
        "id": order.id,
        "order_no": order.order_no,
        "user": {
            "id": user.id if user else None,
            "nickname": user.nickname if user else "未知用户",
            "phone": user.phone if user else None,
        },
        "total_amount": float(order.total_amount),
        "pay_amount": float(order.pay_amount),
        "discount_amount": float(order.discount_amount) if order.discount_amount else 0,
        "freight_amount": float(order.freight_amount) if order.freight_amount else 0,
        "status": order.status,
        "pay_type": order.pay_type,
        "receiver_name": order.receiver_name,
        "receiver_phone": order.receiver_phone,
        "receiver_address": order.receiver_address,
        "remark": order.remark,
        "tracking_company": order.tracking_company,
        "tracking_no": order.tracking_no,
        "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else None,
        "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S") if order.pay_time else None,
        "ship_time": order.ship_time.strftime("%Y-%m-%d %H:%M:%S") if order.ship_time else None,
        "receive_time": order.receive_time.strftime("%Y-%m-%d %H:%M:%S") if order.receive_time else None,
        "items": items,
    })


@router.post("/{order_id}/ship")
async def ship_order(
    order_id: int,
    data: ShipRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """发货"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status != "paid":
        return error(400, "订单状态不正确，无法发货")
    
    order.status = "shipped"
    order.tracking_company = data.tracking_company
    order.tracking_no = data.tracking_no
    order.ship_time = datetime.now()
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="ship",
        target_type="order",
        target_id=order_id,
        content=f"订单发货: {order.order_no}, 快递: {data.tracking_company}, 单号: {data.tracking_no}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="发货成功")


@router.post("/{order_id}/refund")
async def refund_order(
    order_id: int,
    data: RefundRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """退款"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        return error(404, "订单不存在")
    
    if order.status not in ["paid", "shipped", "refunding"]:
        return error(400, "订单状态不正确，无法退款")
    
    refund_amount = data.refund_amount or float(order.pay_amount)
    
    order.status = "refunded"
    
    # 记录操作日志
    content = f"订单退款: {order.order_no}, 金额: {refund_amount}"
    if data.reason:
        content += f", 原因: {data.reason}"
    
    log = AdminLog(
        admin_id=admin.id,
        action="refund",
        target_type="order",
        target_id=order_id,
        content=content,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    # TODO: 实际退款逻辑（暂缓实现）
    # 当前仅更新订单状态，不做实际退款操作
    
    return success(message="退款成功（模拟）")




















