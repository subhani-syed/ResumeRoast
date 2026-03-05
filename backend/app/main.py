from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.db import Base, engine, SessionLocal
from app.routers import auth, resume
from app.dependency import get_current_user
from app.config import settings
from app.services.seed_tiers import seed_tiers
from app.redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_tiers(db)
    yield
    close_redis()

app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.include_router(auth.router)
app.include_router(resume.router)


@app.get("/me")
def read_me(user=Depends(get_current_user)):
    return {
        "id": user.user_id,
        "email": user.email
    }
