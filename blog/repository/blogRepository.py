from fastapi import  HTTPException
from .. import schemas,  models
from sqlalchemy.orm import Session


def get_all_blog(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int , db: Session):
    blog = (db.query(models.Blog).filter(models.Blog.id == id))

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"blog {id} to be deleted does not exist"
        )
    blog.delete(synchronize_session=False)

    db.commit()

    return blog


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"blog with the id {id} is not available")
    return blog


def update(id: int, request: schemas.BlogUpdate,  db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()

    if not blog:
        raise HTTPException(
            status_code =status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id}"
        )
    blog_query.update(request.dict())
    db.commit()
    db.refresh(blog)
    return blog