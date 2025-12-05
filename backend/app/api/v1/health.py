"""
健康筛查接口
POST /health/screening - 提交筛查数据
GET /health/records - 筛查记录列表
GET /health/report/{id} - 获取报告详情
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from decimal import Decimal

from app.database import get_db
from app.models.user import User
from app.models.health import HealthScreening
from app.utils.security import get_current_user
from app.utils.response import success, error, paginate
from app.utils.helpers import calculate_bmi
from pydantic import BaseModel, Field

router = APIRouter(prefix="/health", tags=["健康筛查"])


class ScreeningCreate(BaseModel):
    """提交筛查数据"""
    height: Optional[Decimal] = Field(None, description="身高(cm)")
    weight: Optional[Decimal] = Field(None, description="体重(kg)")
    heart_rate: Optional[int] = Field(None, description="心率")
    blood_pressure_high: Optional[int] = Field(None, description="收缩压")
    blood_pressure_low: Optional[int] = Field(None, description="舒张压")
    body_temperature: Optional[Decimal] = Field(None, description="体温")
    blood_sugar: Optional[Decimal] = Field(None, description="血糖")
    face_image: Optional[str] = Field(None, description="面部照片")
    body_image: Optional[str] = Field(None, description="体态照片")
    questionnaire_data: Optional[dict] = Field(None, description="问卷数据")


class ScreeningResponse(BaseModel):
    """筛查记录响应"""
    id: int
    height: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    bmi: Optional[Decimal] = None
    heart_rate: Optional[int] = None
    blood_pressure_high: Optional[int] = None
    blood_pressure_low: Optional[int] = None
    body_temperature: Optional[Decimal] = None
    blood_sugar: Optional[Decimal] = None
    risk_level: str = "low"
    risk_tags: Optional[list] = None
    ai_suggestion: Optional[str] = None
    diet_suggestion: Optional[str] = None
    exercise_suggestion: Optional[str] = None
    lifestyle_suggestion: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/screening")
async def create_screening(
    data: ScreeningCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    提交筛查数据
    
    TODO: 暂缓实现 AI 分析功能
    原因: 需要配置百炼平台 API Key
    当前: 返回模拟分析结果
    """
    # 计算 BMI
    bmi = None
    if data.height and data.weight:
        bmi = calculate_bmi(float(data.height), float(data.weight))
    
    # 简单风险评估（模拟）
    risk_level = "low"
    risk_tags = []
    
    if bmi:
        if bmi < 18.5:
            risk_level = "medium"
            risk_tags.append("体重偏低")
        elif bmi >= 24:
            risk_level = "medium"
            risk_tags.append("体重偏高")
        if bmi >= 28:
            risk_level = "high"
    
    if data.blood_pressure_high and data.blood_pressure_high >= 140:
        risk_level = "high" if risk_level != "high" else risk_level
        risk_tags.append("血压偏高")
    
    if data.blood_sugar and float(data.blood_sugar) >= 7.0:
        risk_level = "high"
        risk_tags.append("血糖偏高")
    
    # 生成模拟建议
    ai_suggestion = "根据您的健康数据分析，整体状况良好。建议保持规律作息，适量运动。"
    diet_suggestion = "建议均衡饮食，多吃蔬菜水果，控制油盐糖摄入。"
    exercise_suggestion = "建议每天保持30分钟以上中等强度运动，如快走、慢跑等。"
    lifestyle_suggestion = "建议早睡早起，保证充足睡眠，避免久坐，定期体检。"
    
    if risk_level == "high":
        ai_suggestion = "检测到部分指标异常，建议及时就医咨询专业医生。"
    
    # 创建筛查记录
    screening = HealthScreening(
        user_id=current_user.id,
        height=data.height,
        weight=data.weight,
        bmi=Decimal(str(bmi)) if bmi else None,
        heart_rate=data.heart_rate,
        blood_pressure_high=data.blood_pressure_high,
        blood_pressure_low=data.blood_pressure_low,
        body_temperature=data.body_temperature,
        blood_sugar=data.blood_sugar,
        face_image=data.face_image,
        body_image=data.body_image,
        questionnaire_data=data.questionnaire_data,
        risk_level=risk_level,
        risk_tags=risk_tags,
        ai_suggestion=ai_suggestion,
        diet_suggestion=diet_suggestion,
        exercise_suggestion=exercise_suggestion,
        lifestyle_suggestion=lifestyle_suggestion,
    )
    
    db.add(screening)
    await db.commit()
    await db.refresh(screening)
    
    return success(
        data={"id": screening.id, "risk_level": risk_level},
        message="筛查数据提交成功"
    )


@router.get("/records")
async def get_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取筛查记录列表"""
    # 查询总数
    count_query = select(func.count()).select_from(HealthScreening).where(
        HealthScreening.user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(HealthScreening).where(
        HealthScreening.user_id == current_user.id
    ).order_by(desc(HealthScreening.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    items = []
    for r in records:
        items.append({
            "id": r.id,
            "bmi": float(r.bmi) if r.bmi else None,
            "risk_level": r.risk_level,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None
        })
    
    return paginate(items, total, page, page_size)


@router.get("/report/{screening_id}")
async def get_report(
    screening_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取报告详情"""
    result = await db.execute(
        select(HealthScreening).where(
            HealthScreening.id == screening_id,
            HealthScreening.user_id == current_user.id
        )
    )
    screening = result.scalar_one_or_none()
    
    if not screening:
        return error(404, "报告不存在")
    
    data = {
        "id": screening.id,
        "height": float(screening.height) if screening.height else None,
        "weight": float(screening.weight) if screening.weight else None,
        "bmi": float(screening.bmi) if screening.bmi else None,
        "heart_rate": screening.heart_rate,
        "blood_pressure_high": screening.blood_pressure_high,
        "blood_pressure_low": screening.blood_pressure_low,
        "body_temperature": float(screening.body_temperature) if screening.body_temperature else None,
        "blood_sugar": float(screening.blood_sugar) if screening.blood_sugar else None,
        "risk_level": screening.risk_level,
        "risk_tags": screening.risk_tags,
        "ai_suggestion": screening.ai_suggestion,
        "diet_suggestion": screening.diet_suggestion,
        "exercise_suggestion": screening.exercise_suggestion,
        "lifestyle_suggestion": screening.lifestyle_suggestion,
        "created_at": screening.created_at.strftime("%Y-%m-%d %H:%M:%S") if screening.created_at else None
    }
    
    return success(data=data)
























