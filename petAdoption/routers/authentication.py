from fastapi import APIRouter, Depends, status, HTTPException #type: ignore
from .. import schemas, database, models
from ..hashing import Hash
from sqlalchemy.orm import Session #type: ignore
from .. token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm #type: ignore

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail='Invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail='Incorrect password')
    
    access_token = create_access_token(data={"id": user.id, "email": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}