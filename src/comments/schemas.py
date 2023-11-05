from typing import Optional

from pydantic import BaseModel


# Shared properties
class CommentBase(BaseModel):
    text_value: str

# Properties to receive on comment creation
class CommentCreate(CommentBase):    
    user_id: int
    ad_id: int


# Properties to receive on comment update
class CommentUpdate(CommentBase):
    pass


# Properties shared by models stored in DB
class Comment(CommentCreate):
    id: int

    class Config:
        from_attributes = True
