from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    def create(self, db: Session, *, obj_in: ArticleCreate, author_id: int) -> Article:
        article = super().create(db, obj_in=obj_in, author_id=author_id)
        db.commit()
        return article

    def remove(self, db: Session, *, id: int) -> Article:
        article = db.query(self.model).get(id)
        if article:
            db.delete(article)
            db.commit()
        return article

    def get_by_author(
        self, db: Session, *, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[Article]:
        return (
            db.query(self.model)
            .filter(Article.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


article = CRUDArticle(Article)
