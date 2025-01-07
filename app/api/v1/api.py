from fastapi import APIRouter

from app.api.v1 import articles, auth, comments, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
