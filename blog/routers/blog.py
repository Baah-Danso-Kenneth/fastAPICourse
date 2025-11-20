from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas,  models
from ..database import  get_db
from ..repository import blogRepository, userRepository
from typing import List
from sqlalchemy.orm import Session



router = APIRouter(
    prefix = "/blog",
    tags = ['Blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    return blogRepository.get_all_blog(db)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blogRepository.create(request,db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blogRepository.destroy(id, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show_specific_blog(id: int,  db: Session = Depends(get_db)):
    return blogRepository.show(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, db: Session = Depends(get_db)):
    return blogRepository.update(id, db)
