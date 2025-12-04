"""
用户设置接口
GET /settings - 获取用户设置
PUT /settings - 更新用户设置
POST /settings/bind-phone - 绑定手机号
POST /settings/delete-account - 注销账号
POST /feedback - 提交反馈
GET /feedback/list - 获取反馈列表
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
import random

from app.database import get_db
from app.models.user import User, UserSettings, UserFeedback
from app.schemas.user import (
    UserSettingsSchema, UserSettingsUpdate,
    UserFeedbackCreate, UserFeedbackSchema,
    BindPhoneRequest
)
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/settings", tags=["用户设置"])

# 模拟验证码存储 (生产环境应使用Redis)
verification_codes = {}


@router.get("")
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户设置"""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == current_user.id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        # 创建默认设置
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    
    return success(data=UserSettingsSchema.model_validate(settings).model_dump())


@router.put("")
async def update_settings(
    data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户设置"""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == current_user.id)
    )
    settings = result.scalar_one_or_none()
    
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    await db.commit()
    await db.refresh(settings)
    
    return success(
        data=UserSettingsSchema.model_validate(settings).model_dump(),
        message="设置已更新"
    )


@router.post("/send-code")
async def send_verification_code(
    phone: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送验证码"""
    # 检查手机号是否已被绑定
    result = await db.execute(
        select(User).where(User.phone == phone, User.id != current_user.id)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        return error(400, "该手机号已被其他账号绑定")
    
    # 生成验证码 (生产环境应调用短信服务)
    code = str(random.randint(100000, 999999))
    verification_codes[phone] = {
        "code": code,
        "user_id": current_user.id,
        "expires": datetime.now().timestamp() + 300  # 5分钟有效
    }
    
    # 开发环境直接返回验证码
    return success(
        data={"code": code},  # 生产环境不要返回验证码
        message=f"验证码已发送: {code}"
    )


@router.post("/bind-phone")
async def bind_phone(
    data: BindPhoneRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """绑定手机号"""
    # 验证验证码
    stored = verification_codes.get(data.phone)
    if not stored:
        return error(400, "请先获取验证码")
    
    if stored["user_id"] != current_user.id:
        return error(400, "验证码无效")
    
    if datetime.now().timestamp() > stored["expires"]:
        del verification_codes[data.phone]
        return error(400, "验证码已过期")
    
    if stored["code"] != data.code:
        return error(400, "验证码错误")
    
    # 检查手机号是否已被绑定
    result = await db.execute(
        select(User).where(User.phone == data.phone, User.id != current_user.id)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        return error(400, "该手机号已被其他账号绑定")
    
    # 绑定手机号
    current_user.phone = data.phone
    await db.commit()
    
    # 清除验证码
    del verification_codes[data.phone]
    
    return success(message="手机号绑定成功")


@router.post("/unbind-phone")
async def unbind_phone(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """解绑手机号"""
    if not current_user.phone:
        return error(400, "未绑定手机号")
    
    current_user.phone = None
    await db.commit()
    
    return success(message="手机号已解绑")


@router.post("/delete-account")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """注销账号"""
    # 标记账号为已删除状态
    current_user.status = 0
    current_user.nickname = f"已注销用户{current_user.id}"
    current_user.avatar = None
    current_user.phone = None
    
    await db.commit()
    
    return success(message="账号已注销")


# 反馈相关接口
feedback_router = APIRouter(prefix="/feedback", tags=["用户反馈"])


@feedback_router.post("")
async def create_feedback(
    data: UserFeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交反馈"""
    feedback = UserFeedback(
        user_id=current_user.id,
        content=data.content,
        images=data.images,
        contact=data.contact
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    
    return success(
        data=UserFeedbackSchema.model_validate(feedback).model_dump(),
        message="反馈提交成功，感谢您的建议"
    )


@feedback_router.get("/list")
async def get_feedback_list(
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取我的反馈列表"""
    offset = (page - 1) * page_size
    
    result = await db.execute(
        select(UserFeedback)
        .where(UserFeedback.user_id == current_user.id)
        .order_by(UserFeedback.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    feedbacks = result.scalars().all()
    
    return success(data={
        "list": [UserFeedbackSchema.model_validate(f).model_dump() for f in feedbacks],
        "page": page,
        "page_size": page_size
    })


