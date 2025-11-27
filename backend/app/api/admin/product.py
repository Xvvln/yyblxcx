"""
商品管理接口
GET /product/list - 商品列表
POST /product - 添加商品
PUT /product/{id} - 编辑商品
DELETE /product/{id} - 删除商品
GET /category/list - 分类列表
POST /category - 添加分类
PUT /category/{id} - 编辑分类
DELETE /category/{id} - 删除分类
"""
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.shop import Product, ProductCategory
from app.models.system import Admin, AdminLog
from app.utils.security import get_current_admin
from app.utils.response import success, error, paginate

router = APIRouter(tags=["商品管理"])


class ProductCreate(BaseModel):
    """创建商品"""
    category_id: int = Field(..., description="分类ID")
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    subtitle: Optional[str] = Field(None, max_length=200, description="副标题")
    images: Optional[List[str]] = Field(None, description="图片列表")
    description: Optional[str] = Field(None, description="商品描述")
    original_price: float = Field(..., gt=0, description="原价")
    current_price: float = Field(..., gt=0, description="现价")
    member_price: Optional[float] = Field(None, gt=0, description="会员价")
    stock: int = Field(0, ge=0, description="库存")
    suitable_tags: Optional[List[str]] = Field(None, description="适用人群标签")
    health_tags: Optional[List[str]] = Field(None, description="健康标签")
    specs: Optional[List[dict]] = Field(None, description="规格")
    is_recommend: int = Field(0, ge=0, le=1, description="是否推荐")
    is_on_sale: int = Field(1, ge=0, le=1, description="是否上架")
    sort_order: int = Field(0, description="排序")


class ProductUpdate(BaseModel):
    """更新商品"""
    category_id: Optional[int] = Field(None, description="分类ID")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="商品名称")
    subtitle: Optional[str] = Field(None, max_length=200, description="副标题")
    images: Optional[List[str]] = Field(None, description="图片列表")
    description: Optional[str] = Field(None, description="商品描述")
    original_price: Optional[float] = Field(None, gt=0, description="原价")
    current_price: Optional[float] = Field(None, gt=0, description="现价")
    member_price: Optional[float] = Field(None, gt=0, description="会员价")
    stock: Optional[int] = Field(None, ge=0, description="库存")
    suitable_tags: Optional[List[str]] = Field(None, description="适用人群标签")
    health_tags: Optional[List[str]] = Field(None, description="健康标签")
    specs: Optional[List[dict]] = Field(None, description="规格")
    is_recommend: Optional[int] = Field(None, ge=0, le=1, description="是否推荐")
    is_on_sale: Optional[int] = Field(None, ge=0, le=1, description="是否上架")
    sort_order: Optional[int] = Field(None, description="排序")


class CategoryCreate(BaseModel):
    """创建分类"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: int = Field(0, description="排序")
    is_active: int = Field(1, ge=0, le=1, description="是否启用")


class CategoryUpdate(BaseModel):
    """更新分类"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="分类名称")
    parent_id: Optional[int] = Field(None, description="父分类ID")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: Optional[int] = Field(None, description="排序")
    is_active: Optional[int] = Field(None, ge=0, le=1, description="是否启用")


@router.get("/product/list")
async def get_product_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    is_on_sale: Optional[int] = Query(None, description="上架状态"),
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取商品列表"""
    conditions = []
    
    if keyword:
        conditions.append(Product.name.like(f"%{keyword}%"))
    
    if category_id:
        conditions.append(Product.category_id == category_id)
    
    if is_on_sale is not None:
        conditions.append(Product.is_on_sale == is_on_sale)
    
    # 查询总数
    count_query = select(func.count()).select_from(Product)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Product)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(Product.sort_order), desc(Product.id)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    items = []
    for p in products:
        items.append({
            "id": p.id,
            "category_id": p.category_id,
            "name": p.name,
            "subtitle": p.subtitle,
            "images": p.images,
            "original_price": float(p.original_price),
            "current_price": float(p.current_price),
            "member_price": float(p.member_price) if p.member_price else None,
            "stock": p.stock,
            "sales_count": p.sales_count,
            "is_recommend": p.is_recommend,
            "is_on_sale": p.is_on_sale,
            "sort_order": p.sort_order,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/product")
async def create_product(
    data: ProductCreate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """创建商品"""
    # 检查分类是否存在
    cat_result = await db.execute(
        select(ProductCategory).where(ProductCategory.id == data.category_id)
    )
    if not cat_result.scalar_one_or_none():
        return error(400, "分类不存在")
    
    product = Product(
        category_id=data.category_id,
        name=data.name,
        subtitle=data.subtitle,
        images=data.images or [],
        description=data.description,
        original_price=data.original_price,
        current_price=data.current_price,
        member_price=data.member_price,
        stock=data.stock,
        suitable_tags=data.suitable_tags,
        health_tags=data.health_tags,
        specs=data.specs,
        is_recommend=data.is_recommend,
        is_on_sale=data.is_on_sale,
        sort_order=data.sort_order,
    )
    db.add(product)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="create",
        target_type="product",
        target_id=None,
        content=f"创建商品: {data.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    await db.refresh(product)
    
    # 更新日志的target_id
    log.target_id = product.id
    await db.commit()
    
    return success(data={"id": product.id}, message="创建成功")


@router.put("/product/{product_id}")
async def update_product(
    product_id: int,
    data: ProductUpdate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """更新商品"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        return error(404, "商品不存在")
    
    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="update",
        target_type="product",
        target_id=product_id,
        content=f"更新商品: {product.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="更新成功")


