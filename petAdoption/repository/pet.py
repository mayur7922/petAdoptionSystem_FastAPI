from fastapi import HTTPException #type: ignore
from sqlalchemy.orm import Session #type: ignore
from .. import schemas, database, models

def get_all(db: Session):
    pets = db.query(models.Pet).all()
    return pets

def create(request: schemas.Pet, db: Session):
    new_pet = models.Pet(type=request.type, breed=request.breed, age=request.age, isAdopted=request.isAdopted, user_id=0)
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

def update(id: int, request: schemas.Pet, db: Session):
    pet = db.query(models.Pet).filter(models.Pet.id == id)
    if not pet.first():
        raise HTTPException(status_code=404, detail=f'Pet with the given id {id} does not exits')
    pet.update({
        'type': request.type,
        'breed': request.breed,
        'age': request.age,
        'isAdopted': request.isAdopted,
        'user_id': request.user_id
    })
    db.commit()
    return 'Pet details updated successfully'

def destroy(id: int, db: Session):
    pet = db.query(models.Pet).filter(models.Pet.id == id)
    if not pet.first():
        raise HTTPException(status_code=404, detail=f'Pet with the given id {id} does not exits')
    pet.delete(synchronize_session=False)
    db.commit()
    return 'Pet deleted successfully'