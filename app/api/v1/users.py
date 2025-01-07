import os
import shutil
import time

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api import deps
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.schemas.user import UserProfileDetail

router = APIRouter()


@router.get("/me", response_model=UserProfileDetail)
def get_current_user(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Get current user with profile details
    """
    # Get recent activity just like in get_user_profile
    recent_articles = (
        db.query(Article)
        .filter(Article.author_id == current_user.id)
        .order_by(desc(Article.created_at))
        .limit(5)
        .all()
    )

    recent_comments = (
        db.query(Comment)
        .filter(Comment.author_id == current_user.id)
        .order_by(desc(Comment.created_at))
        .limit(5)
        .all()
    )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "avatar_url": current_user.avatar_url,
        "article_count": current_user.article_count,
        "comment_count": current_user.comment_count,
        "created_at": current_user.created_at,
        "recent_articles": recent_articles,
        "recent_comments": recent_comments,
    }


@router.get("/{user_id}", response_model=UserProfileDetail)
def get_user_profile(
    user_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get user profile with recent activity
    """
    # First get the user
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get 5 most recent articles
    recent_articles = (
        db.query(Article)
        .filter(Article.author_id == user_id)
        .order_by(desc(Article.created_at))
        .limit(5)
        .all()
    )

    # Get 5 most recent comments
    recent_comments = (
        db.query(Comment)
        .filter(Comment.author_id == user_id)
        .order_by(desc(Comment.created_at))
        .limit(5)
        .all()
    )

    # Create response with recent activity
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "avatar_url": user.avatar_url,
        "article_count": user.article_count,
        "comment_count": user.comment_count,
        "created_at": user.created_at,
        "recent_articles": recent_articles,
        "recent_comments": recent_comments,
    }


@router.post("/{user_id}/avatar", response_model=UserProfileDetail)
async def upload_avatar(
    user_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    request: Request = None,
):
    """
    Upload user avatar
    """
    print(f"Received avatar upload request for user {user_id}")  # Debug log

    # Check if the user is trying to update their own avatar
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update other user's avatar"
        )

    # Validate file type
    print(f"File content type: {file.content_type}")  # Debug log
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join("uploads", "avatars")
        os.makedirs(upload_dir, exist_ok=True)

        # Save file with unique name and timestamp to prevent caching
        timestamp = int(time.time())
        file_extension = os.path.splitext(file.filename)[1].lower()
        file_name = f"avatar_{user_id}_{timestamp}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)
        print(f"Saving file to: {file_path}")  # Debug log

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Get the base URL from the request
        base_url = str(request.base_url).rstrip("/")

        # Update user's avatar_url in database with dynamic host
        avatar_url = f"{base_url}/uploads/avatars/{file_name}"
        print(f"Setting avatar URL to: {avatar_url}")  # Debug log
        db.query(User).filter(User.id == user_id).update({"avatar_url": avatar_url})
        db.commit()

        return get_user_profile(user_id=user_id, db=db)
    except Exception as e:
        print(f"Error uploading avatar: {e}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))
