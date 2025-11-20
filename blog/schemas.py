from pydantic import BaseModel, constr, validator
from typing import List


class Blog(BaseModel):
    id: int
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: constr(min_length=1, max_length=50)

    @validator('password')
    def password_size_limit(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password too long when encoded (max 72 bytes)')
        return v

    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser | None = None

    class Config:
        orm_mode = True


class UserBlog(BaseModel):
    name: str
    email: str
    blogs: List[Blog]=[]

    class Config():
        orm_mode = True
