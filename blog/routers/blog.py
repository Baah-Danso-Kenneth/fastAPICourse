from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas,  models
from ..database import  get_db
from typing import List
from sqlalchemy.orm import Session



router = APIRouter()

@router.get('/get_blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'], response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get('/get_blogs', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
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

@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show_specific_blog(id,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with the id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'details': f'blog with the id {id} is not available'}
    return blog


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(
            status_code =status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id}"
        )
    blog_query.update(request.dict())
    db.commit()
    return {'message': 'Updated Successfully!!!'}
