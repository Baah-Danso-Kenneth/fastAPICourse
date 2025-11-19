from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog, ShowBlog, User, ShowUser
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/get_blogs', response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = (db.query(models.Blog).filter(models.Blog.id == id))

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog {id} to be deleted does not exist"
        )
    blog.delete(synchronize_session=False)

    db.commit()

    return blog

@app.get('/blog/{id}', status_code=200, response_model=ShowBlog)
def show_specific_blog(id,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with the id {id} is not available'}
    return blog


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: Blog, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(
            status_code =status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id}"
        )
    blog_query.update(request.dict())
    db.commit()
    return {'message': 'Updated Successfully!!!'}


@app.post('/user', response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user/{id}')
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()
    if not user:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, default=f"No user with {id} does not exist in our database")
    return user