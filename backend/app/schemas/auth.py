"""
认证相关 Schema
"""
from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """微信登录请求"""
    code: str = Field(..., description="微信登录code")


class LoginResponse(BaseModel):
    """登录响应"""
    token: str = Field(..., description="JWT Token")
    user_id: int = Field(..., description="用户ID")
    is_new_user: bool = Field(default=False, description="是否新用户")


class TokenData(BaseModel):
    """Token数据"""
    sub: int = Field(..., description="用户ID")
    exp: Optional[int] = Field(None, description="过期时间戳")


class RegisterRequest(BaseModel):
    """完善用户信息请求"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别: 0未知 1男 2女")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


