"""
应用配置模块
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "营养不良筛查与健康管理API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://root:1234@localhost:3306/health_db"
    
    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7天
    
    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    
    # 百炼平台 AI 配置
    DASHSCOPE_API_KEY: str = ""
    DASHSCOPE_MODEL: str = "qwen-turbo"
    
    # 微信支付配置（暂缓实现）
    WECHAT_MCH_ID: str = ""
    WECHAT_API_KEY: str = ""
    
    # 地图服务配置（暂缓实现）
    TENCENT_MAP_KEY: str = ""
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


settings = get_settings()


