"""
社区接口
GET /community/posts - 动态列表
POST /community/post - 发布动态
DELETE /community/post/{id} - 删除动态
POST /community/post/{id}/like - 点赞
DELETE /community/post/{id}/like - 取消点赞
POST /community/post/{id}/comment - 评论
GET /community/following - 关注列表
GET /community/followers - 粉丝列表
POST /community/follow/{user_id} - 关注用户
DELETE /community/follow/{user_id} - 取消关注
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_, or_
from typing import Optional, List
from pydantic import BaseModel, Field

from app.database import get_db
from app.models.user import User
from app.models.community import Post, PostComment, PostLike, UserFollow
from app.utils.security import get_current_user, get_current_user_optional
from app.utils.response import success, error, paginate

router = APIRouter(prefix="/community", tags=["社区"])


class PostCreate(BaseModel):
    """发布动态"""
    content: str = Field(..., min_length=1, max_length=2000, description="内容")
    images: Optional[List[str]] = Field(None, description="图片列表")
    video_url: Optional[str] = Field(None, description="视频地址")
    topic_id: Optional[int] = Field(None, description="话题ID")
    location: Optional[str] = Field(None, max_length=100, description="位置")


class CommentCreate(BaseModel):
    """发表评论"""
    content: str = Field(..., min_length=1, max_length=500, description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID")
    reply_to_user_id: Optional[int] = Field(None, description="回复用户ID")


@router.get("/posts")
async def get_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    user_id: Optional[int] = Query(None, description="指定用户的动态"),
    topic_id: Optional[int] = Query(None, description="指定话题"),
    following_only: int = Query(0, description="仅关注的人"),
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取动态列表"""
    conditions = [Post.status == 1]
    
    if user_id:
        conditions.append(Post.user_id == user_id)
    if topic_id:
        conditions.append(Post.topic_id == topic_id)
    
    # 仅关注的人
    if following_only == 1 and current_user:
        following_result = await db.execute(
            select(UserFollow.follow_user_id).where(UserFollow.user_id == current_user.id)
        )
        following_ids = [row[0] for row in following_result.fetchall()]
        if following_ids:
            conditions.append(Post.user_id.in_(following_ids))
        else:
            return paginate([], 0, page, page_size)
    
    # 查询总数
    count_query = select(func.count()).select_from(Post).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    # 查询列表
    query = select(Post).where(*conditions).order_by(
        desc(Post.is_top), desc(Post.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    posts = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([p.user_id for p in posts]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    # 获取当前用户的点赞状态
    liked_post_ids = set()
    if current_user:
        likes_result = await db.execute(
            select(PostLike.post_id).where(PostLike.user_id == current_user.id)
        )
        liked_post_ids = {row[0] for row in likes_result.fetchall()}
    
    items = []
    for p in posts:
        user = users.get(p.user_id)
        items.append({
            "id": p.id,
            "content": p.content,
            "images": p.images,
            "video_url": p.video_url,
            "location": p.location,
            "view_count": p.view_count,
            "like_count": p.like_count,
            "comment_count": p.comment_count,
            "is_top": p.is_top,
            "is_essence": p.is_essence,
            "is_liked": p.id in liked_post_ids,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S") if p.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/post/{post_id}")
async def get_post_detail(
    post_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取动态详情"""
    # 查询动态
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status == 1)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        return error(404, "动态不存在")
    
    # 增加浏览量
    post.view_count = (post.view_count or 0) + 1
    await db.commit()
    
    # 查询作者信息
    user_result = await db.execute(select(User).where(User.id == post.user_id))
    user = user_result.scalar_one_or_none()
    
    # 检查是否点赞
    is_liked = False
    if current_user:
        like_result = await db.execute(
            select(PostLike).where(
                PostLike.post_id == post_id,
                PostLike.user_id == current_user.id
            )
        )
        is_liked = like_result.scalar_one_or_none() is not None
    
    # 检查是否关注作者
    is_followed = False
    if current_user and user and current_user.id != user.id:
        follow_result = await db.execute(
            select(UserFollow).where(
                UserFollow.user_id == current_user.id,
                UserFollow.follow_user_id == user.id
            )
        )
        is_followed = follow_result.scalar_one_or_none() is not None
    
    return success(data={
        "id": post.id,
        "content": post.content,
        "images": post.images,
        "video_url": post.video_url,
        "location": post.location,
        "topic_id": post.topic_id,
        "view_count": post.view_count,
        "like_count": post.like_count,
        "comment_count": post.comment_count,
        "is_top": post.is_top,
        "is_essence": post.is_essence,
        "is_liked": is_liked,
        "user": {
            "id": user.id if user else None,
            "nickname": user.nickname if user else "未知用户",
            "avatar": user.avatar if user else None,
        },
        "is_followed": is_followed,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S") if post.created_at else None,
    })


@router.post("/post")
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发布动态"""
    post = Post(
        user_id=current_user.id,
        content=data.content,
        images=data.images,
        video_url=data.video_url,
        topic_id=data.topic_id,
        location=data.location,
        status=1,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    return success(data={"id": post.id}, message="发布成功")


@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除动态"""
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.user_id == current_user.id)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        return error(404, "动态不存在")
    
    post.status = 0
    await db.commit()
    
    return success(message="删除成功")


@router.post("/post/{post_id}/like")
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """点赞动态"""
    # 检查动态是否存在
    post_result = await db.execute(select(Post).where(Post.id == post_id, Post.status == 1))
    post = post_result.scalar_one_or_none()
    
    if not post:
        return error(404, "动态不存在")
    
    # 检查是否已点赞
    existing = await db.execute(
        select(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        return error(400, "已点赞")
    
    # 创建点赞记录
    like = PostLike(post_id=post_id, user_id=current_user.id)
    db.add(like)
    
    # 更新点赞数
    post.like_count += 1
    
    await db.commit()
    
    return success(message="点赞成功")


@router.delete("/post/{post_id}/like")
async def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消点赞"""
    result = await db.execute(
        select(PostLike).where(PostLike.post_id == post_id, PostLike.user_id == current_user.id)
    )
    like = result.scalar_one_or_none()
    
    if not like:
        return error(400, "未点赞")
    
    await db.delete(like)
    
    # 更新点赞数
    post_result = await db.execute(select(Post).where(Post.id == post_id))
    post = post_result.scalar_one_or_none()
    if post and post.like_count > 0:
        post.like_count -= 1
    
    await db.commit()
    
    return success(message="取消点赞")


@router.post("/post/{post_id}/comment")
async def create_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发表评论"""
    # 检查动态是否存在
    post_result = await db.execute(select(Post).where(Post.id == post_id, Post.status == 1))
    post = post_result.scalar_one_or_none()
    
    if not post:
        return error(404, "动态不存在")
    
    # 创建评论
    comment = PostComment(
        post_id=post_id,
        user_id=current_user.id,
        parent_id=data.parent_id,
        reply_to_user_id=data.reply_to_user_id,
        content=data.content,
    )
    db.add(comment)
    
    # 更新评论数
    post.comment_count += 1
    
    await db.commit()
    await db.refresh(comment)
    
    return success(data={"id": comment.id}, message="评论成功")


@router.get("/following")
async def get_following(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """关注列表"""
    count_query = select(func.count()).select_from(UserFollow).where(
        UserFollow.user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar()
    
    query = select(UserFollow, User).join(
        User, UserFollow.follow_user_id == User.id
    ).where(
        UserFollow.user_id == current_user.id
    ).order_by(desc(UserFollow.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    items = []
    for row in rows:
        follow, user = row
        items.append({
            "id": user.id,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "follower_count": user.follower_count,
            "follow_time": follow.created_at.strftime("%Y-%m-%d %H:%M:%S") if follow.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/followers")
async def get_followers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """粉丝列表"""
    count_query = select(func.count()).select_from(UserFollow).where(
        UserFollow.follow_user_id == current_user.id
    )
    total = (await db.execute(count_query)).scalar()
    
    query = select(UserFollow, User).join(
        User, UserFollow.user_id == User.id
    ).where(
        UserFollow.follow_user_id == current_user.id
    ).order_by(desc(UserFollow.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    # 获取当前用户关注的人
    following_result = await db.execute(
        select(UserFollow.follow_user_id).where(UserFollow.user_id == current_user.id)
    )
    following_ids = {row[0] for row in following_result.fetchall()}
    
    items = []
    for row in rows:
        follow, user = row
        items.append({
            "id": user.id,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "follower_count": user.follower_count,
            "is_following": user.id in following_ids,
            "follow_time": follow.created_at.strftime("%Y-%m-%d %H:%M:%S") if follow.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.post("/follow/{user_id}")
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """关注用户"""
    if user_id == current_user.id:
        return error(400, "不能关注自己")
    
    # 检查用户是否存在
    target_user_result = await db.execute(select(User).where(User.id == user_id))
    target_user = target_user_result.scalar_one_or_none()
    
    if not target_user:
        return error(404, "用户不存在")
    
    # 检查是否已关注
    existing = await db.execute(
        select(UserFollow).where(
            UserFollow.user_id == current_user.id,
            UserFollow.follow_user_id == user_id
        )
    )
    if existing.scalar_one_or_none():
        return error(400, "已关注该用户")
    
    # 创建关注关系
    follow = UserFollow(user_id=current_user.id, follow_user_id=user_id)
    db.add(follow)
    
    # 更新计数
    current_user.following_count += 1
    target_user.follower_count += 1
    
    await db.commit()
    
    return success(message="关注成功")


@router.delete("/follow/{user_id}")
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消关注"""
    result = await db.execute(
        select(UserFollow).where(
            UserFollow.user_id == current_user.id,
            UserFollow.follow_user_id == user_id
        )
    )
    follow = result.scalar_one_or_none()
    
    if not follow:
        return error(400, "未关注该用户")
    
    await db.delete(follow)
    
    # 更新计数
    if current_user.following_count > 0:
        current_user.following_count -= 1
    
    target_user_result = await db.execute(select(User).where(User.id == user_id))
    target_user = target_user_result.scalar_one_or_none()
    if target_user and target_user.follower_count > 0:
        target_user.follower_count -= 1
    
    await db.commit()
    
    return success(message="取消关注成功")


@router.get("/post/{post_id}/comments")
async def get_post_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    """获取帖子评论列表"""
    # 检查帖子是否存在
    post_result = await db.execute(select(Post).where(Post.id == post_id, Post.status == 1))
    if not post_result.scalar_one_or_none():
        return error(404, "动态不存在")
    
    # 只获取顶层评论
    conditions = [PostComment.post_id == post_id, PostComment.parent_id == None]
    
    count_query = select(func.count()).select_from(PostComment).where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    query = select(PostComment).where(*conditions).order_by(
        desc(PostComment.created_at)
    ).offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    comments = result.scalars().all()
    
    # 获取用户信息
    user_ids = list(set([c.user_id for c in comments]))
    users = {}
    if user_ids:
        users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = {u.id: u for u in users_result.scalars().all()}
    
    # 获取每条评论的回复数
    comment_ids = [c.id for c in comments]
    reply_counts = {}
    if comment_ids:
        for cid in comment_ids:
            count = (await db.execute(
                select(func.count()).select_from(PostComment).where(PostComment.parent_id == cid)
            )).scalar()
            reply_counts[cid] = count
    
    items = []
    for c in comments:
        user = users.get(c.user_id)
        items.append({
            "id": c.id,
            "content": c.content,
            "like_count": c.like_count,
            "reply_count": reply_counts.get(c.id, 0),
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
            },
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/topics")
async def get_topics(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    is_hot: Optional[int] = Query(None, description="是否热门"),
    db: AsyncSession = Depends(get_db)
):
    """获取话题列表"""
    from app.models.community import Topic
    
    conditions = []
    if is_hot is not None:
        conditions.append(Topic.is_hot == is_hot)
    
    count_query = select(func.count()).select_from(Topic)
    if conditions:
        count_query = count_query.where(*conditions)
    total = (await db.execute(count_query)).scalar()
    
    query = select(Topic)
    if conditions:
        query = query.where(*conditions)
    query = query.order_by(desc(Topic.sort_order), desc(Topic.post_count)).offset(
        (page - 1) * page_size
    ).limit(page_size)
    
    result = await db.execute(query)
    topics = result.scalars().all()
    
    items = []
    for t in topics:
        items.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "cover_image": t.cover_image,
            "post_count": t.post_count,
            "participant_count": t.participant_count,
            "is_hot": t.is_hot,
        })
    
    return paginate(items, total, page, page_size)


@router.get("/topic/{topic_id}")
async def get_topic_detail(
    topic_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取话题详情"""
    from app.models.community import Topic
    
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    topic = result.scalar_one_or_none()
    
    if not topic:
        return error(404, "话题不存在")
    
    return success(data={
        "id": topic.id,
        "name": topic.name,
        "description": topic.description,
        "cover_image": topic.cover_image,
        "post_count": topic.post_count,
        "participant_count": topic.participant_count,
        "is_hot": topic.is_hot,
    })


@router.get("/ranking")
async def get_ranking(
    ranking_type: str = Query("checkin", description="排行类型: checkin/sport/points"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """获取排行榜"""
    if ranking_type == "checkin":
        # 打卡天数排行
        query = select(User).where(User.status == 1).order_by(
            desc(User.continuous_checkin_days), desc(User.total_checkin_days)
        ).offset((page - 1) * page_size).limit(page_size)
        
        count_query = select(func.count()).select_from(User).where(User.status == 1)
        total = (await db.execute(count_query)).scalar()
        
        result = await db.execute(query)
        users = result.scalars().all()
        
        items = []
        for i, u in enumerate(users):
            items.append({
                "rank": (page - 1) * page_size + i + 1,
                "user_id": u.id,
                "nickname": u.nickname,
                "avatar": u.avatar,
                "value": u.continuous_checkin_days,
                "extra": f"累计{u.total_checkin_days}天",
            })
    
    elif ranking_type == "sport":
        # 运动时长排行（本周）
        from datetime import datetime, timedelta
        from app.models.sport import SportRecord
        
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 统计本周运动时长
        query = select(
            SportRecord.user_id,
            func.sum(SportRecord.duration).label("total_duration")
        ).where(
            SportRecord.start_time >= week_start
        ).group_by(SportRecord.user_id).order_by(
            desc("total_duration")
        ).offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        # 获取用户信息
        user_ids = [row[0] for row in rows]
        users = {}
        if user_ids:
            users_result = await db.execute(select(User).where(User.id.in_(user_ids)))
            users = {u.id: u for u in users_result.scalars().all()}
        
        items = []
        for i, row in enumerate(rows):
            user = users.get(row[0])
            items.append({
                "rank": (page - 1) * page_size + i + 1,
                "user_id": row[0],
                "nickname": user.nickname if user else "未知用户",
                "avatar": user.avatar if user else None,
                "value": row[1],
                "extra": f"{row[1]}分钟",
            })
        
        total = len(items)
    
    elif ranking_type == "points":
        # 积分排行
        query = select(User).where(User.status == 1).order_by(
            desc(User.sport_coins + User.food_coins)
        ).offset((page - 1) * page_size).limit(page_size)
        
        count_query = select(func.count()).select_from(User).where(User.status == 1)
        total = (await db.execute(count_query)).scalar()
        
        result = await db.execute(query)
        users = result.scalars().all()
        
        items = []
        for i, u in enumerate(users):
            total_coins = u.sport_coins + u.food_coins
            items.append({
                "rank": (page - 1) * page_size + i + 1,
                "user_id": u.id,
                "nickname": u.nickname,
                "avatar": u.avatar,
                "value": total_coins,
                "extra": f"运动币{u.sport_coins} 膳食币{u.food_coins}",
            })
    
    else:
        return error(400, "不支持的排行类型")
    
    return paginate(items, total, page, page_size)

