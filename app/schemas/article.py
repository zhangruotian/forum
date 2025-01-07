from datetime import datetime
from typing import List

from app.schemas.base import ArticleBase, UserBase
from app.schemas.comment import CommentResponse


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    author: UserBase
    comment_count: int
    created_at: datetime
    comments: List[CommentResponse] = []

    model_config = {"from_attributes": True}
