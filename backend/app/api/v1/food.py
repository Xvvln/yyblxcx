"""
饮食接口
POST /food/record - 提交饮食记录
GET /food/records - 饮食记录列表
POST /food/checkin - 饮食打卡
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
from app.models.food import FoodRecord
from app.models.points import CoinRecord
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/food", tags=["饮食"])


class FoodRecordCreate(BaseModel):
    """创建饮食记录"""
    meal_type: str = Field(..., description="餐次: breakfast/lunch/dinner/snack")
    record_date: date = Field(..., description="记录日期")
    food_name: str = Field(..., max_length=100, description="食物名称")
    food_image: Optional[str] = Field(None, description="食物图片")
    amount: Optional[Decimal] = Field(None, description="份量(克)")
    calories: Optional[int] = Field(0, description="热量(大卡)")
    protein: Optional[Decimal] = Field(Decimal("0"), description="蛋白质(克)")
    carbs: Optional[Decimal] = Field(Decimal("0"), description="碳水(克)")
    fat: Optional[Decimal] = Field(Decimal("0"), description="脂肪(克)")
    fiber: Optional[Decimal] = Field(Decimal("0"), description="膳食纤维(克)")
    notes: Optional[str] = Field(None, description="备注")


@router.post("/record")
async def create_food_record(
    data: FoodRecordCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交饮食记录"""
    # 计算获得的膳食币（每条记录3个）
    coins_earned = 3
    
    # 创建饮食记录
    record = FoodRecord(
        user_id=current_user.id,
        meal_type=data.meal_type,
        record_date=data.record_date,
        food_name=data.food_name,
        food_image=data.food_image,
        amount=data.amount,
        calories=data.calories or 0,
        protein=data.protein or Decimal("0"),
        carbs=data.carbs or Decimal("0"),
        fat=data.fat or Decimal("0"),
        fiber=data.fiber or Decimal("0"),
        notes=data.notes,
        coins_earned=coins_earned,
    )
    
    db.add(record)
    
    # 更新用户膳食币
    current_user.food_coins += coins_earned
    
    # 记录积分变动
    coin_record = CoinRecord(
        user_id=current_user.id,
        coin_type="food",
        amount=coins_earned,
        balance=current_user.food_coins,
        source="food_record",
        description=f"记录{data.food_name}"
    )
    db.add(coin_record)
    
    await db.commit()
    await db.refresh(record)
    
    return success(
        data={
            "id": record.id,
            "coins_earned": coins_earned
        },
        message="饮食记录提交成功"
    )


@router.get("/records")
async def get_food_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    record_date: Optional[date] = Query(None, description="日期筛选"),
    meal_type: Optional[str] = Query(None, description="餐次筛选"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取饮食记录列表"""
    # 构建查询条件
    conditions = [FoodRecord.user_id == current_user.id]
    if record_date:
        conditions.append(FoodRecord.record_date == record_date)
    if meal_type:
        conditions.append(FoodRecord.meal_type == meal_type)
    
    # 查询总数
    count_query = select(func.count()).select_from(FoodRecord).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(FoodRecord).where(*conditions).order_by(
        desc(FoodRecord.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "meal_type": r.meal_type,
            "record_date": r.record_date.strftime("%Y-%m-%d"),
            "food_name": r.food_name,
            "food_image": r.food_image,
            "calories": r.calories,
            "protein": float(r.protein),
            "carbs": float(r.carbs),
            "fat": float(r.fat),
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/checkin")
async def food_checkin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    饮食打卡
    
    检查今日是否有饮食记录，有则完成打卡
    """
    today = date.today()
    
    # 检查今日是否有饮食记录
    result = await db.execute(
        select(func.count()).select_from(FoodRecord).where(
            FoodRecord.user_id == current_user.id,
            FoodRecord.record_date == today
        )
    )
    count = result.scalar()
    
    if count == 0:
        return error(400, "今日暂无饮食记录，请先记录饮食")
    
    # 奖励膳食币
    food_coins_earned = 5
    current_user.food_coins += food_coins_earned
    
    # 记录积分变动
    coin_record = CoinRecord(
        user_id=current_user.id,
        coin_type="food",
        amount=food_coins_earned,
        balance=current_user.food_coins,
        source="food_checkin",
        description="饮食打卡奖励"
    )
    db.add(coin_record)
    
    await db.commit()
    
    return success(
        data={
            "food_coins_earned": food_coins_earned,
            "total_food_coins": current_user.food_coins,
            "records_today": count
        },
        message="打卡成功"
    )
























