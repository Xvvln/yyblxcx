"""
远程医疗接口
GET /doctor/list - 医生列表
GET /doctor/{id} - 医生详情
GET /article/list - 科普文章列表
GET /article/{id} - 文章详情
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.response import success, error, paginate

router = APIRouter(tags=["远程医疗"])


# 模拟医生数据
MOCK_DOCTORS = [
    {
        "id": 1,
        "name": "张医生",
        "title": "主任医师",
        "hospital": "北京协和医院",
        "department": "营养科",
        "avatar": None,
        "specialty": ["营养不良", "减重指导", "慢病饮食"],
        "description": "从事临床营养工作20年，擅长营养不良诊治和慢病饮食指导。",
        "consultation_fee": 50.00,
        "rating": 4.9,
        "consultation_count": 1234,
    },
    {
        "id": 2,
        "name": "李医生",
        "title": "副主任医师",
        "hospital": "上海瑞金医院",
        "department": "内分泌科",
        "avatar": None,
        "specialty": ["糖尿病", "甲状腺疾病", "代谢综合征"],
        "description": "内分泌科专家，擅长糖尿病及其并发症的诊治。",
        "consultation_fee": 40.00,
        "rating": 4.8,
        "consultation_count": 856,
    },
    {
        "id": 3,
        "name": "王医生",
        "title": "主治医师",
        "hospital": "广州中山医院",
        "department": "运动医学科",
        "avatar": None,
        "specialty": ["运动损伤", "康复训练", "运动处方"],
        "description": "运动医学专家，为患者制定个性化运动康复方案。",
        "consultation_fee": 35.00,
        "rating": 4.7,
        "consultation_count": 567,
    },
]


# 模拟文章数据
MOCK_ARTICLES = [
    {
        "id": 1,
        "title": "如何科学减重",
        "cover_image": None,
        "summary": "减重不是简单的少吃多动，需要科学的方法和持之以恒的坚持。",
        "content": "减重是一个系统工程，需要从饮食、运动、睡眠等多方面入手...",
        "author": "张医生",
        "category": "减重",
        "view_count": 12345,
        "like_count": 234,
        "created_at": "2024-01-15 10:00:00",
    },
    {
        "id": 2,
        "title": "糖尿病患者的饮食指南",
        "cover_image": None,
        "summary": "糖尿病患者如何科学饮食，控制血糖的同时保证营养均衡。",
        "content": "糖尿病饮食的核心是控制总热量，合理分配三大营养素...",
        "author": "李医生",
        "category": "饮食",
        "view_count": 8765,
        "like_count": 156,
        "created_at": "2024-01-10 14:30:00",
    },
    {
        "id": 3,
        "title": "运动损伤的预防与处理",
        "cover_image": None,
        "summary": "运动中如何避免损伤，以及损伤后的正确处理方法。",
        "content": "运动前热身是预防损伤的第一步，正确的运动姿势也很重要...",
        "author": "王医生",
        "category": "运动",
        "view_count": 5432,
        "like_count": 98,
        "created_at": "2024-01-05 09:00:00",
    },
]


@router.get("/doctor/list")
async def get_doctor_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    department: str = Query(None, description="科室筛选"),
):
    """获取医生列表"""
    doctors = MOCK_DOCTORS
    if department:
        doctors = [d for d in doctors if department in d["department"]]
    
    total = len(doctors)
    start = (page - 1) * page_size
    end = start + page_size
    items = doctors[start:end]
    
    return paginate(items, total, page, page_size)


@router.get("/doctor/{doctor_id}")
async def get_doctor_detail(doctor_id: int):
    """获取医生详情"""
    for doctor in MOCK_DOCTORS:
        if doctor["id"] == doctor_id:
            # 添加更多详情
            doctor_detail = {
                **doctor,
                "schedule": [
                    {"day": "周一", "time": "09:00-12:00"},
                    {"day": "周三", "time": "14:00-17:00"},
                    {"day": "周五", "time": "09:00-12:00"},
                ],
            }
            return success(data=doctor_detail)
    
    return error(404, "医生不存在")


@router.get("/article/list")
async def get_article_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category: str = Query(None, description="分类筛选"),
):
    """获取科普文章列表"""
    articles = MOCK_ARTICLES
    if category:
        articles = [a for a in articles if category in a["category"]]
    
    total = len(articles)
    start = (page - 1) * page_size
    end = start + page_size
    
    # 列表不返回完整内容
    items = []
    for a in articles[start:end]:
        item = {k: v for k, v in a.items() if k != "content"}
        items.append(item)
    
    return paginate(items, total, page, page_size)


@router.get("/article/{article_id}")
async def get_article_detail(article_id: int):
    """获取文章详情"""
    for article in MOCK_ARTICLES:
        if article["id"] == article_id:
            # 增加阅读量
            article["view_count"] += 1
            return success(data=article)
    
    return error(404, "文章不存在")



















