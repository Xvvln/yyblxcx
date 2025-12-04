"""
签到接口
POST /checkin - 每日签到
GET /checkin/status - 今日签到状态
GET /checkin/calendar - 签到日历
GET /checkin/stats - 签到统计
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import date, datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.points import CheckinRecord, CoinRecord
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/checkin", tags=["签到"])


@router.post("")
async def daily_checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """每日签到"""
    today = date.today()
    
    # 检查今日是否已签到
    result = await db.execute(
        select(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date == today
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return error(400, "今日已签到")
    
    # 检查是否连续签到
    is_continuous = False
    continuous_days = 1
    
    if current_user.last_checkin_date:
        diff = (today - current_user.last_checkin_date).days
        if diff == 1:
            is_continuous = True
            continuous_days = current_user.continuous_checkin_days + 1
    
    # 计算奖励（连续签到奖励翻倍，最多7倍）
    base_reward = 5
    multiplier = min(continuous_days, 7)
    sport_coins_earned = base_reward * multiplier
    food_coins_earned = base_reward * multiplier
    
    # 创建签到记录
    checkin = CheckinRecord(
        user_id=current_user.id,
        checkin_date=today,
        sport_coins_earned=sport_coins_earned,
        food_coins_earned=food_coins_earned,
        is_continuous=1 if is_continuous else 0,
        continuous_days=continuous_days,
    )
    db.add(checkin)
    
    # 更新用户信息
    current_user.sport_coins += sport_coins_earned
    current_user.food_coins += food_coins_earned
    current_user.last_checkin_date = today
    current_user.continuous_checkin_days = continuous_days if is_continuous else 1
    current_user.total_checkin_days = (current_user.total_checkin_days or 0) + 1
    
    # 记录积分变动
    coin_record1 = CoinRecord(
        user_id=current_user.id,
        coin_type="sport",
        amount=sport_coins_earned,
        balance=current_user.sport_coins,
        source="daily_checkin",
        description=f"连续签到第{continuous_days}天"
    )
    db.add(coin_record1)
    
    coin_record2 = CoinRecord(
        user_id=current_user.id,
        coin_type="food",
        amount=food_coins_earned,
        balance=current_user.food_coins,
        source="daily_checkin",
        description=f"连续签到第{continuous_days}天"
    )
    db.add(coin_record2)
    
    await db.commit()
    
    return success(
        data={
            "sport_coins_earned": sport_coins_earned,
            "food_coins_earned": food_coins_earned,
            "continuous_days": continuous_days,
            "total_checkin_days": current_user.total_checkin_days,
            "multiplier": multiplier,
        },
        message=f"签到成功！连续签到{continuous_days}天"
    )


@router.get("/status")
async def get_checkin_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取今日签到状态"""
    today = date.today()
    
    result = await db.execute(
        select(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date == today
        )
    )
    record = result.scalar_one_or_none()
    
    # 计算明天可获得的奖励
    continuous = current_user.continuous_checkin_days or 0
    tomorrow_multiplier = min(continuous + 1, 7) if record else min(1, 7)
    
    return success(data={
        "is_checked_in": record is not None,
        "continuous_days": current_user.continuous_checkin_days or 0,
        "total_checkin_days": current_user.total_checkin_days or 0,
        "tomorrow_reward_multiplier": tomorrow_multiplier,
        "base_reward": 5,
    })


@router.get("/calendar")
async def get_checkin_calendar(
    year: int = Query(None, description="年份"),
    month: int = Query(None, description="月份"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取签到日历"""
    today = date.today()
    year = year or today.year
    month = month or today.month
    
    # 计算月份范围
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    # 查询该月签到记录
    result = await db.execute(
        select(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date >= start_date,
            CheckinRecord.checkin_date <= end_date
        )
    )
    records = result.scalars().all()
    
    # 构建签到日期列表
    checkin_dates = []
    for r in records:
        checkin_dates.append({
            "date": r.checkin_date.strftime("%Y-%m-%d"),
            "continuous_days": r.continuous_days,
            "sport_coins_earned": r.sport_coins_earned,
            "food_coins_earned": r.food_coins_earned,
        })
    
    return success(data={
        "year": year,
        "month": month,
        "checkin_dates": checkin_dates,
        "total_days": len(checkin_dates),
    })


@router.get("/stats")
async def get_checkin_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取签到统计"""
    # 本月签到天数
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    month_count = (await db.execute(
        select(func.count()).select_from(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date >= month_start
        )
    )).scalar()
    
    # 最长连续签到天数
    max_continuous = (await db.execute(
        select(func.max(CheckinRecord.continuous_days)).where(
            CheckinRecord.user_id == current_user.id
        )
    )).scalar() or 0
    
    # 累计获得积分
    total_sport_coins = (await db.execute(
        select(func.sum(CheckinRecord.sport_coins_earned)).where(
            CheckinRecord.user_id == current_user.id
        )
    )).scalar() or 0
    
    total_food_coins = (await db.execute(
        select(func.sum(CheckinRecord.food_coins_earned)).where(
            CheckinRecord.user_id == current_user.id
        )
    )).scalar() or 0
    
    return success(data={
        "total_checkin_days": current_user.total_checkin_days or 0,
        "continuous_checkin_days": current_user.continuous_checkin_days or 0,
        "month_checkin_days": month_count,
        "max_continuous_days": max_continuous,
        "total_sport_coins_earned": total_sport_coins,
        "total_food_coins_earned": total_food_coins,
    })



















