from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    articles = relationship(
        "Article", back_populates="author", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )

    @property
    def article_count(self):
        return len(self.articles)

    @property
    def comment_count(self):
        return len(self.comments)
