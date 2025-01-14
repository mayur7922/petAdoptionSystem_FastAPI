from typing import List, Optional 
from pydantic import BaseModel #type: ignore

class PetBase(BaseModel):
    type: str
    breed: str
    age: int
    isAdopted: Optional[bool] = False
    user_id: Optional[int] = 0

class Pet(PetBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    role: str
    pets: List[Pet] = []

    class Config():
        orm_mode = True

class ShowPet(BaseModel):
    type: str
    breed: str
    age: int
    isAdopted: bool
    adoptor: ShowUser

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: str
    role: str

class Search(BaseModel):
    type: str

class Adopt(BaseModel):
    pet_id: int

class Return(BaseModel):
    pet_id: int