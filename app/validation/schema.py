from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class users(BaseModel):
    username : str
    email : str
    password : str

class create_user(users):
    pass

class response_user(create_user):
    pass

class user_login(BaseModel):
    username:str
    password:str

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool

class TodoCreate(TodoBase):
    owner_id : Optional[int]

class TodoUpdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
