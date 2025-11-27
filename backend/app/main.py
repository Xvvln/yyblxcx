"""
FastAPI 应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from pathlib import Path

from app.config import settings
from app.database import close_db

# 确保上传目录存在（在应用启动前创建）
UPLOAD_PATH = Path(__file__).parent.parent / settings.UPLOAD_DIR
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
(UPLOAD_PATH / "avatars").mkdir(exist_ok=True)
(UPLOAD_PATH / "images").mkdir(exist_ok=True)
(UPLOAD_PATH / "posts").mkdir(exist_ok=True)
from app.api.v1 import (
    auth,
    user,
    health,
    sport,
    food,
    course,
    shop,
    cart,
    order,
    coupon,
    community,
    message,
    points,
    task,
    member,
    reminder,
    address,
    doctor,
    upload,
    ai,
    notification,
    banner,
    checkin,
    food_library,
    sport_goal,
    stats,
)
from app.api.admin import (
    auth as admin_auth,
    user as admin_user,
    audit as admin_audit,
    product as admin_product,
    order as admin_order,
    stats as admin_stats,
    setting as admin_setting,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时（目录已在模块加载时创建）
    yield
    
    # 关闭时
    await close_db()


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="营养不良筛查与健康管理小程序后端API",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

# 注册路由 - 小程序端 API
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(user.router, prefix="/api/v1", tags=["用户"])
app.include_router(health.router, prefix="/api/v1", tags=["健康筛查"])
app.include_router(sport.router, prefix="/api/v1", tags=["运动"])
app.include_router(food.router, prefix="/api/v1", tags=["饮食"])
app.include_router(course.router, prefix="/api/v1", tags=["课程"])
app.include_router(shop.router, prefix="/api/v1", tags=["商城"])
app.include_router(cart.router, prefix="/api/v1", tags=["购物车"])
app.include_router(order.router, prefix="/api/v1", tags=["订单"])
app.include_router(coupon.router, prefix="/api/v1", tags=["优惠券"])
app.include_router(community.router, prefix="/api/v1", tags=["社区"])
app.include_router(message.router, prefix="/api/v1", tags=["私聊"])
app.include_router(points.router, prefix="/api/v1", tags=["积分"])
app.include_router(task.router, prefix="/api/v1", tags=["任务"])
app.include_router(member.router, prefix="/api/v1", tags=["会员"])
app.include_router(reminder.router, prefix="/api/v1", tags=["提醒"])
app.include_router(address.router, prefix="/api/v1", tags=["地址"])
app.include_router(doctor.router, prefix="/api/v1", tags=["远程医疗"])
app.include_router(upload.router, prefix="/api/v1", tags=["上传"])
app.include_router(ai.router, prefix="/api/v1", tags=["AI助手"])
app.include_router(notification.router, prefix="/api/v1", tags=["通知"])
app.include_router(banner.router, prefix="/api/v1", tags=["轮播图"])
app.include_router(checkin.router, prefix="/api/v1", tags=["签到"])
app.include_router(food_library.router, prefix="/api/v1", tags=["食物库"])
app.include_router(sport_goal.router, prefix="/api/v1", tags=["运动目标"])
app.include_router(stats.router, prefix="/api/v1", tags=["数据统计"])

# 注册路由 - Web管理端 API
app.include_router(admin_auth.router, prefix="/api/admin/v1", tags=["管理员认证"])
app.include_router(admin_user.router, prefix="/api/admin/v1", tags=["用户管理"])
app.include_router(admin_audit.router, prefix="/api/admin/v1", tags=["内容审核"])
app.include_router(admin_product.router, prefix="/api/admin/v1", tags=["商品管理"])
app.include_router(admin_order.router, prefix="/api/admin/v1", tags=["订单管理"])
app.include_router(admin_stats.router, prefix="/api/admin/v1", tags=["数据统计"])
app.include_router(admin_setting.router, prefix="/api/admin/v1", tags=["系统设置"])


@app.get("/")
async def root():
    """根路由"""
    return {
        "code": 200,
        "message": "欢迎使用营养不良筛查与健康管理API",
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

