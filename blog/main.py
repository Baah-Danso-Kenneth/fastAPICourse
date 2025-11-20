from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models
from .database import engine
from sqlalchemy.orm import Session
from .routers import blog, user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)