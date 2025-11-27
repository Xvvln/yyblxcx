"""
数据统计接口
GET /stats/overview - 数据概览
GET /stats/user - 用户统计
GET /stats/order - 订单统计
GET /stats/health - 健康数据统计
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.models.health import HealthScreening
from app.models.sport import SportRecord
from app.models.food import FoodRecord
from app.models.community import Post
from app.models.points import CheckinRecord
from app.models.system import Admin
from app.utils.security import get_current_admin
from app.utils.response import success

router = APIRouter(prefix="/stats", tags=["数据统计"])


@router.get("/overview")
async def get_overview(
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """数据概览"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    
    # 用户总数
    total_users = (await db.execute(
        select(func.count()).select_from(User)
    )).scalar()
    
    # 今日新增用户
    today_new_users = (await db.execute(
        select(func.count()).select_from(User).where(User.created_at >= today)
    )).scalar()
    
    # 昨日新增用户
    yesterday_new_users = (await db.execute(
        select(func.count()).select_from(User).where(
            and_(User.created_at >= yesterday, User.created_at < today)
        )
    )).scalar()
    
    # 订单统计
    total_orders = (await db.execute(
        select(func.count()).select_from(Order)
    )).scalar()
    
    today_orders = (await db.execute(
        select(func.count()).select_from(Order).where(Order.created_at >= today)
    )).scalar()
    
    # 今日订单金额
    today_amount_result = await db.execute(
        select(func.sum(Order.pay_amount)).where(
            and_(Order.created_at >= today, Order.status.in_(["paid", "shipped", "received", "completed"]))
        )
    )
    today_amount = today_amount_result.scalar() or 0
    
    # 总交易金额
    total_amount_result = await db.execute(
        select(func.sum(Order.pay_amount)).where(
            Order.status.in_(["paid", "shipped", "received", "completed"])
        )
    )
    total_amount = total_amount_result.scalar() or 0
    
    # 今日打卡数
    today_checkins = (await db.execute(
        select(func.count()).select_from(CheckinRecord).where(
            CheckinRecord.checkin_date == today.date()
        )
    )).scalar()
    
    # 社区动态数
    total_posts = (await db.execute(
        select(func.count()).select_from(Post).where(Post.status == 1)
    )).scalar()
    
    return success(data={
        "users": {
            "total": total_users,
            "today_new": today_new_users,
            "yesterday_new": yesterday_new_users,
        },
        "orders": {
            "total": total_orders,
            "today_count": today_orders,
            "today_amount": float(today_amount),
            "total_amount": float(total_amount),
        },
        "activities": {
            "today_checkins": today_checkins,
            "total_posts": total_posts,
        }
    })


@router.get("/user")
async def get_user_stats(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """用户统计"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 每日新增用户
    daily_data = []
    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = (await db.execute(
            select(func.count()).select_from(User).where(
                and_(User.created_at >= day_start, User.created_at < day_end)
            )
        )).scalar()
        
        daily_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count,
        })
    
    # 会员类型分布 (0:普通 1:月卡 2:年卡 3:终身)
    member_distribution = []
    member_labels = {0: "普通用户", 1: "月卡会员", 2: "年卡会员", 3: "终身会员"}
    for level in [0, 1, 2, 3]:
        count = (await db.execute(
            select(func.count()).select_from(User).where(
                User.member_level == level
            )
        )).scalar()
        member_distribution.append({
            "type": member_labels[level],
            "level": level,
            "count": count,
        })
    
    # 用户等级分布
    level_distribution = []
    for level in range(1, 11):
        count = (await db.execute(
            select(func.count()).select_from(User).where(
                User.user_level == level
            )
        )).scalar()
        level_distribution.append({
            "level": level,
            "count": count,
        })
    
    return success(data={
        "daily_new_users": daily_data,
        "member_distribution": member_distribution,
        "level_distribution": level_distribution,
    })


@router.get("/order")
async def get_order_stats(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """订单统计"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 每日订单数和金额
    daily_data = []
    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = (await db.execute(
            select(func.count()).select_from(Order).where(
                and_(Order.created_at >= day_start, Order.created_at < day_end)
            )
        )).scalar()
        
        amount_result = await db.execute(
            select(func.sum(Order.pay_amount)).where(
                and_(
                    Order.created_at >= day_start,
                    Order.created_at < day_end,
                    Order.status.in_(["paid", "shipped", "received", "completed"])
                )
            )
        )
        amount = amount_result.scalar() or 0
        
        daily_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count,
            "amount": float(amount),
        })
    
    # 订单状态分布
    status_distribution = []
    for status in ["pending", "paid", "shipped", "received", "completed", "cancelled", "refunded"]:
        count = (await db.execute(
            select(func.count()).select_from(Order).where(Order.status == status)
        )).scalar()
        status_distribution.append({
            "status": status,
            "count": count,
        })
    
    return success(data={
        "daily_orders": daily_data,
        "status_distribution": status_distribution,
    })


@router.get("/health")
async def get_health_stats(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """健康数据统计"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 每日筛查数
    screening_data = []
    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = (await db.execute(
            select(func.count()).select_from(HealthScreening).where(
                and_(HealthScreening.created_at >= day_start, HealthScreening.created_at < day_end)
            )
        )).scalar()
        
        screening_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count,
        })
    
    # 风险等级分布
    risk_distribution = []
    for risk_level in ["low", "medium", "high"]:
        count = (await db.execute(
            select(func.count()).select_from(HealthScreening).where(
                HealthScreening.risk_level == risk_level
            )
        )).scalar()
        risk_distribution.append({
            "level": risk_level,
            "count": count,
        })
    
    # 每日运动记录数
    sport_data = []
    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = (await db.execute(
            select(func.count()).select_from(SportRecord).where(
                and_(SportRecord.created_at >= day_start, SportRecord.created_at < day_end)
            )
        )).scalar()
        
        sport_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count,
        })
    
    # 每日饮食记录数
    food_data = []
    for i in range(days - 1, -1, -1):
        day_start = today - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        count = (await db.execute(
            select(func.count()).select_from(FoodRecord).where(
                and_(FoodRecord.created_at >= day_start, FoodRecord.created_at < day_end)
            )
        )).scalar()
        
        food_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count,
        })
    
    return success(data={
        "daily_screenings": screening_data,
        "risk_distribution": risk_distribution,
        "daily_sports": sport_data,
        "daily_foods": food_data,
    })


