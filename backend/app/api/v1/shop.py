"""
商城接口
GET /shop/products - 商品列表
GET /shop/product/{id} - 商品详情
GET /shop/categories - 商品分类
GET /shop/product/{id}/reviews - 商品评价列表
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.shop import Product, ProductCategory, ProductReview, ProductCollect
from app.utils.security import get_current_user_optional, get_current_user
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/shop", tags=["商城"])


@router.get("/products")
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category_id: Optional[int] = Query(None, description="分类ID"),
    is_recommend: Optional[int] = Query(None, description="是否推荐"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    sort: str = Query("default", description="排序: default/sales/price_asc/price_desc"),
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取商品列表"""
    # 构建查询条件
    conditions = [Product.is_on_sale == 1]
    if category_id:
        conditions.append(Product.category_id == category_id)
    if is_recommend is not None:
        conditions.append(Product.is_recommend == is_recommend)
    if keyword:
        conditions.append(Product.name.contains(keyword))
    
    # 查询总数
    count_query = select(func.count()).select_from(Product).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 排序
    order_by = []
    if sort == "sales":
        order_by.append(desc(Product.sales_count))
    elif sort == "price_asc":
        order_by.append(Product.current_price)
    elif sort == "price_desc":
        order_by.append(desc(Product.current_price))
    else:
        order_by.append(desc(Product.is_recommend))
        order_by.append(desc(Product.sort_order))
    order_by.append(desc(Product.id))
    
    # 查询列表
    query = select(Product).where(*conditions).order_by(
        *order_by
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    # 检查是否会员
    is_member = current_user and current_user.member_level > 0 if current_user else False
    
    items = []
    for p in products:
        images = p.images if p.images else []
        items.append({
            "id": p.id,
            "name": p.name,
            "subtitle": p.subtitle,
            "image": images[0] if images else None,
            "original_price": float(p.original_price),
            "current_price": float(p.current_price),
            "member_price": float(p.member_price) if p.member_price else None,
            "show_price": float(p.member_price) if is_member and p.member_price else float(p.current_price),
            "stock": p.stock,
            "sales_count": p.sales_count,
            "health_tags": p.health_tags,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/product/{product_id}")
async def get_product_detail(
    product_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取商品详情"""
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_on_sale == 1)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        return error(404, "商品不存在")
    
    # 检查是否会员
    is_member = current_user and current_user.member_level > 0 if current_user else False
    
    # 获取评价统计
    review_count = (await db.execute(
        select(func.count()).select_from(ProductReview).where(
            ProductReview.product_id == product_id,
            ProductReview.status == 1
        )
    )).scalar()
    
    avg_rating = (await db.execute(
        select(func.avg(ProductReview.rating)).where(
            ProductReview.product_id == product_id,
            ProductReview.status == 1
        )
    )).scalar()
    
    data = {
        "id": product.id,
        "name": product.name,
        "subtitle": product.subtitle,
        "images": product.images or [],
        "description": product.description,
        "original_price": float(product.original_price),
        "current_price": float(product.current_price),
        "member_price": float(product.member_price) if product.member_price else None,
        "show_price": float(product.member_price) if is_member and product.member_price else float(product.current_price),
        "stock": product.stock,
        "sales_count": product.sales_count,
        "suitable_tags": product.suitable_tags,
        "health_tags": product.health_tags,
        "specs": product.specs,
        "review_count": review_count,
        "avg_rating": round(float(avg_rating), 1) if avg_rating else 5.0,
    }
    
    return success(data=data)


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """获取商品分类"""
    result = await db.execute(
        select(ProductCategory).where(
            ProductCategory.is_active == 1
        ).order_by(ProductCategory.sort_order, ProductCategory.id)
    )
    categories = result.scalars().all()
    
    items = []
    for c in categories:
        items.append({
            "id": c.id,
            "name": c.name,
            "parent_id": c.parent_id,
            "icon": c.icon,
        })
    
    return success(data=items)


@router.get("/product/{product_id}/reviews")
async def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """获取商品评价列表"""
    # 查询总数
    count_query = select(func.count()).select_from(ProductReview).where(
        ProductReview.product_id == product_id,
        ProductReview.status == 1
    )
    total = (await db.execute(count_query)).scalar()
    
    # 查询评价列表
    query = select(ProductReview).where(
        ProductReview.product_id == product_id,
        ProductReview.status == 1
    ).order_by(desc(ProductReview.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    reviews = result.scalars().all()
    
    # 获取用户信息
    from app.models.user import User
    user_ids = [r.user_id for r in reviews]
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    else:
        users = {}
    
    items = []
    for r in reviews:
        user = users.get(r.user_id)
        items.append({
            "id": r.id,
            "rating": r.rating,
            "content": r.content,
            "images": r.images,
            "user": {
                "id": user.id if user else None,
                "nickname": "匿名用户" if r.is_anonymous else (user.nickname if user else "未知"),
                "avatar": None if r.is_anonymous else (user.avatar if user else None),
            },
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/product/{product_id}/collect")
async def collect_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """收藏商品"""
    # 检查商品是否存在
    product_result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = product_result.scalar_one_or_none()
    
    if not product:
        return error(404, "商品不存在")
    
    # 检查是否已收藏
    collect_result = await db.execute(
        select(ProductCollect).where(
            ProductCollect.user_id == current_user.id,
            ProductCollect.product_id == product_id
        )
    )
    existing = collect_result.scalar_one_or_none()
    
    if existing:
        return error(400, "已收藏该商品")
    
    # 添加收藏
    collect = ProductCollect(
        user_id=current_user.id,
        product_id=product_id
    )
    db.add(collect)
    await db.commit()
    
    return success(message="收藏成功")


@router.delete("/product/{product_id}/collect")
async def uncollect_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏商品"""
    collect_result = await db.execute(
        select(ProductCollect).where(
            ProductCollect.user_id == current_user.id,
            ProductCollect.product_id == product_id
        )
    )
    collect = collect_result.scalar_one_or_none()
    
    if not collect:
        return error(404, "未收藏该商品")
    
    await db.delete(collect)
    await db.commit()
    
    return success(message="取消收藏成功")


@router.get("/my-collects")
async def get_my_collects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取我的收藏列表"""
    # 查询总数
    count_query = select(func.count()).select_from(ProductCollect).where(
        ProductCollect.user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar()
    
    # 查询收藏列表
    query = select(ProductCollect).where(
        ProductCollect.user_id == current_user.id
    ).order_by(desc(ProductCollect.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    collects = result.scalars().all()
    
    # 获取商品信息
    product_ids = [c.product_id for c in collects]
    if product_ids:
        products_result = await db.execute(select(Product).where(Product.id.in_(product_ids)))
        products = {p.id: p for p in products_result.scalars().all()}
    else:
        products = {}
    
    # 检查是否会员
    is_member = current_user.member_level > 0
    
    items = []
    for c in collects:
        product = products.get(c.product_id)
        if not product:
            continue
        
        images = product.images if product.images else []
        items.append({
            "id": c.id,
            "product_id": c.product_id,
            "product": {
                "id": product.id,
                "name": product.name,
                "image": images[0] if images else None,
                "original_price": float(product.original_price),
                "current_price": float(product.current_price),
                "member_price": float(product.member_price) if product.member_price else None,
                "show_price": float(product.member_price) if is_member and product.member_price else float(product.current_price),
                "is_on_sale": product.is_on_sale,
            },
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


