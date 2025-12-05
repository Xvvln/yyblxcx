"""
系统设置接口
GET /setting/points - 积分规则配置
PUT /setting/points - 更新积分规则
GET /setting/member - 会员配置
PUT /setting/member - 更新会员配置
GET /setting/system - 系统配置列表
PUT /setting/system - 更新系统配置
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.system import SystemConfig, Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error

router = APIRouter(prefix="/setting", tags=["系统设置"])


class PointsConfig(BaseModel):
    """积分规则配置"""
    checkin_base_coin: int = Field(10, ge=0, description="每日签到基础积分")
    checkin_continuous_bonus: int = Field(5, ge=0, description="连续签到额外奖励")
    sport_record_coin: int = Field(5, ge=0, description="记录运动获得积分")
    food_record_coin: int = Field(5, ge=0, description="记录饮食获得积分")
    share_post_coin: int = Field(10, ge=0, description="分享帖子获得积分")
    invite_reward_coin: int = Field(50, ge=0, description="邀请好友奖励积分")


class MemberConfig(BaseModel):
    """会员配置"""
    member_month_price: float = Field(29, gt=0, description="月卡会员价格")
    member_year_price: float = Field(198, gt=0, description="年卡会员价格")
    member_lifetime_price: float = Field(998, gt=0, description="终身会员价格")
    member_discount: float = Field(0.8, gt=0, le=1, description="会员折扣")


class SystemConfigUpdate(BaseModel):
    """系统配置更新"""
    configs: Dict[str, str] = Field(..., description="配置项键值对")


async def get_config_value(db: AsyncSession, key: str, default: str = "") -> str:
    """获取配置值"""
    result = await db.execute(
        select(SystemConfig).where(SystemConfig.config_key == key)
    )
    config = result.scalar_one_or_none()
    return config.config_value if config else default


async def set_config_value(db: AsyncSession, key: str, value: str, description: str = None):
    """设置配置值"""
    result = await db.execute(
        select(SystemConfig).where(SystemConfig.config_key == key)
    )
    config = result.scalar_one_or_none()
    
    if config:
        config.config_value = value
        if description:
            config.description = description
    else:
        config = SystemConfig(
            config_key=key,
            config_value=value,
            description=description,
        )
        db.add(config)


@router.get("/points")
async def get_points_config(
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取积分规则配置"""
    return success(data={
        "checkin_base_coin": int(await get_config_value(db, "checkin_base_coin", "10")),
        "checkin_continuous_bonus": int(await get_config_value(db, "checkin_continuous_bonus", "5")),
        "sport_record_coin": int(await get_config_value(db, "sport_record_coin", "5")),
        "food_record_coin": int(await get_config_value(db, "food_record_coin", "5")),
        "share_post_coin": int(await get_config_value(db, "share_post_coin", "10")),
        "invite_reward_coin": int(await get_config_value(db, "invite_reward_coin", "50")),
    })


@router.put("/points")
async def update_points_config(
    data: PointsConfig,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """更新积分规则配置"""
    await set_config_value(db, "checkin_base_coin", str(data.checkin_base_coin), "每日签到基础积分")
    await set_config_value(db, "checkin_continuous_bonus", str(data.checkin_continuous_bonus), "连续签到额外奖励")
    await set_config_value(db, "sport_record_coin", str(data.sport_record_coin), "记录运动获得积分")
    await set_config_value(db, "food_record_coin", str(data.food_record_coin), "记录饮食获得积分")
    await set_config_value(db, "share_post_coin", str(data.share_post_coin), "分享帖子获得积分")
    await set_config_value(db, "invite_reward_coin", str(data.invite_reward_coin), "邀请好友奖励积分")
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="update",
        target_type="system_config",
        target_id=None,
        content="更新积分规则配置",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="更新成功")


@router.get("/member")
async def get_member_config(
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取会员配置"""
    return success(data={
        "member_month_price": float(await get_config_value(db, "member_month_price", "29")),
        "member_year_price": float(await get_config_value(db, "member_year_price", "198")),
        "member_lifetime_price": float(await get_config_value(db, "member_lifetime_price", "998")),
        "member_discount": float(await get_config_value(db, "member_discount", "0.8")),
    })


@router.put("/member")
async def update_member_config(
    data: MemberConfig,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """更新会员配置"""
    await set_config_value(db, "member_month_price", str(data.member_month_price), "月卡会员价格")
    await set_config_value(db, "member_year_price", str(data.member_year_price), "年卡会员价格")
    await set_config_value(db, "member_lifetime_price", str(data.member_lifetime_price), "终身会员价格")
    await set_config_value(db, "member_discount", str(data.member_discount), "会员折扣")
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="update",
        target_type="system_config",
        target_id=None,
        content="更新会员配置",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="更新成功")


@router.get("/system")
async def get_system_configs(
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取系统配置列表"""
    result = await db.execute(
        select(SystemConfig).order_by(SystemConfig.config_key)
    )
    configs = result.scalars().all()
    
    items = []
    for c in configs:
        items.append({
            "id": c.id,
            "config_key": c.config_key,
            "config_value": c.config_value,
            "description": c.description,
            "updated_at": c.updated_at.strftime("%Y-%m-%d %H:%M:%S") if c.updated_at else None,
        })
    
    return success(data=items)


@router.put("/system")
async def update_system_configs(
    data: SystemConfigUpdate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """批量更新系统配置"""
    for key, value in data.configs.items():
        await set_config_value(db, key, value)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="update",
        target_type="system_config",
        target_id=None,
        content=f"批量更新系统配置: {list(data.configs.keys())}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="更新成功")
























