"""
用户管理接口
GET /user/list - 用户列表
GET /user/{id} - 用户详情
PUT /user/{id}/status - 禁用/启用用户
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, or_
from typing import Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User, UserHealthProfile
from app.models.system import Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/user", tags=["用户管理"])


class StatusUpdate(BaseModel):
    """状态更新"""
    status: int = Field(..., ge=0, le=1, description="状态: 0禁用, 1启用")
    reason: Optional[str] = Field(None, max_length=200, description="原因")


@router.get("/list")
async def get_user_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[int] = Query(None, description="状态筛选"),
    member_level: Optional[int] = Query(None, description="会员等级筛选: 0普通 1月卡 2年卡 3终身"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取用户列表"""
    conditions = []
    
    if keyword:
        conditions.append(
            or_(
                User.nickname.like(f"%{keyword}%"),
                User.phone.like(f"%{keyword}%")
            )
        )
    
    if status is not None:
        conditions.append(User.status == status)
    
    if member_level is not None:
        conditions.append(User.member_level == member_level)
    
    # 查询总数
    count_query = select(func.count()).select_from(User)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(User)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(User.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    items = []
    for u in users:
        items.append({
            "id": u.id,
            "openid": u.openid[:10] + "..." if u.openid else None,
            "nickname": u.nickname,
            "avatar": u.avatar,
            "phone": u.phone,
            "gender": u.gender,
            "member_level": u.member_level,
            "member_expire_time": u.member_expire_time.strftime("%Y-%m-%d") if u.member_expire_time else None,
            "sport_coins": u.sport_coins,
            "food_coins": u.food_coins,
            "user_level": u.user_level,
            "status": u.status,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/{user_id}")
async def get_user_detail(
    user_id: int,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取用户详情"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return error(404, "用户不存在")
    
    # 获取健康档案
    health_result = await db.execute(
        select(UserHealthProfile).where(UserHealthProfile.user_id == user_id)
    )
    health_profile = health_result.scalar_one_or_none()
    
    health_data = None
    if health_profile:
        health_data = {
            "health_goal": health_profile.health_goal,
            "target_weight": float(health_profile.target_weight) if health_profile.target_weight else None,
            "preferred_sports": health_profile.preferred_sports,
            "daily_exercise_minutes": health_profile.daily_exercise_minutes,
            "has_injury": health_profile.has_injury,
            "chronic_diseases": health_profile.chronic_diseases,
            "diet_habit": health_profile.diet_habit,
            "allergies": health_profile.allergies,
        }
    
    return success(data={
        "id": user.id,
        "openid": user.openid,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "phone": user.phone,
        "gender": user.gender,
        "birthday": user.birthday.strftime("%Y-%m-%d") if user.birthday else None,
        "height": float(user.height) if user.height else None,
        "weight": float(user.weight) if user.weight else None,
        "member_level": user.member_level,
        "member_expire_time": user.member_expire_time.strftime("%Y-%m-%d %H:%M:%S") if user.member_expire_time else None,
        "sport_coins": user.sport_coins,
        "food_coins": user.food_coins,
        "balance": float(user.balance) if user.balance else 0,
        "continuous_checkin_days": user.continuous_checkin_days,
        "last_checkin_date": user.last_checkin_date.strftime("%Y-%m-%d") if user.last_checkin_date else None,
        "user_level": user.user_level,
        "follower_count": user.follower_count,
        "following_count": user.following_count,
        "status": user.status,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S") if user.created_at else None,
        "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else None,
        "health_profile": health_data,
    })


@router.put("/{user_id}/status")
async def update_user_status(
    user_id: int,
    data: StatusUpdate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """禁用/启用用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return error(404, "用户不存在")
    
    old_status = user.status
    user.status = data.status
    
    # 记录操作日志
    action = "enable_user" if data.status == 1 else "disable_user"
    content = f"{'启用' if data.status == 1 else '禁用'}用户: {user.nickname}"
    if data.reason:
        content += f", 原因: {data.reason}"
    
    log = AdminLog(
        admin_id=admin.id,
        action=action,
        target_type="user",
        target_id=user_id,
        content=content,
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="操作成功")


