"""
轮播图接口
GET /banner/list - 获取轮播图列表
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.system import Banner
from app.utils.response import success

router = APIRouter(prefix="/banner", tags=["轮播图"])


@router.get("/list")
async def get_banners(
    position: Optional[str] = Query("home", description="位置: home/shop/community"),
    db: AsyncSession = Depends(get_db)
):
    """获取轮播图列表"""
    now = datetime.now()
    
    # 查询条件：启用、位置匹配、在有效期内
    conditions = [
        Banner.is_active == 1,
        Banner.position == position,
    ]
    
    query = select(Banner).where(*conditions).order_by(
        Banner.sort_order.desc(),
        Banner.id.desc()
    )
    
    result = await db.execute(query)
    banners = result.scalars().all()
    
    items = []
    for b in banners:
        # 检查有效期
        if b.start_time and b.start_time > now:
            continue
        if b.end_time and b.end_time < now:
            continue
            
        items.append({
            "id": b.id,
            "title": b.title,
            "image_url": b.image_url,
            "link_type": b.link_type,
            "link_value": b.link_value,
        })
    
    return success(data=items)














