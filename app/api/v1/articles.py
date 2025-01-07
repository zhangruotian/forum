from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import crud, schemas
from app.api import deps
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User

router = APIRouter()


@router.post("", response_model=schemas.ArticleResponse)
def create_article(
    *,
    article_in: schemas.ArticleCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create new article
    """
    article = crud.article.create(
        db=db,
        obj_in=article_in,
        author_id=current_user.id,
    )
    return article


@router.get("", response_model=schemas.PaginatedResponse[schemas.ArticleResponse])
def list_articles(
    db: Session = Depends(deps.get_db),
    page: int = 1,
    size: int = 10,
):
    """
    Get list of articles with pagination
    """
    skip = (page - 1) * size

    articles = (
        db.query(Article)
        .options(
            joinedload(Article.author),
            joinedload(Article.comments).joinedload(Comment.author),
        )
        .order_by(Article.created_at.desc())
        .offset(skip)
        .limit(size)
        .all()
    )

    total = db.query(Article).count()

    return {
        "items": articles,
        "total": total,
        "page": page,
        "size": size,
    }


@router.get("/{id}", response_model=schemas.ArticleResponse)
def get_article(
    id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get article by ID
    """
    article = (
        db.query(Article)
        .options(
            joinedload(Article.author),
            joinedload(Article.comments).joinedload(Comment.author),
        )
        .filter(Article.id == id)
        .first()
    )

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article
