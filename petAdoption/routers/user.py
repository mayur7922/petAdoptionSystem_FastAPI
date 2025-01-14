from typing import List
from fastapi import APIRouter, Depends, HTTPException #type: ignore
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session #type: ignore
from .. repository import user
get_db = database.get_db

router = APIRouter()

@router.post('/register',response_model=schemas.ShowUser, tags=['Authentication'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # new_user = models.User(request) doubt here 2:21:32
    return user.create(request,db)

@router.get('/user',response_model=List[schemas.ShowUser],tags=['debug'])
def all(db: Session = Depends(get_db)):
    return user.show(db)

@router.post('/pets',tags=['Users'])
def all(request: schemas.Search, db: Session = Depends(get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    if current_user.role == 'admin':
        raise HTTPException(status_code=404, detail="Access denied")
    return user.search(request,db)

@router.post('/pets/adopt',tags=['Users'])
def all(request: schemas.Adopt, db: Session = Depends(get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    return user.adopt(request,db,current_user)

@router.post('/pets/return',tags=['Users'])
def all(request: schemas.Return, db: Session = Depends(get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    return user.Return(request,db,current_user)