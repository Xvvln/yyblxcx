"""
通用工具函数
"""
import random
import string
import uuid
from datetime import datetime, date
from typing import Optional
import hashlib


def generate_order_no() -> str:
    """
    生成订单号
    格式: 年月日时分秒 + 6位随机数
    """
    now = datetime.now()
    date_str = now.strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.digits, k=6))
    return f"{date_str}{random_str}"


def generate_uuid() -> str:
    """生成 UUID"""
    return str(uuid.uuid4()).replace("-", "")


def generate_random_string(length: int = 16) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def calculate_bmi(height: float, weight: float) -> Optional[float]:
    """
    计算 BMI
    
    Args:
        height: 身高（厘米）
        weight: 体重（千克）
        
    Returns:
        BMI 值，保留两位小数
    """
    if height <= 0 or weight <= 0:
        return None
    height_m = height / 100  # 转换为米
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def calculate_calories(
    sport_type: str,
    duration: int,
    weight: float = 60
) -> int:
    """
    估算运动消耗卡路里
    
    Args:
        sport_type: 运动类型
        duration: 时长（分钟）
        weight: 体重（千克）
        
    Returns:
        消耗卡路里（大卡）
    """
    # MET 值（代谢当量）参考
    met_values = {
        "running": 9.8,
        "walking": 3.5,
        "cycling": 7.5,
        "swimming": 8.0,
        "yoga": 2.5,
        "hiit": 12.0,
        "strength": 6.0,
        "rope_jumping": 11.0,
        "dancing": 5.0,
        "default": 5.0
    }
    
    met = met_values.get(sport_type, met_values["default"])
    # 卡路里 = MET × 体重(kg) × 时间(小时)
    calories = met * weight * (duration / 60)
    return int(calories)


def calculate_age(birthday: date) -> int:
    """
    计算年龄
    
    Args:
        birthday: 生日
        
    Returns:
        年龄
    """
    today = date.today()
    age = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age


def mask_phone(phone: str) -> str:
    """
    手机号脱敏
    
    Args:
        phone: 手机号
        
    Returns:
        脱敏后的手机号，如 138****1234
    """
    if not phone or len(phone) < 11:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"


def md5(text: str) -> str:
    """计算 MD5"""
    return hashlib.md5(text.encode()).hexdigest()


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return ""


def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_date(d: date) -> str:
    """格式化日期"""
    return d.strftime("%Y-%m-%d")
























