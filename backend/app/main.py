from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db import Base, engine
from app.routers import auth,resume
from app.dependency import get_current_user
from app.config import settings

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://ui:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
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
