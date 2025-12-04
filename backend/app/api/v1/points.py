"""
积分接口
GET /points/balance - 积分余额
GET /points/records - 积分记录
GET /points/gifts - 可兑换礼品
POST /points/exchange - 兑换礼品
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.points import CoinRecord
from app.models.shop import Product
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/points", tags=["积分"])


class ExchangeRequest(BaseModel):
    """兑换请求"""
    gift_id: int = Field(..., description="礼品ID")
    quantity: int = Field(1, ge=1, description="数量")


@router.get("/balance")
async def get_balance(current_user: User = Depends(get_current_user)):
    """获取积分余额"""
    return success(data={
        "sport_coins": current_user.sport_coins,
        "food_coins": current_user.food_coins,
        "total_coins": current_user.sport_coins + current_user.food_coins,
        "user_level": current_user.user_level,
    })


@router.get("/records")
async def get_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    coin_type: Optional[str] = Query(None, description="积分类型: sport/food"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取积分记录"""
    conditions = [CoinRecord.user_id == current_user.id]
    if coin_type:
        conditions.append(CoinRecord.coin_type == coin_type)
    
    # 查询总数
    count_query = select(func.count()).select_from(CoinRecord).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(CoinRecord).where(*conditions).order_by(
        desc(CoinRecord.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "coin_type": r.coin_type,
            "amount": r.amount,
            "balance": r.balance,
            "source": r.source,
            "description": r.description,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/gifts")
async def get_gifts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """获取可兑换礼品"""
    # 这里简化处理，实际应该有专门的礼品表
    # 暂时返回推荐商品作为可兑换礼品
    conditions = [Product.is_on_sale == 1, Product.is_recommend == 1]
    
    count_query = select(func.count()).select_from(Product).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    query = select(Product).where(*conditions).order_by(
        Product.sort_order.desc(), Product.id.desc()
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    items = []
    for p in products:
        # 积分价格 = 商品价格 * 10
        points_price = int(float(p.current_price) * 10)
        items.append({
            "id": p.id,
            "name": p.name,
            "image": p.images[0] if p.images else None,
            "points_price": points_price,
            "original_price": float(p.current_price),
            "stock": p.stock,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/exchange")
async def exchange_gift(
    data: ExchangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """兑换礼品"""
    # 获取礼品信息
    result = await db.execute(
        select(Product).where(Product.id == data.gift_id, Product.is_on_sale == 1)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        return error(404, "礼品不存在")
    
    if product.stock < data.quantity:
        return error(400, "库存不足")
    
    # 计算所需积分
    points_price = int(float(product.current_price) * 10)
    total_points = points_price * data.quantity
    
    # 检查积分是否足够（优先使用运动币）
    total_user_coins = current_user.sport_coins + current_user.food_coins
    if total_user_coins < total_points:
        return error(400, "积分不足")
    
    # 扣除积分
    remaining = total_points
    sport_deduct = min(current_user.sport_coins, remaining)
    current_user.sport_coins -= sport_deduct
    remaining -= sport_deduct
    
    if remaining > 0:
        current_user.food_coins -= remaining
    
    # 记录积分变动
    if sport_deduct > 0:
        coin_record1 = CoinRecord(
            user_id=current_user.id,
            coin_type="sport",
            amount=-sport_deduct,
            balance=current_user.sport_coins,
            source="exchange",
            source_id=product.id,
            description=f"兑换{product.name}"
        )
        db.add(coin_record1)
    
    if remaining > 0:
        coin_record2 = CoinRecord(
            user_id=current_user.id,
            coin_type="food",
            amount=-remaining,
            balance=current_user.food_coins,
            source="exchange",
            source_id=product.id,
            description=f"兑换{product.name}"
        )
        db.add(coin_record2)
    
    # 扣减库存
    product.stock -= data.quantity
    
    await db.commit()
    
    return success(
        data={
            "gift_name": product.name,
            "quantity": data.quantity,
            "points_used": total_points
        },
        message="兑换成功"
    )




















