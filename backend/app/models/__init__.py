"""
数据库模型模块
"""
from app.models.user import User, UserHealthProfile, UserAddress
from app.models.health import HealthScreening, HealthReminder
from app.models.sport import SportRecord, SportGoal
from app.models.food import FoodRecord, FoodLibrary
from app.models.course import Course, UserCourseCollect
from app.models.shop import ProductCategory, Product, ProductReview
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.coupon import Coupon, UserCoupon
from app.models.community import Post, PostComment, PostLike, Topic, UserFollow
from app.models.message import Conversation, Message
from app.models.points import CoinRecord, CheckinRecord, DailyTask, UserTaskRecord
from app.models.member import MemberOrder
from app.models.system import Admin, AdminLog, Notification, Banner, SystemConfig, File

__all__ = [
    # 用户
    "User", "UserHealthProfile", "UserAddress",
    # 健康
    "HealthScreening", "HealthReminder",
    # 运动
    "SportRecord", "SportGoal",
    # 饮食
    "FoodRecord", "FoodLibrary",
    # 课程
    "Course", "UserCourseCollect",
    # 商城
    "ProductCategory", "Product", "ProductReview",
    # 购物车
    "Cart",
    # 订单
    "Order", "OrderItem",
    # 优惠券
    "Coupon", "UserCoupon",
    # 社区
    "Post", "PostComment", "PostLike", "Topic", "UserFollow",
    # 私信
    "Conversation", "Message",
    # 积分
    "CoinRecord", "CheckinRecord", "DailyTask", "UserTaskRecord",
    # 会员
    "MemberOrder",
    # 系统
    "Admin", "AdminLog", "Notification", "Banner", "SystemConfig", "File",
]
























