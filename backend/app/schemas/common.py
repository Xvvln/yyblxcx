"""
通用 Schema 定义
"""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class PageParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")


class PageResponse(BaseModel, Generic[T]):
    """分页响应"""
    list: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class IdModel(BaseModel):
    """ID模型"""
    id: int


