"""
用户接口
GET /user/profile - 获取个人信息
PUT /user/profile - 更新个人信息
POST /user/avatar - 上传头像
GET /user/health-profile - 获取健康档案
PUT /user/health-profile - 更新健康档案
GET /user/{user_id}/profile - 获取其他用户公开信息
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.config import settings
from app.models.user import User, UserHealthProfile
from app.models.community import Post, UserFollow
from app.schemas.user import (
    UserProfile, UserProfileUpdate, 
    UserHealthProfileSchema, UserHealthProfileUpdate
)
from app.utils.security import get_current_user, get_current_user_optional
from app.utils.response import success, error

router = APIRouter(prefix="/user", tags=["用户"])


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return success(data=UserProfile.model_validate(current_user).model_dump())


@router.put("/profile")
async def update_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return success(
        data=UserProfile.model_validate(current_user).model_dump(),
        message="更新成功"
    )


@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传头像"""
    # 验证文件类型
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        return error(400, "不支持的图片格式")
    
    # 验证文件大小
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        return error(400, "文件大小超过限制")
    
    # 生成文件名
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, "avatars", filename)
    
    # 保存文件
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(content)
    
    # 更新用户头像
    avatar_url = f"/uploads/avatars/{filename}"
    current_user.avatar = avatar_url
    await db.commit()
    
    return success(
        data={"avatar": avatar_url},
        message="上传成功"
    )


@router.get("/health-profile")
async def get_health_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取健康档案"""
    result = await db.execute(
        select(UserHealthProfile).where(UserHealthProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        # 创建空的健康档案
        profile = UserHealthProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    
    return success(data=UserHealthProfileSchema.model_validate(profile).model_dump())


@router.put("/health-profile")
async def update_health_profile(
    data: UserHealthProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新健康档案"""
    result = await db.execute(
        select(UserHealthProfile).where(UserHealthProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        profile = UserHealthProfile(user_id=current_user.id)
        db.add(profile)
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return success(
        data=UserHealthProfileSchema.model_validate(profile).model_dump(),
        message="更新成功"
    )


@router.get("/{user_id}/profile")
async def get_user_public_profile(
    user_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取其他用户公开信息"""
    # 查询用户
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        return error(404, "用户不存在")
    
    # 统计获赞数
    like_count_result = await db.execute(
        select(func.sum(Post.like_count)).where(Post.user_id == user_id)
    )
    like_count = like_count_result.scalar() or 0
    
    # 检查是否关注
    is_followed = False
    if current_user:
        follow_result = await db.execute(
            select(UserFollow).where(
                UserFollow.user_id == current_user.id,
                UserFollow.follow_user_id == user_id
            )
        )
        is_followed = follow_result.scalar_one_or_none() is not None
    
    return success(data={
        "id": user.id,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "bio": None,  # 可以添加个人简介字段
        "gender": user.gender,
        "user_level": user.user_level,
        "follower_count": user.follower_count,
        "following_count": user.following_count,
        "like_count": int(like_count),
        "is_followed": is_followed
    })


