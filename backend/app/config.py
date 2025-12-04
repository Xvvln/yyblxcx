"""
配置管理模块

环境变量配置说明:
1. 复制 .env.example 为 .env
2. 修改 .env 中的配置为实际值
3. .env 文件不会被提交到 Git 仓库
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置
    
    所有敏感配置都从环境变量读取，确保安全性。
    请在 .env 文件中配置实际值。
    """
    
    # 应用基本信息
    APP_NAME: str = "营养不良筛查与健康管理"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置 - 必须在 .env 中配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "mysql+aiomysql://root:password@localhost:3306/health_db"
    )
    
    # JWT 配置 - 生产环境必须修改密钥
    JWT_SECRET_KEY: str = os.getenv(
        "JWT_SECRET_KEY",
        "change-this-secret-key-in-production"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # 上传目录
    UPLOAD_DIR: str = "uploads"
    
    # 微信小程序配置 - 必须在 .env 中配置
    WECHAT_APPID: str = os.getenv("WECHAT_APPID", "")
    WECHAT_SECRET: str = os.getenv("WECHAT_SECRET", "")
    
    # 阿里云百炼 AI 服务配置（可选）
    DASHSCOPE_API_KEY: Optional[str] = os.getenv("DASHSCOPE_API_KEY", None)
    DASHSCOPE_MODEL: str = "qwen-turbo"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # 允许忽略 .env 中的额外字段


# 全局配置实例
settings = Settings()
