from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlmodel import Session, select, func, text, or_
from api.models.models import Category, Post, Comment, PostCategory, PostCreate, PostRead
from api.database import engine, get_session
from fastapi_crudrouter import SQLAlchemyCRUDRouter

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead)
def create_post(post: PostCreate, db: Session = Depends(get_session)):
    # 1. Cria o post básico
    db_post = Post(**post.dict(exclude={"category_ids"}))
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # 2. Processa as categorias
    if post.category_ids:
        for category_id in post.category_ids:
            # Verifica se a categoria existe
            category = db.get(Category, category_id)
            if not category:
                raise HTTPException(status_code=404, detail=f"Categoria {category_id} não encontrada")
            
            # Cria a associação
            db.add(PostCategory(post_id=db_post.id, category_id=category_id))
        
        db.commit()
        db.refresh(db_post)

    return db_post

@router.put("/{item_id}", response_model=PostRead)
def update_post(item_id: int, post: PostCreate, db: Session = Depends(get_session)):
    # 1. Atualiza o post básico
    db_post = db.get(Post, item_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    for key, value in post.dict(exclude={"category_ids"}).items():
        setattr(db_post, key, value)
    
    # 2. Remove todas as associações existentes
    db.exec(select(PostCategory).where(PostCategory.post_id == item_id)).delete()
    
    # 3. Adiciona as novas associações
    if post.category_ids:
        for category_id in post.category_ids:
            category = db.get(Category, category_id)
            if not category:
                raise HTTPException(status_code=404, detail=f"Categoria {category_id} não encontrada")
            
            db.add(PostCategory(post_id=item_id, category_id=category_id))
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostRead])
def read_posts(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_session)
):
    # Obtém todos os posts com suas categorias carregadas
    posts = db.exec(
        select(Post)
        .offset(skip)
        .limit(limit)
    ).all()
    
    return posts

# Mantenha suas rotas existentes de search, filter e most_commented
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=PostRead,
        create_schema=PostCreate,
        update_schema=PostCreate,
        db_model=Post,
        db=get_session,
        prefix="",
        tags=["Posts"],
        get_all_route=False,  # Desativa as rotas padrão que vamos substituir
        create_route=False,
        update_route=False
    )
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