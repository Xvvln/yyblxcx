"""
食物库接口
GET /food-library/search - 搜索食物
GET /food-library/categories - 食物分类
GET /food-library/{id} - 食物详情
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from typing import Optional

from app.database import get_db
from app.models.food import FoodLibrary
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/food-library", tags=["食物库"])


@router.get("/search")
async def search_food(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    category: Optional[str] = Query(None, description="分类筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """搜索食物库"""
    conditions = []
    
    if keyword:
        conditions.append(FoodLibrary.name.contains(keyword))
    
    if category:
        conditions.append(FoodLibrary.category == category)
    
    # 查询总数
    count_query = select(func.count()).select_from(FoodLibrary)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(FoodLibrary)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(FoodLibrary.name).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    foods = result.scalars().all()
    
    items = []
    for f in foods:
        items.append({
            "id": f.id,
            "name": f.name,
            "category": f.category,
            "image": f.image,
            "calories": f.calories,
            "protein": float(f.protein),
            "carbs": float(f.carbs),
            "fat": float(f.fat),
            "fiber": float(f.fiber),
            "serving_size": f.serving_size,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取食物分类列表"""
    result = await db.execute(
        select(distinct(FoodLibrary.category)).where(FoodLibrary.category.isnot(None))
    )
    categories = [row[0] for row in result.all() if row[0]]
    
    return success(data=categories)


@router.get("/{food_id}")
async def get_food_detail(
    food_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取食物详情"""
    result = await db.execute(
        select(FoodLibrary).where(FoodLibrary.id == food_id)
    )
    food = result.scalar_one_or_none()
    
    if not food:
        return error(404, "食物不存在")
    
    return success(data={
        "id": food.id,
        "name": food.name,
        "category": food.category,
        "image": food.image,
        "calories": food.calories,
        "protein": float(food.protein),
        "carbs": float(food.carbs),
        "fat": float(food.fat),
        "fiber": float(food.fiber),
        "serving_size": food.serving_size,
    })























