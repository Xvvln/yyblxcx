"""
任务接口
GET /task/daily - 今日任务列表
GET /task/progress - 任务进度
POST /task/{id}/claim - 领取任务奖励
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, datetime

from app.database import get_db
from app.models.user import User
from app.models.points import DailyTask, UserTaskRecord, CoinRecord
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/task", tags=["任务"])


@router.get("/daily")
async def get_daily_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取今日任务列表"""
    today = date.today()
    
    # 获取所有启用的任务
    result = await db.execute(
        select(DailyTask).where(DailyTask.is_active == 1).order_by(DailyTask.sort_order)
    )
    tasks = result.scalars().all()
    
    # 获取用户今日任务进度
    records_result = await db.execute(
        select(UserTaskRecord).where(
            UserTaskRecord.user_id == current_user.id,
            UserTaskRecord.task_date == today
        )
    )
    records = {r.task_id: r for r in records_result.scalars().all()}
    
    items = []
    for t in tasks:
        record = records.get(t.id)
        items.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "task_type": t.task_type,
            "target_value": t.target_value,
            "current_value": record.current_value if record else 0,
            "reward_coin_type": t.reward_coin_type,
            "reward_amount": t.reward_amount,
            "is_completed": record.is_completed if record else 0,
            "is_claimed": record.is_claimed if record else 0,
        })
    
    return success(data=items)


@router.get("/progress")
async def get_task_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取任务进度"""
    today = date.today()
    
    # 获取今日任务统计
    tasks_result = await db.execute(
        select(DailyTask).where(DailyTask.is_active == 1)
    )
    total_tasks = len(tasks_result.scalars().all())
    
    # 获取已完成任务数
    completed_result = await db.execute(
        select(UserTaskRecord).where(
            UserTaskRecord.user_id == current_user.id,
            UserTaskRecord.task_date == today,
            UserTaskRecord.is_completed == 1
        )
    )
    completed_tasks = len(completed_result.scalars().all())
    
    # 获取可领取奖励数
    claimable_result = await db.execute(
        select(UserTaskRecord).where(
            UserTaskRecord.user_id == current_user.id,
            UserTaskRecord.task_date == today,
            UserTaskRecord.is_completed == 1,
            UserTaskRecord.is_claimed == 0
        )
    )
    claimable_count = len(claimable_result.scalars().all())
    
    return success(data={
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "claimable_count": claimable_count,
        "completion_rate": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0
    })


@router.post("/{task_id}/claim")
async def claim_task_reward(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """领取任务奖励"""
    today = date.today()
    
    # 获取任务信息
    task_result = await db.execute(
        select(DailyTask).where(DailyTask.id == task_id, DailyTask.is_active == 1)
    )
    task = task_result.scalar_one_or_none()
    
    if not task:
        return error(404, "任务不存在")
    
    # 获取用户任务记录
    record_result = await db.execute(
        select(UserTaskRecord).where(
            UserTaskRecord.user_id == current_user.id,
            UserTaskRecord.task_id == task_id,
            UserTaskRecord.task_date == today
        )
    )
    record = record_result.scalar_one_or_none()
    
    if not record:
        return error(400, "任务未完成")
    
    if record.is_completed != 1:
        return error(400, "任务未完成")
    
    if record.is_claimed == 1:
        return error(400, "奖励已领取")
    
    # 发放奖励
    if task.reward_coin_type == "sport":
        current_user.sport_coins += task.reward_amount
        balance = current_user.sport_coins
    else:
        current_user.food_coins += task.reward_amount
        balance = current_user.food_coins
    
    # 记录积分变动
    coin_record = CoinRecord(
        user_id=current_user.id,
        coin_type=task.reward_coin_type,
        amount=task.reward_amount,
        balance=balance,
        source="task_reward",
        source_id=task.id,
        description=f"完成任务: {task.name}"
    )
    db.add(coin_record)
    
    # 更新领取状态
    record.is_claimed = 1
    record.claimed_at = datetime.now()
    
    await db.commit()
    
    return success(
        data={
            "reward_coin_type": task.reward_coin_type,
            "reward_amount": task.reward_amount
        },
        message="领取成功"
    )



















