"""
课程接口
GET /course/list - 课程列表
GET /course/{id} - 课程详情
POST /course/{id}/collect - 收藏课程
DELETE /course/{id}/collect - 取消收藏
GET /course/my-collects - 我的收藏
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.course import Course, UserCourseCollect
from app.utils.security import get_current_user, get_current_user_optional
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/course", tags=["课程"])


@router.get("/list")
async def get_course_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    sport_type: Optional[str] = Query(None, description="运动类型"),
    difficulty: Optional[str] = Query(None, description="难度"),
    is_recommend: Optional[int] = Query(None, description="是否推荐"),
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取课程列表"""
    # 构建查询条件
    conditions = [Course.status == 1]
    if sport_type:
        conditions.append(Course.sport_type == sport_type)
    if difficulty:
        conditions.append(Course.difficulty == difficulty)
    if is_recommend is not None:
        conditions.append(Course.is_recommend == is_recommend)
    
    # 查询总数
    count_query = select(func.count()).select_from(Course).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Course).where(*conditions).order_by(
        desc(Course.is_recommend),
        desc(Course.sort_order),
        desc(Course.id)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    courses = result.scalars().all()
    
    # 获取用户收藏状态
    collected_ids = set()
    if current_user:
        collect_result = await db.execute(
            select(UserCourseCollect.course_id).where(
                UserCourseCollect.user_id == current_user.id
            )
        )
        collected_ids = {row[0] for row in collect_result.fetchall()}
    
    items = []
    for c in courses:
        items.append({
            "id": c.id,
            "title": c.title,
            "subtitle": c.subtitle,
            "cover_image": c.cover_image,
            "duration": c.duration,
            "difficulty": c.difficulty,
            "sport_type": c.sport_type,
            "calories": c.calories,
            "coach_name": c.coach_name,
            "play_count": c.play_count,
            "collect_count": c.collect_count,
            "is_free": c.is_free,
            "is_collected": c.id in collected_ids,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/{course_id}")
async def get_course_detail(
    course_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取课程详情"""
    result = await db.execute(
        select(Course).where(Course.id == course_id, Course.status == 1)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        return error(404, "课程不存在")
    
    # 增加播放次数
    course.play_count += 1
    await db.commit()
    
    # 检查是否已收藏
    is_collected = False
    if current_user:
        collect_result = await db.execute(
            select(UserCourseCollect).where(
                UserCourseCollect.user_id == current_user.id,
                UserCourseCollect.course_id == course_id
            )
        )
        is_collected = collect_result.scalar_one_or_none() is not None
    
    data = {
        "id": course.id,
        "title": course.title,
        "subtitle": course.subtitle,
        "cover_image": course.cover_image,
        "video_url": course.video_url,
        "duration": course.duration,
        "difficulty": course.difficulty,
        "sport_type": course.sport_type,
        "calories": course.calories,
        "equipment": course.equipment,
        "description": course.description,
        "coach_name": course.coach_name,
        "coach_avatar": course.coach_avatar,
        "play_count": course.play_count,
        "collect_count": course.collect_count,
        "is_free": course.is_free,
        "is_collected": is_collected,
    }
    
    return success(data=data)


@router.post("/{course_id}/collect")
async def collect_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """收藏课程"""
    # 检查课程是否存在
    result = await db.execute(
        select(Course).where(Course.id == course_id, Course.status == 1)
    )
    course = result.scalar_one_or_none()
    
    if not course:
        return error(404, "课程不存在")
    
    # 检查是否已收藏
    collect_result = await db.execute(
        select(UserCourseCollect).where(
            UserCourseCollect.user_id == current_user.id,
            UserCourseCollect.course_id == course_id
        )
    )
    existing = collect_result.scalar_one_or_none()
    
    if existing:
        return error(400, "已收藏该课程")
    
    # 创建收藏记录
    collect = UserCourseCollect(
        user_id=current_user.id,
        course_id=course_id
    )
    db.add(collect)
    
    # 更新课程收藏数
    course.collect_count += 1
    
    await db.commit()
    
    return success(message="收藏成功")


@router.delete("/{course_id}/collect")
async def uncollect_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏"""
    # 查找收藏记录
    result = await db.execute(
        select(UserCourseCollect).where(
            UserCourseCollect.user_id == current_user.id,
            UserCourseCollect.course_id == course_id
        )
    )
    collect = result.scalar_one_or_none()
    
    if not collect:
        return error(400, "未收藏该课程")
    
    # 删除收藏记录
    await db.delete(collect)
    
    # 更新课程收藏数
    course_result = await db.execute(select(Course).where(Course.id == course_id))
    course = course_result.scalar_one_or_none()
    if course and course.collect_count > 0:
        course.collect_count -= 1
    
    await db.commit()
    
    return success(message="取消收藏成功")


@router.get("/my-collects")
async def get_my_collects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """我的收藏"""
    # 查询总数
    count_query = select(func.count()).select_from(UserCourseCollect).where(
        UserCourseCollect.user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar()
    
    # 联表查询收藏的课程
    query = select(Course, UserCourseCollect.created_at.label("collect_time")).join(
        UserCourseCollect, Course.id == UserCourseCollect.course_id
    ).where(
        UserCourseCollect.user_id == current_user.id,
        Course.status == 1
    ).order_by(desc(UserCourseCollect.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    items = []
    for row in rows:
        course = row[0]
        collect_time = row[1]
        items.append({
            "id": course.id,
            "title": course.title,
            "subtitle": course.subtitle,
            "cover_image": course.cover_image,
            "duration": course.duration,
            "difficulty": course.difficulty,
            "sport_type": course.sport_type,
            "calories": course.calories,
            "coach_name": course.coach_name,
            "is_free": course.is_free,
            "collect_time": collect_time.strftime("%Y-%m-%d %H:%M:%S") if collect_time else None,
        })
    
    return paginate(items, total, page, page_size)




















