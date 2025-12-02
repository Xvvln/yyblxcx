"""
统一响应格式模块
"""
from typing import Any, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """统一响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


def success(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error(code: int = 400, message: str = "请求失败", data: Any = None) -> dict:
    """错误响应"""
    return {
        "code": code,
        "message": message,
        "data": data
    }


def paginate(items: list, total: int, page: int, page_size: int) -> dict:
    """分页响应"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
    }















