from sqlalchemy import Column, Integer, String, Boolean, ForeignKey #type: ignore
from .database import Base
from sqlalchemy.orm import relationship #type: ignore

class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    breed = Column(String)
    age = Column(Integer)
    isAdopted = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))

    adopter = relationship("User", back_populates="pets")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    pets = relationship('Pet', back_populates="adopter")