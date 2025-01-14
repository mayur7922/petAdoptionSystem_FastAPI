from sqlalchemy import create_engine #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore
from sqlalchemy.orm import sessionmaker #type: ignore

SQLALCHEMY_DATABASE_URL = 'sqlite:///./petAdoption.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()