"""
提醒接口
GET /reminder/list - 提醒设置列表
POST /reminder - 添加提醒
PUT /reminder/{id} - 修改提醒
DELETE /reminder/{id} - 删除提醒
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import time
from typing import Optional, List
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.health import HealthReminder
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/reminder", tags=["提醒"])


class ReminderCreate(BaseModel):
    """创建提醒"""
    reminder_type: str = Field(..., max_length=50, description="提醒类型: drink/exercise/meal/sleep")
    reminder_time: str = Field(..., description="提醒时间 HH:MM")
    content: Optional[str] = Field(None, max_length=200, description="提醒内容")
    repeat_days: Optional[List[int]] = Field(None, description="重复日期[1-7]")
    is_enabled: int = Field(1, ge=0, le=1, description="是否启用")


class ReminderUpdate(BaseModel):
    """更新提醒"""
    reminder_type: Optional[str] = Field(None, max_length=50)
    reminder_time: Optional[str] = Field(None)
    content: Optional[str] = Field(None, max_length=200)
    repeat_days: Optional[List[int]] = Field(None)
    is_enabled: Optional[int] = Field(None, ge=0, le=1)


@router.get("/list")
async def get_reminders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取提醒设置列表"""
    result = await db.execute(
        select(HealthReminder).where(
            HealthReminder.user_id == current_user.id
        ).order_by(HealthReminder.reminder_time)
    )
    reminders = result.scalars().all()
    
    items = []
    for r in reminders:
        items.append({
            "id": r.id,
            "reminder_type": r.reminder_type,
            "reminder_time": r.reminder_time.strftime("%H:%M") if r.reminder_time else None,
            "content": r.content,
            "repeat_days": r.repeat_days,
            "is_enabled": r.is_enabled,
        })
    
    return success(data=items)


@router.post("")
async def create_reminder(
    data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加提醒"""
    # 解析时间
    try:
        hour, minute = map(int, data.reminder_time.split(":"))
        reminder_time = time(hour, minute)
    except:
        return error(400, "时间格式错误，应为 HH:MM")
    
    reminder = HealthReminder(
        user_id=current_user.id,
        reminder_type=data.reminder_type,
        reminder_time=reminder_time,
        content=data.content,
        repeat_days=data.repeat_days,
        is_enabled=data.is_enabled,
    )
    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)
    
    return success(data={"id": reminder.id}, message="添加成功")


@router.put("/{reminder_id}")
async def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改提醒"""
    result = await db.execute(
        select(HealthReminder).where(
            HealthReminder.id == reminder_id,
            HealthReminder.user_id == current_user.id
        )
    )
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        return error(404, "提醒不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # 处理时间字段
    if "reminder_time" in update_data:
        try:
            hour, minute = map(int, update_data["reminder_time"].split(":"))
            update_data["reminder_time"] = time(hour, minute)
        except:
            return error(400, "时间格式错误")
    
    for field, value in update_data.items():
        setattr(reminder, field, value)
    
    await db.commit()
    
    return success(message="修改成功")


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除提醒"""
    result = await db.execute(
        select(HealthReminder).where(
            HealthReminder.id == reminder_id,
            HealthReminder.user_id == current_user.id
        )
    )
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        return error(404, "提醒不存在")
    
    await db.delete(reminder)
    await db.commit()
    
    return success(message="删除成功")


