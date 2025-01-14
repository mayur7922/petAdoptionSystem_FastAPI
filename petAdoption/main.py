from fastapi import FastAPI #type: ignore
from . import models
from . database import engine
from . routers import admin, authentication, user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(user.router)