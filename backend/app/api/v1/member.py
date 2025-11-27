"""
会员接口
GET /member/info - 会员信息
GET /member/plans - 会员套餐列表
POST /member/purchase - 购买会员
GET /member/orders - 会员购买记录
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta
from decimal import Decimal
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.member import MemberOrder
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.utils.helpers import generate_order_no

router = APIRouter(prefix="/member", tags=["会员"])


# 会员套餐配置
MEMBER_PLANS = [
    {
        "id": "month",
        "name": "月卡会员",
        "original_price": 30.00,
        "price": 19.90,
        "days": 30,
        "level": 1,
        "benefits": ["专属会员价", "积分加成20%", "优先客服"]
    },
    {
        "id": "year",
        "name": "年卡会员",
        "original_price": 360.00,
        "price": 168.00,
        "days": 365,
        "level": 2,
        "benefits": ["专属会员价", "积分加成50%", "优先客服", "专属活动"]
    },
    {
        "id": "lifetime",
        "name": "终身会员",
        "original_price": 999.00,
        "price": 399.00,
        "days": 36500,
        "level": 3,
        "benefits": ["专属会员价", "积分加成100%", "优先客服", "专属活动", "终身免费升级"]
    }
]


class PurchaseRequest(BaseModel):
    """购买会员请求"""
    plan_type: str = Field(..., description="套餐类型: month/year/lifetime")
    pay_type: str = Field("wechat", description="支付方式: wechat/alipay")


@router.get("/info")
async def get_member_info(current_user: User = Depends(get_current_user)):
    """获取会员信息"""
    is_member = current_user.member_level > 0
    expire_time = current_user.member_expire_time
    
    # 检查是否过期
    if is_member and expire_time and expire_time < datetime.now():
        is_member = False
    
    # 获取当前套餐信息
    current_plan = None
    if is_member:
        for plan in MEMBER_PLANS:
            if plan["level"] == current_user.member_level:
                current_plan = plan
                break
    
    return success(data={
        "is_member": is_member,
        "member_level": current_user.member_level,
        "member_level_name": current_plan["name"] if current_plan else "普通用户",
        "expire_time": expire_time.strftime("%Y-%m-%d %H:%M:%S") if expire_time else None,
        "benefits": current_plan["benefits"] if current_plan else [],
    })


@router.get("/plans")
async def get_member_plans():
    """获取会员套餐列表"""
    return success(data=MEMBER_PLANS)


@router.post("/purchase")
async def purchase_member(
    data: PurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    购买会员
    
    TODO: 暂缓实现真实支付
    原因: 需要微信商户资质
    当前: 直接模拟支付成功
    """
    # 获取套餐信息
    plan = None
    for p in MEMBER_PLANS:
        if p["id"] == data.plan_type:
            plan = p
            break
    
    if not plan:
        return error(400, "套餐不存在")
    
    # 生成订单号
    order_no = generate_order_no()
    
    # 计算会员时间
    now = datetime.now()
    if current_user.member_expire_time and current_user.member_expire_time > now:
        # 续费，在原有基础上延长
        start_time = current_user.member_expire_time
    else:
        start_time = now
    
    end_time = start_time + timedelta(days=plan["days"])
    
    # 创建订单
    order = MemberOrder(
        order_no=order_no,
        user_id=current_user.id,
        plan_type=data.plan_type,
        plan_name=plan["name"],
        original_price=Decimal(str(plan["original_price"])),
        pay_amount=Decimal(str(plan["price"])),
        pay_type=data.pay_type,
        status="paid",  # 模拟支付成功
        member_start_time=start_time,
        member_end_time=end_time,
        pay_time=now,
    )
    db.add(order)
    
    # 更新用户会员状态
    current_user.member_level = plan["level"]
    current_user.member_expire_time = end_time
    
    await db.commit()
    
    return success(
        data={
            "order_no": order_no,
            "plan_name": plan["name"],
            "expire_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
        },
        message="购买成功"
    )


@router.get("/orders")
async def get_member_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """会员购买记录"""
    conditions = [MemberOrder.user_id == current_user.id]
    
    count_query = select(func.count()).select_from(MemberOrder).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    query = select(MemberOrder).where(*conditions).order_by(
        desc(MemberOrder.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    orders = result.scalars().all()
    
    items = []
    for o in orders:
        items.append({
            "id": o.id,
            "order_no": o.order_no,
            "plan_type": o.plan_type,
            "plan_name": o.plan_name,
            "original_price": float(o.original_price),
            "pay_amount": float(o.pay_amount),
            "pay_type": o.pay_type,
            "status": o.status,
            "member_start_time": o.member_start_time.strftime("%Y-%m-%d") if o.member_start_time else None,
            "member_end_time": o.member_end_time.strftime("%Y-%m-%d") if o.member_end_time else None,
            "pay_time": o.pay_time.strftime("%Y-%m-%d %H:%M:%S") if o.pay_time else None,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


