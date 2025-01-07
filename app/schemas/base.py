from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    article_count: int = 0
    comment_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class ArticleBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str] = []
    status: str = "draft"


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

    model_config = {"from_attributes": True}
