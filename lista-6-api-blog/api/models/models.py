from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int
    category_ids: List[int] = []
    
class PostCategory(SQLModel, table=True):
    post_id: int = Field(foreign_key="post.id", primary_key=True)  # Removido Optional
    category_id: int = Field(foreign_key="category.id", primary_key=True) 

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str

    posts: List["Post"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
    likes: List["Like"] = Relationship(back_populates="user")

class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    posts: List["Post"] = Relationship(
        back_populates="categories",
        link_model=PostCategory
    )
    
class PostRead(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    categories: List[CategoryRead] = []  

    class Config:
        from_attributes = True

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")
    likes: List["Like"] = Relationship(back_populates="post")
    categories: List[Category] = Relationship(
        back_populates="posts",
        link_model=PostCategory
    )

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")

    post: Optional[Post] = Relationship(back_populates="comments")
    user: Optional[User] = Relationship(back_populates="comments")

class Like(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id")
    user_id: int = Field(foreign_key="user.id")

    post: Optional[Post] = Relationship(back_populates="likes")
    user: Optional[User] = Relationship(back_populates="likes")
