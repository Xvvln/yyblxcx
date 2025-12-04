"""
用户统计接口
GET /stats/health - 健康数据趋势
GET /stats/sport - 运动数据统计
GET /stats/food - 饮食数据统计
GET /stats/overview - 个人数据概览
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, date, timedelta
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.health import HealthScreening
from app.models.sport import SportRecord
from app.models.food import FoodRecord
from app.models.points import CheckinRecord
from app.utils.security import get_current_user
from app.utils.response import success

router = APIRouter(prefix="/stats", tags=["数据统计"])


@router.get("/overview")
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取个人数据概览"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = date(today.year, today.month, 1)
    
    # 本周运动统计
    week_sport = await db.execute(
        select(
            func.sum(SportRecord.duration),
            func.sum(SportRecord.calories),
            func.count()
        ).where(
            SportRecord.user_id == current_user.id,
            SportRecord.start_time >= datetime.combine(week_start, datetime.min.time())
        )
    )
    week_sport_data = week_sport.first()
    
    # 本月饮食记录数
    month_food_count = (await db.execute(
        select(func.count()).select_from(FoodRecord).where(
            FoodRecord.user_id == current_user.id,
            FoodRecord.record_date >= month_start
        )
    )).scalar()
    
    # 本月签到天数
    month_checkin = (await db.execute(
        select(func.count()).select_from(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date >= month_start
        )
    )).scalar()
    
    # 最近一次健康筛查
    latest_screening = (await db.execute(
        select(HealthScreening).where(
            HealthScreening.user_id == current_user.id
        ).order_by(HealthScreening.created_at.desc()).limit(1)
    )).scalar_one_or_none()
    
    return success(data={
        "week_sport": {
            "total_duration": week_sport_data[0] or 0,
            "total_calories": week_sport_data[1] or 0,
            "workout_count": week_sport_data[2] or 0,
        },
        "month_food_records": month_food_count,
        "month_checkin_days": month_checkin,
        "continuous_checkin_days": current_user.continuous_checkin_days or 0,
        "latest_bmi": float(latest_screening.bmi) if latest_screening and latest_screening.bmi else None,
        "risk_level": latest_screening.risk_level if latest_screening else None,
        "sport_coins": current_user.sport_coins,
        "food_coins": current_user.food_coins,
        "user_level": current_user.user_level,
    })


@router.get("/health")
async def get_health_trend(
    days: int = Query(30, ge=7, le=90, description="天数范围"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取健康数据趋势"""
    start_date = datetime.now() - timedelta(days=days)
    
    result = await db.execute(
        select(HealthScreening).where(
            HealthScreening.user_id == current_user.id,
            HealthScreening.created_at >= start_date
        ).order_by(HealthScreening.created_at)
    )
    screenings = result.scalars().all()
    
    # 构建趋势数据
    bmi_trend = []
    weight_trend = []
    heart_rate_trend = []
    blood_pressure_trend = []
    
    for s in screenings:
        date_str = s.created_at.strftime("%Y-%m-%d")
        
        if s.bmi:
            bmi_trend.append({"date": date_str, "value": float(s.bmi)})
        
        if s.weight:
            weight_trend.append({"date": date_str, "value": float(s.weight)})
        
        if s.heart_rate:
            heart_rate_trend.append({"date": date_str, "value": s.heart_rate})
        
        if s.blood_pressure_high and s.blood_pressure_low:
            blood_pressure_trend.append({
                "date": date_str,
                "high": s.blood_pressure_high,
                "low": s.blood_pressure_low
            })
    
    return success(data={
        "bmi_trend": bmi_trend,
        "weight_trend": weight_trend,
        "heart_rate_trend": heart_rate_trend,
        "blood_pressure_trend": blood_pressure_trend,
    })


@router.get("/sport")
async def get_sport_stats(
    days: int = Query(30, ge=7, le=90, description="天数范围"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取运动数据统计"""
    start_date = datetime.now() - timedelta(days=days)
    
    # 按日期统计
    result = await db.execute(
        select(SportRecord).where(
            SportRecord.user_id == current_user.id,
            SportRecord.start_time >= start_date
        ).order_by(SportRecord.start_time)
    )
    records = result.scalars().all()
    
    # 按日期分组
    daily_stats = {}
    sport_type_stats = {}
    total_duration = 0
    total_calories = 0
    total_distance = 0
    
    for r in records:
        date_str = r.start_time.strftime("%Y-%m-%d")
        
        # 日统计
        if date_str not in daily_stats:
            daily_stats[date_str] = {"duration": 0, "calories": 0}
        daily_stats[date_str]["duration"] += r.duration
        daily_stats[date_str]["calories"] += r.calories
        
        # 运动类型统计
        if r.sport_type not in sport_type_stats:
            sport_type_stats[r.sport_type] = {"count": 0, "duration": 0}
        sport_type_stats[r.sport_type]["count"] += 1
        sport_type_stats[r.sport_type]["duration"] += r.duration
        
        # 总计
        total_duration += r.duration
        total_calories += r.calories
        if r.distance:
            total_distance += float(r.distance)
    
    # 转换为列表
    daily_trend = [{"date": k, **v} for k, v in sorted(daily_stats.items())]
    sport_types = [{"type": k, **v} for k, v in sport_type_stats.items()]
    
    return success(data={
        "daily_trend": daily_trend,
        "sport_types": sport_types,
        "total_duration": total_duration,
        "total_calories": total_calories,
        "total_distance": round(total_distance, 2),
        "workout_count": len(records),
        "avg_duration": round(total_duration / len(records), 1) if records else 0,
    })


@router.get("/food")
async def get_food_stats(
    days: int = Query(30, ge=7, le=90, description="天数范围"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取饮食数据统计"""
    start_date = date.today() - timedelta(days=days)
    
    result = await db.execute(
        select(FoodRecord).where(
            FoodRecord.user_id == current_user.id,
            FoodRecord.record_date >= start_date
        ).order_by(FoodRecord.record_date)
    )
    records = result.scalars().all()
    
    # 按日期分组
    daily_stats = {}
    meal_type_stats = {
        "breakfast": {"count": 0, "calories": 0},
        "lunch": {"count": 0, "calories": 0},
        "dinner": {"count": 0, "calories": 0},
        "snack": {"count": 0, "calories": 0},
    }
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for r in records:
        date_str = r.record_date.strftime("%Y-%m-%d")
        
        # 日统计
        if date_str not in daily_stats:
            daily_stats[date_str] = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        daily_stats[date_str]["calories"] += r.calories
        daily_stats[date_str]["protein"] += float(r.protein)
        daily_stats[date_str]["carbs"] += float(r.carbs)
        daily_stats[date_str]["fat"] += float(r.fat)
        
        # 餐次统计
        if r.meal_type in meal_type_stats:
            meal_type_stats[r.meal_type]["count"] += 1
            meal_type_stats[r.meal_type]["calories"] += r.calories
        
        # 总计
        total_calories += r.calories
        total_protein += float(r.protein)
        total_carbs += float(r.carbs)
        total_fat += float(r.fat)
    
    # 转换为列表
    daily_trend = [{"date": k, **v} for k, v in sorted(daily_stats.items())]
    
    return success(data={
        "daily_trend": daily_trend,
        "meal_type_stats": meal_type_stats,
        "total_calories": total_calories,
        "total_protein": round(total_protein, 1),
        "total_carbs": round(total_carbs, 1),
        "total_fat": round(total_fat, 1),
        "record_count": len(records),
        "avg_daily_calories": round(total_calories / days, 1) if days > 0 else 0,
    })


















