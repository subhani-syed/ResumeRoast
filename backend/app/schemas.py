from pydantic import BaseModel, EmailStr
from .models import JobStatus
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class ResumeRoastRequest(BaseModel):
    text: str

class ResumeJobRead(BaseModel):
    id: str
    status: JobStatus
    result_text: Optional[str] = None
    score: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

