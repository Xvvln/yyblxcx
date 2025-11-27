"""
优惠券接口
GET /coupon/available - 可领取优惠券
POST /coupon/{id}/receive - 领取优惠券
GET /coupon/my-coupons - 我的优惠券
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.coupon import Coupon, UserCoupon
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/coupon", tags=["优惠券"])


@router.get("/available")
async def get_available_coupons(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取可领取的优惠券"""
    now = datetime.now()
    
    # 查询有效的优惠券
    result = await db.execute(
        select(Coupon).where(
            Coupon.is_active == 1,
            Coupon.start_time <= now,
            Coupon.end_time >= now,
            Coupon.total_count > Coupon.used_count
        ).order_by(Coupon.id.desc())
    )
    coupons = result.scalars().all()
    
    # 查询用户已领取的优惠券
    user_coupons_result = await db.execute(
        select(UserCoupon.coupon_id).where(UserCoupon.user_id == current_user.id)
    )
    received_ids = {row[0] for row in user_coupons_result.fetchall()}
    
    items = []
    for c in coupons:
        items.append({
            "id": c.id,
            "name": c.name,
            "type": c.type,
            "value": float(c.value),
            "min_amount": float(c.min_amount),
            "max_discount": float(c.max_discount) if c.max_discount else None,
            "start_time": c.start_time.strftime("%Y-%m-%d"),
            "end_time": c.end_time.strftime("%Y-%m-%d"),
            "is_received": c.id in received_ids,
            "remaining": c.total_count - c.used_count,
        })
    
    return success(data=items)


@router.post("/{coupon_id}/receive")
async def receive_coupon(
    coupon_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """领取优惠券"""
    now = datetime.now()
    
    # 查询优惠券
    result = await db.execute(
        select(Coupon).where(
            Coupon.id == coupon_id,
            Coupon.is_active == 1,
            Coupon.start_time <= now,
            Coupon.end_time >= now
        )
    )
    coupon = result.scalar_one_or_none()
    
    if not coupon:
        return error(404, "优惠券不存在或已过期")
    
    if coupon.used_count >= coupon.total_count:
        return error(400, "优惠券已领完")
    
    # 检查是否已领取
    existing = await db.execute(
        select(UserCoupon).where(
            UserCoupon.user_id == current_user.id,
            UserCoupon.coupon_id == coupon_id
        )
    )
    if existing.scalar_one_or_none():
        return error(400, "已领取该优惠券")
    
    # 创建用户优惠券记录
    user_coupon = UserCoupon(
        user_id=current_user.id,
        coupon_id=coupon_id,
        status="unused"
    )
    db.add(user_coupon)
    
    # 更新优惠券领取数量
    coupon.used_count += 1
    
    await db.commit()
    
    return success(message="领取成功")


@router.get("/my-coupons")
async def get_my_coupons(
    status: str = Query("unused", description="状态: unused/used/expired"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """我的优惠券"""
    conditions = [UserCoupon.user_id == current_user.id]
    
    if status == "unused":
        conditions.append(UserCoupon.status == "unused")
    elif status == "used":
        conditions.append(UserCoupon.status == "used")
    elif status == "expired":
        conditions.append(UserCoupon.status == "expired")
    
    # 查询总数
    count_query = select(func.count()).select_from(UserCoupon).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 联表查询
    query = select(UserCoupon, Coupon).join(Coupon).where(*conditions).order_by(
        UserCoupon.received_at.desc()
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    items = []
    for row in rows:
        uc, c = row
        items.append({
            "id": uc.id,
            "coupon_id": c.id,
            "name": c.name,
            "type": c.type,
            "value": float(c.value),
            "min_amount": float(c.min_amount),
            "max_discount": float(c.max_discount) if c.max_discount else None,
            "status": uc.status,
            "start_time": c.start_time.strftime("%Y-%m-%d"),
            "end_time": c.end_time.strftime("%Y-%m-%d"),
            "received_at": uc.received_at.strftime("%Y-%m-%d %H:%M:%S") if uc.received_at else None,
        })
    
    return paginate(items, total, page, page_size)


