from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500))
    status = Column(String(20), default="draft")
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Foreign Keys
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    author = relationship("User", back_populates="articles")
    comments = relationship(
        "Comment", back_populates="article", cascade="all, delete-orphan"
    )

    @property
    def comment_count(self):
        return len(self.comments)
