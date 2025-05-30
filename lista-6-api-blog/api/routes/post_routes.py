from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Optional
from sqlmodel import Session, select, func, text, or_
from api.models.models import Post, Comment, PostCategory
from api.database import engine, get_session
from fastapi_crudrouter import SQLAlchemyCRUDRouter

router = APIRouter(prefix="/posts", tags=["Posts"])

router.include_router(
    SQLAlchemyCRUDRouter(
        schema=Post,
        create_schema=Post,
        update_schema=Post,
        db_model=Post,
        db=get_session,  
        prefix="",
        tags=["Posts"]
    ),
    prefix=""
)

@router.get("/search")
def search_posts(keyword: str, page: int = 1, size: int = 10):
    with Session(engine) as session:
        statement = select(Post).where(or_(Post.title.contains(keyword), Post.content.contains(keyword)))
        results = session.exec(statement.offset((page-1)*size).limit(size)).all()
    return results

@router.get("/filter")
def filter_posts(category_id: int, page: int = 1, size: int = 10):
    with Session(engine) as session:
        statement = select(Post).join(PostCategory).where(PostCategory.category_id == category_id)
        results = session.exec(statement.offset((page-1)*size).limit(size)).all()
    return results

@router.get("/most_commented")
def most_commented(page: int = 1, size: int = 10):
    with Session(engine) as session:
        statement = select(
            Post, func.count(Comment.id).label("comment_count")
        ).join(Comment).group_by(Post.id).order_by(text("comment_count DESC"))
        raw = session.exec(statement.offset((page-1)*size).limit(size)).all()
    return [{"post": p, "comment_count": c} for (p, c) in raw]