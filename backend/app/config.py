"""
配置管理模块

环境变量配置说明:
1. 复制 .env.example 为 .env
2. 修改 .env 中的配置为实际值
3. .env 文件不会被提交到 Git 仓库
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """应用配置
    
    所有敏感配置都从环境变量或 .env 文件读取，确保安全性。
    请在 backend/.env 文件中配置实际值。
    """
    
    # pydantic-settings v2 配置
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # 应用基本信息
    APP_NAME: str = "营养不良筛查与健康管理"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 数据库配置 - 必须在 .env 中配置
    DATABASE_URL: str = "mysql+aiomysql://root:YOUR_PASSWORD@localhost:3306/health_db"
    
    # JWT 配置 - 生产环境必须修改
    JWT_SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    
    # 上传目录
    UPLOAD_DIR: str = "uploads"
    
    # 微信小程序配置 - 必须在 .env 中配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""
    
    # 阿里云百炼 AI 服务配置（可选）
    DASHSCOPE_API_KEY: Optional[str] = None
    DASHSCOPE_MODEL: str = "qwen-turbo"


# 全局配置实例
settings = Settings()
