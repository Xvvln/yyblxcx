"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用基本信息
    APP_NAME: str = "营养不良筛查与健康管理"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://root:1234@localhost:3306/health_db"
    
    # JWT 配置
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # 上传目录
    UPLOAD_DIR: str = "uploads"
    
    # 微信小程序配置
    WECHAT_APPID: str = "wxeec4f29b9dc7b78b"
    WECHAT_SECRET: str = "9c1a5d9fd4d29b56d601d5d083e39a0d"
    
    # 阿里云百炼 AI 服务配置（可选）
    DASHSCOPE_API_KEY: Optional[str] = None
    DASHSCOPE_MODEL: str = "qwen-turbo"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # 允许忽略 .env 中的额外字段


# 全局配置实例
settings = Settings()
