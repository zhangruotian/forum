from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import UserBase


class CommentBase(BaseModel):
    content: str
    article_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    author: UserBase
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# For use in other schemas without circular imports
class CommentInResponse(CommentResponse):
    pass
