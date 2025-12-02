"""
认证接口
POST /auth/login - 微信登录
POST /auth/dev-login - 开发环境登录（无需微信）
GET /auth/check - 检查登录状态
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.security import create_access_token, get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login")
async def wechat_login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    微信登录
    
    流程：
    1. 使用code换取openid
    2. 查询或创建用户
    3. 返回JWT Token
    """
    # 如果没有配置微信APPID，使用开发模式
    if not settings.WECHAT_APPID or not settings.WECHAT_SECRET:
        return error(400, "微信登录未配置，请使用开发登录接口 /auth/dev-login")
    
    # 调用微信API获取openid
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "js_code": data.code,
        "grant_type": "authorization_code"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            result = response.json()
    except Exception as e:
        return error(500, f"微信API调用失败: {str(e)}")
    
    if "errcode" in result and result["errcode"] != 0:
        return error(400, f"微信登录失败: {result.get('errmsg', '未知错误')}")
    
    openid = result.get("openid")
    if not openid:
        return error(400, "获取openid失败")
    
    # 查询或创建用户
    query = select(User).where(User.openid == openid)
    db_result = await db.execute(query)
    user = db_result.scalar_one_or_none()
    
    is_new_user = False
    if not user:
        # 创建新用户
        user = User(
            openid=openid,
            union_id=result.get("unionid"),
            nickname=f"用户{openid[-6:]}",
            created_at=datetime.now()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        is_new_user = True
    
    # 生成JWT Token
    token = create_access_token({"sub": str(user.id), "type": "user"})
    
    return success(data={
        "token": token,
        "user_id": user.id,
        "is_new_user": is_new_user,
        "nickname": user.nickname,
        "avatar": user.avatar,
    })


@router.post("/dev-login")
async def dev_login(
    openid: str = "dev_user_001",
    db: AsyncSession = Depends(get_db)
):
    """
    开发环境登录（无需微信code）
    
    用于开发测试，直接使用openid登录
    """
    # 查询或创建用户
    query = select(User).where(User.openid == openid)
    db_result = await db.execute(query)
    user = db_result.scalar_one_or_none()
    
    is_new_user = False
    if not user:
        # 创建新用户
        user = User(
            openid=openid,
            nickname=f"测试用户{openid[-4:]}",
            created_at=datetime.now()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        is_new_user = True
    
    # 生成JWT Token
    token = create_access_token({"sub": str(user.id), "type": "user"})
    
    return success(data={
        "token": token,
        "user_id": user.id,
        "is_new_user": is_new_user,
        "nickname": user.nickname,
        "avatar": user.avatar,
    })


@router.get("/check")
async def check_login(current_user: User = Depends(get_current_user)):
    """检查登录状态"""
    return success(data={
        "user_id": current_user.id,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar,
        "member_level": current_user.member_level,
    })


@router.put("/register")
async def complete_register(
    data: RegisterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """完善用户信息"""
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return success(
        data={
            "user_id": current_user.id,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "phone": current_user.phone,
            "gender": current_user.gender,
        },
        message="信息更新成功"
    )
