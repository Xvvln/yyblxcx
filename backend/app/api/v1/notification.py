"""
通知接口
GET /notification/list - 通知列表
POST /notification/read - 标记已读
POST /notification/read-all - 全部标记已读
GET /notification/unread-count - 未读数量
DELETE /notification/{id} - 删除通知
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, update
from typing import Optional, List
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.system import Notification
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/notification", tags=["通知"])


class ReadRequest(BaseModel):
    """标记已读请求"""
    ids: List[int] = Field(..., description="通知ID列表")


@router.get("/list")
async def get_notifications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    type: Optional[str] = Query(None, description="通知类型"),
    is_read: Optional[int] = Query(None, description="是否已读"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取通知列表"""
    conditions = [Notification.user_id == current_user.id]
    
    if type:
        conditions.append(Notification.type == type)
    
    if is_read is not None:
        conditions.append(Notification.is_read == is_read)
    
    # 查询总数
    count_query = select(func.count()).select_from(Notification).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Notification).where(*conditions).order_by(
        desc(Notification.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    items = []
    for n in notifications:
        items.append({
            "id": n.id,
            "type": n.type,
            "title": n.title,
            "content": n.content,
            "related_id": n.related_id,
            "related_type": n.related_type,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S") if n.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/read")
async def mark_read(
    data: ReadRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """标记已读"""
    await db.execute(
        update(Notification).where(
            Notification.id.in_(data.ids),
            Notification.user_id == current_user.id
        ).values(is_read=1)
    )
    await db.commit()
    
    return success(message="标记成功")


@router.post("/read-all")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """全部标记已读"""
    await db.execute(
        update(Notification).where(
            Notification.user_id == current_user.id,
            Notification.is_read == 0
        ).values(is_read=1)
    )
    await db.commit()
    
    return success(message="全部标记成功")


@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取未读数量"""
    count = (await db.execute(
        select(func.count()).select_from(Notification).where(
            Notification.user_id == current_user.id,
            Notification.is_read == 0
        )
    )).scalar()
    
    return success(data={"count": count})


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除通知"""
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        return error(404, "通知不存在")
    
    await db.delete(notification)
    await db.commit()
    
    return success(message="删除成功")




















