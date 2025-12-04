"""
用户相关模型
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, Date, Text, Numeric, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    openid: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="微信openid")
    union_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="微信union_id")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像URL")
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True, comment="手机号")
    gender: Mapped[int] = mapped_column(Integer, default=0, comment="性别: 0未知 1男 2女")
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="生日")
    height: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="身高(cm)")
    weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="体重(kg)")
    
    # 会员相关
    member_level: Mapped[int] = mapped_column(Integer, default=0, index=True, comment="会员等级: 0普通 1月卡 2年卡 3终身")
    member_expire_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="会员过期时间")
    
    # 积分相关
    sport_coins: Mapped[int] = mapped_column(Integer, default=0, comment="运动币")
    food_coins: Mapped[int] = mapped_column(Integer, default=0, comment="膳食币")
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), comment="余额")
    user_level: Mapped[int] = mapped_column(Integer, default=1, comment="用户等级 LV1-LV10")
    
    # 社交相关
    follower_count: Mapped[int] = mapped_column(Integer, default=0, comment="粉丝数")
    following_count: Mapped[int] = mapped_column(Integer, default=0, comment="关注数")
    
    # 打卡相关
    continuous_checkin_days: Mapped[int] = mapped_column(Integer, default=0, comment="连续打卡天数")
    total_checkin_days: Mapped[int] = mapped_column(Integer, default=0, comment="累计签到天数")
    last_checkin_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="最后打卡日期")
    
    # 状态
    status: Mapped[int] = mapped_column(Integer, default=1, comment="状态: 0禁用 1正常")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    health_profile: Mapped[Optional["UserHealthProfile"]] = relationship(
        "UserHealthProfile", back_populates="user", uselist=False
    )
    addresses: Mapped[list["UserAddress"]] = relationship("UserAddress", back_populates="user")


class UserHealthProfile(Base):
    """用户健康档案表"""
    __tablename__ = "user_health_profiles"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False, comment="用户ID")
    
    # 健康目标
    health_goal: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="健康目标")
    target_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment="目标体重")
    
    # 运动偏好
    preferred_sports: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="喜好运动")
    daily_exercise_minutes: Mapped[int] = mapped_column(Integer, default=30, comment="每日运动目标(分钟)")
    
    # 身体状况
    has_injury: Mapped[int] = mapped_column(Integer, default=0, comment="是否有伤病")
    injury_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="伤病描述")
    chronic_diseases: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="慢性病")
    
    # 体能测试
    pushup_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="俯卧撑个数")
    squat_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="深蹲个数")
    crunch_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="仰卧起坐个数")
    climb_stairs_tired: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="爬楼是否气喘")
    
    # 饮食习惯
    diet_habit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="饮食习惯")
    allergies: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="过敏食物")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    user: Mapped["User"] = relationship("User", back_populates="health_profile")


class UserSettings(Base):
    """用户设置表"""
    __tablename__ = "user_settings"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False, comment="用户ID")
    
    # 隐私设置
    share_health_data: Mapped[int] = mapped_column(Integer, default=0, comment="向医生展示健康数据: 0否 1是")
    public_profile: Mapped[int] = mapped_column(Integer, default=1, comment="允许陌生人查看动态: 0否 1是")
    personalized: Mapped[int] = mapped_column(Integer, default=1, comment="个性化推荐: 0否 1是")
    
    # 通用设置
    elderly_mode: Mapped[int] = mapped_column(Integer, default=0, comment="长辈模式: 0否 1是")
    notification_enabled: Mapped[int] = mapped_column(Integer, default=1, comment="消息通知: 0否 1是")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class UserFeedback(Base):
    """用户反馈表"""
    __tablename__ = "user_feedbacks"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="反馈内容")
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment="反馈图片")
    contact: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="联系方式")
    status: Mapped[int] = mapped_column(Integer, default=0, comment="状态: 0待处理 1已处理 2已回复")
    reply: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="回复内容")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class UserAddress(Base):
    """用户收货地址表"""
    __tablename__ = "user_addresses"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    receiver_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="收货人姓名")
    receiver_phone: Mapped[str] = mapped_column(String(20), nullable=False, comment="收货人电话")
    province: Mapped[str] = mapped_column(String(50), nullable=False, comment="省")
    city: Mapped[str] = mapped_column(String(50), nullable=False, comment="市")
    district: Mapped[str] = mapped_column(String(50), nullable=False, comment="区")
    detail: Mapped[str] = mapped_column(String(200), nullable=False, comment="详细地址")
    is_default: Mapped[int] = mapped_column(Integer, default=0, comment="是否默认: 0否 1是")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    user: Mapped["User"] = relationship("User", back_populates="addresses")


