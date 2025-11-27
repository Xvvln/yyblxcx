"""
运动接口
POST /sport/record - 提交运动记录
GET /sport/records - 运动记录列表
POST /sport/checkin - 运动打卡
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.sport import SportRecord
from app.models.points import CheckinRecord, CoinRecord
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.utils.helpers import calculate_calories

router = APIRouter(prefix="/sport", tags=["运动"])


class SportRecordCreate(BaseModel):
    """创建运动记录"""
    sport_type: str = Field(..., max_length=50, description="运动类型")
    sport_name: Optional[str] = Field(None, max_length=50, description="运动名称")
    duration: int = Field(..., ge=1, description="时长(分钟)")
    distance: Optional[Decimal] = Field(None, description="距离(米)")
    avg_pace: Optional[Decimal] = Field(None, description="平均配速")
    avg_heart_rate: Optional[int] = Field(None, description="平均心率")
    max_heart_rate: Optional[int] = Field(None, description="最大心率")
    weather: Optional[str] = Field(None, max_length=20, description="天气")
    feeling: Optional[int] = Field(3, ge=1, le=5, description="感受1-5")
    notes: Optional[str] = Field(None, description="备注")
    start_time: datetime = Field(..., description="开始时间")
    end_time: datetime = Field(..., description="结束时间")
    gps_track: Optional[dict] = Field(None, description="GPS轨迹")


@router.post("/record")
async def create_sport_record(
    data: SportRecordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交运动记录"""
    # 计算消耗卡路里
    weight = float(current_user.weight) if current_user.weight else 60
    calories = calculate_calories(data.sport_type, data.duration, weight)
    
    # 计算获得的运动币（每10分钟1个，最多50个）
    coins_earned = min(data.duration // 10, 50)
    
    # 创建运动记录
    record = SportRecord(
        user_id=current_user.id,
        sport_type=data.sport_type,
        sport_name=data.sport_name,
        duration=data.duration,
        distance=data.distance,
        calories=calories,
        avg_pace=data.avg_pace,
        avg_heart_rate=data.avg_heart_rate,
        max_heart_rate=data.max_heart_rate,
        weather=data.weather,
        feeling=data.feeling,
        notes=data.notes,
        start_time=data.start_time,
        end_time=data.end_time,
        gps_track=data.gps_track,  # GPS轨迹存储暂缓
        coins_earned=coins_earned,
    )
    
    db.add(record)
    
    # 更新用户运动币
    current_user.sport_coins += coins_earned
    
    # 记录积分变动
    coin_record = CoinRecord(
        user_id=current_user.id,
        coin_type="sport",
        amount=coins_earned,
        balance=current_user.sport_coins,
        source="sport_record",
        source_id=None,  # 稍后更新
        description=f"运动{data.duration}分钟获得"
    )
    db.add(coin_record)
    
    await db.commit()
    await db.refresh(record)
    
    # 更新积分记录的source_id
    coin_record.source_id = record.id
    await db.commit()
    
    return success(
        data={
            "id": record.id,
            "calories": calories,
            "coins_earned": coins_earned
        },
        message="运动记录提交成功"
    )


@router.get("/records")
async def get_sport_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    sport_type: Optional[str] = Query(None, description="运动类型筛选"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取运动记录列表"""
    # 构建查询条件
    conditions = [SportRecord.user_id == current_user.id]
    if sport_type:
        conditions.append(SportRecord.sport_type == sport_type)
    
    # 查询总数
    count_query = select(func.count()).select_from(SportRecord).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(SportRecord).where(*conditions).order_by(
        desc(SportRecord.start_time)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "sport_type": r.sport_type,
            "sport_name": r.sport_name,
            "duration": r.duration,
            "distance": float(r.distance) if r.distance else None,
            "calories": r.calories,
            "coins_earned": r.coins_earned,
            "start_time": r.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "feeling": r.feeling,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/checkin")
async def sport_checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """运动打卡"""
    today = date.today()
    
    # 检查今日是否已打卡
    result = await db.execute(
        select(CheckinRecord).where(
            CheckinRecord.user_id == current_user.id,
            CheckinRecord.checkin_date == today
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return error(400, "今日已打卡")
    
    # 检查是否连续打卡
    is_continuous = False
    continuous_days = 1
    
    if current_user.last_checkin_date:
        diff = (today - current_user.last_checkin_date).days
        if diff == 1:
            is_continuous = True
            continuous_days = current_user.continuous_checkin_days + 1
    
    # 计算奖励（连续打卡奖励翻倍，最多5倍）
    base_reward = 5
    multiplier = min(continuous_days, 5)
    sport_coins_earned = base_reward * multiplier
    
    # 创建打卡记录
    checkin = CheckinRecord(
        user_id=current_user.id,
        checkin_date=today,
        sport_coins_earned=sport_coins_earned,
        is_continuous=1 if is_continuous else 0,
        continuous_days=continuous_days,
    )
    db.add(checkin)
    
    # 更新用户信息
    current_user.sport_coins += sport_coins_earned
    current_user.last_checkin_date = today
    current_user.continuous_checkin_days = continuous_days if is_continuous else 1
    
    # 记录积分变动
    coin_record = CoinRecord(
        user_id=current_user.id,
        coin_type="sport",
        amount=sport_coins_earned,
        balance=current_user.sport_coins,
        source="checkin",
        description=f"连续打卡{continuous_days}天"
    )
    db.add(coin_record)
    
    await db.commit()
    
    return success(
        data={
            "sport_coins_earned": sport_coins_earned,
            "continuous_days": continuous_days,
            "total_sport_coins": current_user.sport_coins
        },
        message="打卡成功"
    )