@router.delete("/product/{product_id}")
async def delete_product(
    product_id: int,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """删除商品（软删除，下架）"""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        return error(404, "商品不存在")
    
    product.is_on_sale = 0
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="delete",
        target_type="product",
        target_id=product_id,
        content=f"删除商品: {product.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="删除成功")


@router.get("/category/list")
async def get_category_list(
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """获取分类列表（树形结构）"""
    result = await db.execute(
        select(ProductCategory).order_by(ProductCategory.sort_order.desc(), ProductCategory.id)
    )
    categories = result.scalars().all()
    
    # 构建树形结构
    category_map = {}
    root_categories = []
    
    for cat in categories:
        category_map[cat.id] = {
            "id": cat.id,
            "name": cat.name,
            "parent_id": cat.parent_id,
            "icon": cat.icon,
            "sort_order": cat.sort_order,
            "is_active": cat.is_active,
            "children": [],
        }
    
    for cat in categories:
        if cat.parent_id and cat.parent_id in category_map:
            category_map[cat.parent_id]["children"].append(category_map[cat.id])
        else:
            root_categories.append(category_map[cat.id])
    
    return success(data=root_categories)


@router.post("/category")
async def create_category(
    data: CategoryCreate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """创建分类"""
    # 检查父分类是否存在
    if data.parent_id:
        parent_result = await db.execute(
            select(ProductCategory).where(ProductCategory.id == data.parent_id)
        )
        if not parent_result.scalar_one_or_none():
            return error(400, "父分类不存在")
    
    category = ProductCategory(
        name=data.name,
        parent_id=data.parent_id,
        icon=data.icon,
        sort_order=data.sort_order,
        is_active=data.is_active,
    )
    db.add(category)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="create",
        target_type="category",
        target_id=None,
        content=f"创建分类: {data.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    await db.refresh(category)
    
    log.target_id = category.id
    await db.commit()
    
    return success(data={"id": category.id}, message="创建成功")


@router.put("/category/{category_id}")
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """更新分类"""
    result = await db.execute(
        select(ProductCategory).where(ProductCategory.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        return error(404, "分类不存在")
    
    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="update",
        target_type="category",
        target_id=category_id,
        content=f"更新分类: {category.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="更新成功")


@router.delete("/category/{category_id}")
async def delete_category(
    category_id: int,
    request: Request,
    admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """删除分类"""
    result = await db.execute(
        select(ProductCategory).where(ProductCategory.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        return error(404, "分类不存在")
    
    # 检查是否有子分类
    child_result = await db.execute(
        select(func.count()).select_from(ProductCategory).where(
            ProductCategory.parent_id == category_id
        )
    )
    if child_result.scalar() > 0:
        return error(400, "存在子分类，无法删除")
    
    # 检查是否有关联商品
    product_result = await db.execute(
        select(func.count()).select_from(Product).where(
            Product.category_id == category_id
        )
    )
    if product_result.scalar() > 0:
        return error(400, "存在关联商品，无法删除")
    
    await db.delete(category)
    
    # 记录操作日志
    log = AdminLog(
        admin_id=admin.id,
        action="delete",
        target_type="category",
        target_id=category_id,
        content=f"删除分类: {category.name}",
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(log)
    
    await db.commit()
    
    return success(message="删除成功")


