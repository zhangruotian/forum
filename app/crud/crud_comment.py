from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def create(self, db: Session, *, obj_in: CommentCreate, author_id: int) -> Comment:
        comment = super().create(db, obj_in=obj_in, author_id=author_id)
        db.commit()
        return comment

    def remove(self, db: Session, *, id: int) -> Comment:
        comment = db.query(self.model).get(id)
        if comment:
            db.delete(comment)
            db.commit()
        return comment

    def get_by_article(
        self, db: Session, *, article_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.article_id == article_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


comment = CRUDComment(Comment)
