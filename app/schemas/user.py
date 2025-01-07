from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.article import ArticleResponse
from app.schemas.base import UserBase


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    article_count: int
    comment_count: int
    created_at: datetime


class UserProfileDetail(UserBase):
    id: int
    email: str
    full_name: str
    avatar_url: str | None = None
    article_count: int
    comment_count: int
    created_at: datetime
    recent_articles: List[ArticleResponse]
    recent_comments: List["CommentResponse"]  # Forward reference

    model_config = ConfigDict(from_attributes=True)


# Import at the bottom to avoid circular imports
from app.schemas.comment import CommentResponse  # noqa: E402
