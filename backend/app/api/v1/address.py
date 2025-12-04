"""
地址接口
GET /address/list - 地址列表
POST /address - 添加地址
PUT /address/{id} - 修改地址
DELETE /address/{id} - 删除地址
PUT /address/{id}/default - 设为默认
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User, UserAddress
from app.schemas.user import UserAddressCreate, UserAddressUpdate, UserAddressSchema
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/address", tags=["地址"])


@router.get("/list")
async def get_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取地址列表"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.user_id == current_user.id
        ).order_by(UserAddress.is_default.desc(), UserAddress.id.desc())
    )
    addresses = result.scalars().all()
    
    items = [UserAddressSchema.model_validate(a).model_dump() for a in addresses]
    
    return success(data=items)


@router.post("")
async def create_address(
    data: UserAddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加地址"""
    # 如果设为默认，清除其他默认地址
    if data.is_default == 1:
        await db.execute(
            UserAddress.__table__.update().where(
                UserAddress.user_id == current_user.id
            ).values(is_default=0)
        )
    
    address = UserAddress(
        user_id=current_user.id,
        **data.model_dump()
    )
    db.add(address)
    await db.commit()
    await db.refresh(address)
    
    return success(data={"id": address.id}, message="添加成功")


@router.put("/{address_id}")
async def update_address(
    address_id: int,
    data: UserAddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改地址"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id
        )
    )
    address = result.scalar_one_or_none()
    
    if not address:
        return error(404, "地址不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # 如果设为默认，清除其他默认地址
    if update_data.get("is_default") == 1:
        await db.execute(
            UserAddress.__table__.update().where(
                UserAddress.user_id == current_user.id,
                UserAddress.id != address_id
            ).values(is_default=0)
        )
    
    for field, value in update_data.items():
        setattr(address, field, value)
    
    await db.commit()
    
    return success(message="修改成功")


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除地址"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id
        )
    )
    address = result.scalar_one_or_none()
    
    if not address:
        return error(404, "地址不存在")
    
    await db.delete(address)
    await db.commit()
    
    return success(message="删除成功")


@router.put("/{address_id}/default")
async def set_default_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """设为默认地址"""
    result = await db.execute(
        select(UserAddress).where(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id
        )
    )
    address = result.scalar_one_or_none()
    
    if not address:
        return error(404, "地址不存在")
    
    # 清除其他默认地址
    await db.execute(
        UserAddress.__table__.update().where(
            UserAddress.user_id == current_user.id
        ).values(is_default=0)
    )
    
    # 设置当前地址为默认
    address.is_default = 1
    await db.commit()
    
    return success(message="设置成功")




















