"""
认证接口
POST /auth/login - 微信登录
POST /auth/register - 完善用户信息
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.utils.security import create_access_token, get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    微信登录
    
    通过微信登录code获取openid，创建或获取用户，返回JWT Token
    """
    openid = None
    
    # 如果配置了微信小程序，则调用微信接口获取openid
    if settings.WECHAT_APPID and settings.WECHAT_SECRET:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.weixin.qq.com/sns/jscode2session",
                    params={
                        "appid": settings.WECHAT_APPID,
                        "secret": settings.WECHAT_SECRET,
                        "js_code": request.code,
                        "grant_type": "authorization_code"
                    }
                )
                result = response.json()
                if "openid" in result:
                    openid = result["openid"]
                else:
                    return error(400, f"微信登录失败: {result.get('errmsg', '未知错误')}")
        except Exception as e:
            return error(500, f"微信接口调用失败: {str(e)}")
    else:
        # 开发模式：使用code作为openid
        openid = f"dev_{request.code}"
    
    # 查询或创建用户
    result = await db.execute(select(User).where(User.openid == openid))
    user = result.scalar_one_or_none()
    
    is_new_user = False
    if not user:
        # 创建新用户
        user = User(openid=openid)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        is_new_user = True
    
    # 生成 JWT Token (sub 必须是字符串)
    token = create_access_token(data={"sub": str(user.id)})
    
    return success(
        data=LoginResponse(
            token=token,
            user_id=user.id,
            is_new_user=is_new_user
        ).model_dump(),
        message="登录成功"
    )


@router.post("/register")
async def register(
    request: RegisterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    完善用户信息
    
    首次登录后完善昵称、头像等基本信息
    """
    # 更新用户信息
    if request.nickname is not None:
        current_user.nickname = request.nickname
    if request.avatar is not None:
        current_user.avatar = request.avatar
    if request.gender is not None:
        current_user.gender = request.gender
    if request.phone is not None:
        current_user.phone = request.phone
    
    await db.commit()
    await db.refresh(current_user)
    
    return success(message="信息完善成功")


