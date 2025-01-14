from typing import List
from fastapi import APIRouter, Depends, status, HTTPException #type: ignore
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session #type: ignore
get_db = database.get_db
from .. repository import pet, user

router = APIRouter(
    tags=['Admin']
)

@router.get('/admin/pets')
def all(db: Session = Depends(database.get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    # Role based authentication
    # user cannot access admin routes
    if current_user.role == 'user':
        raise HTTPException(status_code=404, detail="Access denied")
    return pet.get_all(db)

@router.post('/admin/pets', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Pet, db: Session = Depends(get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    # Role based authentication
    # user cannot access admin routes
    if current_user.role == 'user':
        raise HTTPException(status_code=404, detail="Access denied")
    return pet.create(request,db)

@router.put('/admin/pets/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Pet, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    # Role based authentication
    # user cannot access admin routes
    if current_user.role == 'user':
        raise HTTPException(status_code=404, detail="Access denied")
    return pet.update(id,request, db)

@router.delete('/admin/pets/{id}',status_code=204)
def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.User = 
Depends(oauth2.get_current_user)):
    # Role based authentication
    # user cannot access admin routes
    if current_user.role == 'user':
        raise HTTPException(status_code=404, detail="Access denied")
    return pet.destroy(id,db)