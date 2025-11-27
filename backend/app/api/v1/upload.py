"""
上传接口
POST /upload/image - 上传图片
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import os
import uuid
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.models.system import File as FileModel
from app.utils.security import get_current_user
from app.utils.response import success, error

router = APIRouter(prefix="/upload", tags=["上传"])


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    category: Optional[str] = Form("images", description="分类: avatars/images/posts"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传图片"""
    # 验证文件类型
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        return error(400, "不支持的图片格式，仅支持 jpg/png/gif/webp")
    
    # 读取文件内容
    content = await file.read()
    
    # 验证文件大小
    if len(content) > settings.MAX_FILE_SIZE:
        return error(400, f"文件大小超过限制，最大 {settings.MAX_FILE_SIZE // 1024 // 1024}MB")
    
    # 生成文件名
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    # 按日期组织目录
    date_dir = datetime.now().strftime("%Y%m")
    upload_dir = os.path.join(settings.UPLOAD_DIR, category, date_dir)
    os.makedirs(upload_dir, exist_ok=True)
    
    filepath = os.path.join(upload_dir, filename)
    
    # 保存文件
    with open(filepath, "wb") as f:
        f.write(content)
    
    # 生成访问URL
    url = f"/uploads/{category}/{date_dir}/{filename}"
    
    # 记录到数据库
    file_record = FileModel(
        user_id=current_user.id,
        filename=file.filename,
        filepath=filepath,
        file_type=category,
        file_size=len(content),
        mime_type=file.content_type,
    )
    db.add(file_record)
    await db.commit()
    
    return success(
        data={
            "url": url,
            "filename": filename,
            "size": len(content)
        },
        message="上传成功"
    )


