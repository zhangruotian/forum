from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import crud, schemas
from app.api import deps
from app.models.comment import Comment
from app.models.user import User

router = APIRouter()


@router.get("/article/{article_id}", response_model=List[schemas.CommentResponse])
def list_comments(
    article_id: int,
    db: Session = Depends(deps.get_db),
):
    """
    Get all comments for an article.
    """
    article = crud.article.get(db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    comments = (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.article_id == article_id)
        .all()
    )
    return comments


@router.post("", response_model=schemas.CommentResponse)
def create_comment(
    comment_in: schemas.CommentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new comment.
    """
    article = crud.article.get(db, id=comment_in.article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    comment = crud.comment.create(db, obj_in=comment_in, author_id=current_user.id)
    db.commit()

    # Refresh to get the relationships loaded
    db.refresh(comment)
    return comment


@router.delete("/{id}", response_model=schemas.CommentResponse)
def delete_comment(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a comment.
    """
    comment = crud.comment.get(db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    comment = crud.comment.remove(db, id=id)
    return comment
