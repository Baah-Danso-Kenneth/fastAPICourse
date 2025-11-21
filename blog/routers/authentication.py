from fastapi import APIRouter,status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import  database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter()


@router.post('/login/', tags=['Authentication'])
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Password did not match')

    access_token = token.create_access_token(
        data={"sub": user.email})

    return {"access_token":access_token, "token_type": "bearer"}

