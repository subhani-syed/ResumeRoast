from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routers import auth,resume
from app.dependency import get_current_user
from app import models

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(resume.router)

@app.get("/me")
def read_me(user=Depends(get_current_user)):
    return {
        "id": user.user_id,
        "email": user.email
    }
