"""
运动目标接口
GET /sport-goal/list - 目标列表
POST /sport-goal - 创建目标
PUT /sport-goal/{id} - 更新目标
DELETE /sport-goal/{id} - 删除目标
GET /sport-goal/stats - 目标统计
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, date, timedelta
from typing import Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.sport import SportGoal, SportRecord
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/sport-goal", tags=["运动目标"])


class GoalCreate(BaseModel):
    """创建目标"""
    goal_type: str = Field(..., description="目标类型: duration/distance/calories/times")
    target_value: int = Field(..., ge=1, description="目标值")
    unit: str = Field(..., description="单位")
    period: str = Field("daily", description="周期: daily/weekly/monthly")


class GoalUpdate(BaseModel):
    """更新目标"""
    target_value: Optional[int] = Field(None, ge=1, description="目标值")


@router.get("/list")
async def get_goals(
    period: Optional[str] = Query(None, description="周期筛选"),
    is_active: int = Query(1, description="是否进行中"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取运动目标列表"""
    today = date.today()
    
    conditions = [SportGoal.user_id == current_user.id]
    
    if period:
        conditions.append(SportGoal.period == period)
    
    if is_active:
        conditions.append(SportGoal.end_date >= datetime.combine(today, datetime.min.time()))
    
    result = await db.execute(
        select(SportGoal).where(*conditions).order_by(SportGoal.created_at.desc())
    )
    goals = result.scalars().all()
    
    items = []
    for g in goals:
        progress = round(g.current_value / g.target_value * 100, 1) if g.target_value > 0 else 0
        items.append({
            "id": g.id,
            "goal_type": g.goal_type,
            "target_value": g.target_value,
            "current_value": g.current_value,
            "unit": g.unit,
            "period": g.period,
            "progress": min(progress, 100),
            "is_completed": g.is_completed,
            "start_date": g.start_date.strftime("%Y-%m-%d") if g.start_date else None,
            "end_date": g.end_date.strftime("%Y-%m-%d") if g.end_date else None,
        })
    
    return success(data=items)


@router.post("")
async def create_goal(
    data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建运动目标"""
    today = date.today()
    
    # 计算目标周期
    if data.period == "daily":
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
    elif data.period == "weekly":
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = datetime.combine(start_of_week, datetime.min.time())
        end_date = datetime.combine(end_of_week, datetime.max.time())
    else:  # monthly
        start_date = datetime.combine(date(today.year, today.month, 1), datetime.min.time())
        if today.month == 12:
            end_date = datetime.combine(date(today.year + 1, 1, 1) - timedelta(days=1), datetime.max.time())
        else:
            end_date = datetime.combine(date(today.year, today.month + 1, 1) - timedelta(days=1), datetime.max.time())
    
    # 检查是否已有相同类型的目标
    existing = await db.execute(
        select(SportGoal).where(
            SportGoal.user_id == current_user.id,
            SportGoal.goal_type == data.goal_type,
            SportGoal.period == data.period,
            SportGoal.end_date >= datetime.now()
        )
    )
    if existing.scalar_one_or_none():
        return error(400, "该周期已存在相同类型的目标")
    
    # 创建目标
    goal = SportGoal(
        user_id=current_user.id,
        goal_type=data.goal_type,
        target_value=data.target_value,
        current_value=0,
        unit=data.unit,
        period=data.period,
        start_date=start_date,
        end_date=end_date,
    )
    
    # 计算当前进度
    await _update_goal_progress(goal, current_user.id, db)
    
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    
    return success(
        data={"id": goal.id},
        message="目标创建成功"
    )


@router.put("/{goal_id}")
async def update_goal(
    goal_id: int,
    data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新运动目标"""
    result = await db.execute(
        select(SportGoal).where(
            SportGoal.id == goal_id,
            SportGoal.user_id == current_user.id
        )
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        return error(404, "目标不存在")
    
    if data.target_value:
        goal.target_value = data.target_value
        # 检查是否完成
        goal.is_completed = 1 if goal.current_value >= goal.target_value else 0
    
    await db.commit()
    
    return success(message="更新成功")


@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除运动目标"""
    result = await db.execute(
        select(SportGoal).where(
            SportGoal.id == goal_id,
            SportGoal.user_id == current_user.id
        )
    )
    goal = result.scalar_one_or_none()
    
    if not goal:
        return error(404, "目标不存在")
    
    await db.delete(goal)
    await db.commit()
    
    return success(message="删除成功")


@router.get("/stats")
async def get_goal_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取目标统计"""
    today = date.today()
    now = datetime.now()
    
    # 进行中的目标数
    active_count = (await db.execute(
        select(func.count()).select_from(SportGoal).where(
            SportGoal.user_id == current_user.id,
            SportGoal.end_date >= now,
            SportGoal.is_completed == 0
        )
    )).scalar()
    
    # 已完成的目标数
    completed_count = (await db.execute(
        select(func.count()).select_from(SportGoal).where(
            SportGoal.user_id == current_user.id,
            SportGoal.is_completed == 1
        )
    )).scalar()
    
    # 本月完成目标数
    month_start = date(today.year, today.month, 1)
    month_completed = (await db.execute(
        select(func.count()).select_from(SportGoal).where(
            SportGoal.user_id == current_user.id,
            SportGoal.is_completed == 1,
            SportGoal.start_date >= datetime.combine(month_start, datetime.min.time())
        )
    )).scalar()
    
    return success(data={
        "active_count": active_count,
        "completed_count": completed_count,
        "month_completed_count": month_completed,
    })


async def _update_goal_progress(goal: SportGoal, user_id: int, db: AsyncSession):
    """更新目标进度"""
    # 根据目标类型查询运动记录
    conditions = [
        SportRecord.user_id == user_id,
        SportRecord.start_time >= goal.start_date,
        SportRecord.start_time <= goal.end_date
    ]
    
    if goal.goal_type == "duration":
        # 总时长
        result = await db.execute(
            select(func.sum(SportRecord.duration)).where(*conditions)
        )
        goal.current_value = result.scalar() or 0
        
    elif goal.goal_type == "distance":
        # 总距离
        result = await db.execute(
            select(func.sum(SportRecord.distance)).where(*conditions)
        )
        goal.current_value = int(result.scalar() or 0)
        
    elif goal.goal_type == "calories":
        # 总卡路里
        result = await db.execute(
            select(func.sum(SportRecord.calories)).where(*conditions)
        )
        goal.current_value = result.scalar() or 0
        
    elif goal.goal_type == "times":
        # 运动次数
        result = await db.execute(
            select(func.count()).select_from(SportRecord).where(*conditions)
        )
        goal.current_value = result.scalar() or 0
    
    # 检查是否完成
    if goal.current_value >= goal.target_value:
        goal.is_completed = 1























