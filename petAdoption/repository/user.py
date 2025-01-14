from fastapi import HTTPException, Depends #type: ignore
from sqlalchemy.orm import Session #type: ignore
from .. import schemas, database, models, hashing, oauth2

def create(request: schemas.User, db: Session):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password), role="user")
    db.add(new_user)
    print(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def search(request: schemas.Search, db: Session):
    pets = db.query(models.Pet).filter(models.Pet.type == request.type).all()
    if not pets:
        raise HTTPException(status_code=404, detail="No pets found")
    return pets

def adopt(request: schemas.Adopt, db: Session, current_user: schemas.TokenData):
    print(current_user)
    pet = db.query(models.Pet).filter(models.Pet.id == request.pet_id).first()
    if pet.isAdopted == True:
        raise HTTPException(status_code=404, detail="Pet is already adopted")
    pet.isAdopted=True
    pet.user_id=current_user.id
    db.commit()
    return "Pet adopted successfully"

def Return(request: schemas.Adopt, db: Session, current_user: schemas.TokenData):
    pet = db.query(models.Pet).filter(models.Pet.id == request.pet_id).first()
    if pet.id != current_user.id or pet.isAdopted == False:
        raise HTTPException(status_code=404, detail="You have not adopted this pet")
    pet.isAdopted=False
    pet.user_id=0
    db.commit()
    return "Pet returned successfully"

# funtion for debug endpoint
def show(db: Session):
    users = db.query(models.User).all()
    return users