"""
用户相关 Schema
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """用户信息"""
    id: int
    openid: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    gender: int = 0
    birthday: Optional[date] = None
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    member_level: int = 0
    member_expire_time: Optional[datetime] = None
    sport_coins: int = 0
    food_coins: int = 0
    balance: Decimal = Decimal("0.00")
    user_level: int = 1
    follower_count: int = 0
    following_count: int = 0
    continuous_checkin_days: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """更新用户信息"""
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    height: Optional[Decimal] = Field(None, ge=0, le=300, description="身高(cm)")
    weight: Optional[Decimal] = Field(None, ge=0, le=500, description="体重(kg)")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserHealthProfileSchema(BaseModel):
    """用户健康档案"""
    id: int
    user_id: int
    health_goal: Optional[str] = None
    target_weight: Optional[Decimal] = None
    preferred_sports: Optional[list] = None
    daily_exercise_minutes: int = 30
    has_injury: int = 0
    injury_description: Optional[str] = None
    chronic_diseases: Optional[list] = None
    pushup_count: Optional[int] = None
    squat_count: Optional[int] = None
    crunch_count: Optional[int] = None
    climb_stairs_tired: Optional[int] = None
    diet_habit: Optional[str] = None
    allergies: Optional[list] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserHealthProfileUpdate(BaseModel):
    """更新健康档案"""
    health_goal: Optional[str] = Field(None, max_length=50, description="健康目标")
    target_weight: Optional[Decimal] = Field(None, description="目标体重")
    preferred_sports: Optional[list] = Field(None, description="喜好运动")
    daily_exercise_minutes: Optional[int] = Field(None, ge=0, description="每日运动目标")
    has_injury: Optional[int] = Field(None, ge=0, le=1, description="是否有伤病")
    injury_description: Optional[str] = Field(None, description="伤病描述")
    chronic_diseases: Optional[list] = Field(None, description="慢性病")
    pushup_count: Optional[int] = Field(None, ge=0, description="俯卧撑个数")
    squat_count: Optional[int] = Field(None, ge=0, description="深蹲个数")
    crunch_count: Optional[int] = Field(None, ge=0, description="仰卧起坐个数")
    climb_stairs_tired: Optional[int] = Field(None, ge=0, le=1, description="爬楼是否气喘")
    diet_habit: Optional[str] = Field(None, max_length=50, description="饮食习惯")
    allergies: Optional[list] = Field(None, description="过敏食物")


class UserAddressSchema(BaseModel):
    """地址信息"""
    id: int
    user_id: int
    receiver_name: str
    receiver_phone: str
    province: str
    city: str
    district: str
    detail: str
    is_default: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserAddressCreate(BaseModel):
    """创建地址"""
    receiver_name: str = Field(..., max_length=50, description="收货人")
    receiver_phone: str = Field(..., max_length=20, description="手机号")
    province: str = Field(..., max_length=50, description="省")
    city: str = Field(..., max_length=50, description="市")
    district: str = Field(..., max_length=50, description="区")
    detail: str = Field(..., max_length=200, description="详细地址")
    is_default: int = Field(default=0, ge=0, le=1, description="是否默认")


class UserAddressUpdate(BaseModel):
    """更新地址"""
    receiver_name: Optional[str] = Field(None, max_length=50, description="收货人")
    receiver_phone: Optional[str] = Field(None, max_length=20, description="手机号")
    province: Optional[str] = Field(None, max_length=50, description="省")
    city: Optional[str] = Field(None, max_length=50, description="市")
    district: Optional[str] = Field(None, max_length=50, description="区")
    detail: Optional[str] = Field(None, max_length=200, description="详细地址")
    is_default: Optional[int] = Field(None, ge=0, le=1, description="是否默认")















