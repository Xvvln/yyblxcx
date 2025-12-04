"""
初始化管理员账号脚本
运行方式: python init_admin.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

from app.config import settings
from app.models.system import Admin
from app.utils.security import get_password_hash
from app.database import Base


async def init_admin():
    """初始化默认管理员账号"""
    # 创建数据库引擎
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 创建会话
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 检查是否已存在管理员
        result = await session.execute(select(Admin).where(Admin.username == "admin"))
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("管理员账号已存在!")
            print(f"  用户名: admin")
            print(f"  密码: admin123")
        else:
            # 创建默认管理员
            admin = Admin(
                username="admin",
                password=get_password_hash("admin123"),
                nickname="超级管理员",
                role="super_admin",
                status=1
            )
            session.add(admin)
            await session.commit()
            print("=" * 50)
            print("默认管理员账号创建成功!")
            print("=" * 50)
            print(f"  用户名: admin")
            print(f"  密码: admin123")
            print("=" * 50)
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_admin())



















