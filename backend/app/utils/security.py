"""
安全工具模块 - JWT认证、密码加密
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.database import get_db


# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer Token 认证
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Token
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        JWT Token 字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    解码 JWT Token
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        解码后的数据字典，失败返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前登录用户依赖
    
    通过 JWT Token 验证并获取当前用户信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": 401, "message": "未登录或Token已失效", "data": None},
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    user_id = int(user_id_str)
    
    # 查询用户
    from app.models.user import User
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "账号已被禁用", "data": None}
        )
    
    return user


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    可选的当前用户依赖
    
    如果提供了有效 Token 则返回用户，否则返回 None
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        return None
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None
    user_id = int(user_id_str)
    
    # 查询用户
    from app.models.user import User
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    return user


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前登录管理员依赖
    
    通过 JWT Token 验证并获取当前管理员信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": 401, "message": "未登录或Token已失效", "data": None},
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # 检查是否为管理员Token
    token_type = payload.get("type")
    if token_type != "admin":
        raise credentials_exception
    
    admin_id_str = payload.get("sub")
    if admin_id_str is None:
        raise credentials_exception
    admin_id = int(admin_id_str)
    
    # 查询管理员
    from app.models.system import Admin
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    admin = result.scalar_one_or_none()
    
    if admin is None:
        raise credentials_exception
    
    if admin.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": 403, "message": "账号已被禁用", "data": None}
        )
    
    return admin

