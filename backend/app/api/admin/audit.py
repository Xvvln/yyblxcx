"""
内容审核接口
GET /audit/posts - 待审核动态列表
PUT /audit/post/{id} - 审核动态
GET /audit/comments - 待审核评论列表
PUT /audit/comment/{id} - 审核评论
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.community import Post, PostComment
from app.models.system import Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/audit", tags=["内容审核"])


class AuditRequest(BaseModel):
    """审核请求"""
    status: int = Field(..., description="审核状态: 1通过, 2拒绝")
    reason: Optional[str] = Field(None, max_length=200, description="拒绝原因")


@router.get("/posts")
async def get_pending_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[int] = Query(None, description="状态筛选: 0待审核, 1已通过, 2已拒绝"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取动态列表（审核用）"""
    conditions = []
    
    if status is not None:
        conditions.append(Post.status == status)
    
    # 查询总数
    count_query = select(func.count()).select_from(Post)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Post)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(Post.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    posts = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([p.user_id for p in posts]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    items = []
    for p in posts:
        user = users.get(p.user_id)
        items.append({
            "id": p.id,
            "content": p.content,
            "images": p.images,
            "video_url": p.video_url,
            "location": p.location,
            "status": p.status,
            "view_count": p.view_count,
            "like_count": p.like_count,
            "comment_count": p.comment_count,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.put("/post/{post_id}")
async def audit_post(
    post_id: int,
    data: AuditRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """审核动态"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        return error(404, "动态不存在")
    
    post.status = data.status
    
    # 记录操作日志
    action = "approve_post" if data.status == 1 else "reject_post"
    content = f"{'通过' if data.status == 1 else '拒绝'}动态审核"
    if data.reason:
        content += f", 原因: {data.reason}"
    
    log = AdminLog(
        admin_id=admin.id,
        action=action,
        target_type="post",
        target_id=post_id,
        content=content,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="审核完成")


@router.get("/comments")
async def get_pending_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[int] = Query(None, description="状态筛选: 0待审核, 1已通过, 2已拒绝"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取评论列表（审核用）"""
    conditions = []
    
    if status is not None:
        conditions.append(PostComment.status == status)
    
    # 查询总数
    count_query = select(func.count()).select_from(PostComment)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(PostComment)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(PostComment.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    comments = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([c.user_id for c in comments]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    items = []
    for c in comments:
        user = users.get(c.user_id)
        items.append({
            "id": c.id,
            "post_id": c.post_id,
            "content": c.content,
            "status": c.status,
            "like_count": c.like_count,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
            },
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.put("/comment/{comment_id}")
async def audit_comment(
    comment_id: int,
    data: AuditRequest,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """审核评论"""
    result = await db.execute(select(PostComment).where(PostComment.id == comment_id))
    comment = result.scalar_one_or_none()
    
    if not comment:
        return error(404, "评论不存在")
    
    comment.status = data.status
    
    # 记录操作日志
    action = "approve_comment" if data.status == 1 else "reject_comment"
    content = f"{'通过' if data.status == 1 else '拒绝'}评论审核"
    if data.reason:
        content += f", 原因: {data.reason}"
    
    log = AdminLog(
        admin_id=admin.id,
        action=action,
        target_type="comment",
        target_id=comment_id,
        content=content,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="审核完成")




















