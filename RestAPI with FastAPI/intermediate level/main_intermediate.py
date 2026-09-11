from fastapi import FastAPI
from database import engine, Base
from routers.notes import router
import models
from routers.auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(auth_router)