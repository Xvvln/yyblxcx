"""
用户反馈管理接口
GET /feedback/list - 反馈列表
GET /feedback/{id} - 反馈详情
PUT /feedback/{id} - 更新反馈状态
POST /feedback/{id}/reply - 回复反馈
DELETE /feedback/{id} - 删除反馈
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserFeedback
from app.models.system import Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/feedback", tags=["反馈管理"])


class FeedbackUpdateRequest(BaseModel):
    """更新反馈状态"""
    status: int = Field(..., ge=0, le=2, description="状态: 0待处理, 1已处理, 2已回复")


class FeedbackReplyRequest(BaseModel):
    """回复反馈"""
    reply: str = Field(..., min_length=1, max_length=500, description="回复内容")


@router.get("/list")
async def get_feedback_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[int] = Query(None, description="状态筛选: 0待处理, 1已处理, 2已回复"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取反馈列表"""
    conditions = []
    
    if status is not None:
        conditions.append(UserFeedback.status == status)
    
    if keyword:
        conditions.append(UserFeedback.content.like(f"%{keyword}%"))
    
    # 查询总数
    count_query = select(func.count()).select_from(UserFeedback)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(UserFeedback)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(UserFeedback.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    feedbacks = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([f.user_id for f in feedbacks]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    items = []
    for f in feedbacks:
        user = users.get(f.user_id)
        items.append({
            "id": f.id,
            "content": f.content,
            "images": f.images,
            "contact": f.contact,
            "status": f.status,
            "reply": f.reply,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
                "phone": user.phone if user else None,
            },
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S") if f.created_at else None,
            "updated_at": f.updated_at.strftime("%Y-%m-%d %H:%M:%S") if f.updated_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/{feedback_id}")
async def get_feedback_detail(
    feedback_id: int,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取反馈详情"""
    result = await db.execute(select(UserFeedback).where(UserFeedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        return error(404, "反馈不存在")
    
    # 获取用户信息
    user_result = await db.execute(select(User).where(User.id == feedback.user_id))
    user = user_result.scalar_one_or_none()
    
    return success(data={
        "id": feedback.id,
        "content": feedback.content,
        "images": feedback.images,
        "contact": feedback.contact,
        "status": feedback.status,
        "reply": feedback.reply,
        "user": {
            "id": user.id if user else None,
            "nickname": user.nickname if user else "未知用户",
            "avatar": user.avatar if user else None,
            "phone": user.phone if user else None,
        },
        "created_at": feedback.created_at.strftime("%Y-%m-%d %H:%M:%S") if feedback.created_at else None,
        "updated_at": feedback.updated_at.strftime("%Y-%m-%d %H:%M:%S") if feedback.updated_at else None,
    })


@router.put("/{feedback_id}")
async def update_feedback_status(
    feedback_id: int,
    data: FeedbackUpdateRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """更新反馈状态"""
    result = await db.execute(select(UserFeedback).where(UserFeedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        return error(404, "反馈不存在")
    
    old_status = feedback.status
    feedback.status = data.status
    feedback.updated_at = datetime.now()
    
    # 记录操作日志
    status_map = {0: "待处理", 1: "已处理", 2: "已回复"}
    log = AdminLog(
        admin_id=admin.id,
        action="update_feedback",
        target_type="feedback",
        target_id=feedback_id,
        content=f"更新反馈状态: {status_map.get(old_status, '未知')} -> {status_map.get(data.status, '未知')}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="状态更新成功")


@router.post("/{feedback_id}/reply")
async def reply_feedback(
    feedback_id: int,
    data: FeedbackReplyRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """回复反馈"""
    result = await db.execute(select(UserFeedback).where(UserFeedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        return error(404, "反馈不存在")
    
    feedback.reply = data.reply
    feedback.status = 2  # 已回复
    feedback.updated_at = datetime.now()
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="reply_feedback",
        target_type="feedback",
        target_id=feedback_id,
        content=f"回复用户反馈: {data.reply[:50]}...",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="回复成功")


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """删除反馈"""
    result = await db.execute(select(UserFeedback).where(UserFeedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        return error(404, "反馈不存在")
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="delete_feedback",
        target_type="feedback",
        target_id=feedback_id,
        content=f"删除用户反馈",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.delete(feedback)
    await db.commit()
    
    return success(message="删除成功")


