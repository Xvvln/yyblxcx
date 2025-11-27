"""
管理员认证接口
POST /auth/login - 管理员登录
POST /auth/logout - 退出登录
GET /auth/info - 获取当前管理员信息
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.models.system import Admin, AdminLog
from app.utils.security import verify_password, create_access_token, get_current_admin
from app.utils.response import success, error

router = APIRouter(prefix="/auth", tags=["管理员认证"])


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=1, description="密码")


class LoginResponse(BaseModel):
    """登录响应"""
    token: str
    admin_id: int
    username: str
    role: str


@router.post("/login")
async def login(
    data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """管理员登录"""
    # 查询管理员
    result = await db.execute(
        select(Admin).where(Admin.username == data.username)
    )
    admin = result.scalar_one_or_none()
    
    if not admin:
        return error(401, "用户名或密码错误")
    
    # 验证密码
    if not verify_password(data.password, admin.password):
        return error(401, "用户名或密码错误")
    
    # 检查状态
    if admin.status != 1:
        return error(403, "账号已被禁用")
    
    # 生成token
    token = create_access_token({"sub": str(admin.id), "type": "admin"})
    
    # 更新最后登录时间
    admin.last_login_time = datetime.now()
    
    # 记录登录日志
    log = AdminLog(
        admin_id=admin.id,
        action="login",
        target_type="admin",
        target_id=admin.id,
        content="管理员登录",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    await db.commit()
    
    return success(data={
        "token": token,
        "admin_id": admin.id,
        "username": admin.username,
        "role": admin.role,
        "nickname": admin.nickname,
        "avatar": admin.avatar,
    })


@router.post("/logout")
async def logout(
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """退出登录"""
    # 记录登出日志
    log = AdminLog(
        admin_id=admin.id,
        action="logout",
        target_type="admin",
        target_id=admin.id,
        content="管理员退出登录",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    await db.commit()
    
    return success(message="退出成功")


@router.get("/info")
async def get_info(admin: Admin = Depends(get_current_admin)):
    """获取当前管理员信息"""
    return success(data={
        "id": admin.id,
        "username": admin.username,
        "nickname": admin.nickname,
        "avatar": admin.avatar,
        "role": admin.role,
        "last_login_time": admin.last_login_time.strftime("%Y-%m-%d %H:%M:%S") if admin.last_login_time else None,
    })


