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

class ResumeResponse(BaseModel):
    id:str
    original_filename:str
    content_type:str
    created_at:datetime
    thumbnail:str

class ResumeDetailResponse(BaseModel):
    resume_id: str
    filename: str
    mime_type: str
    file_size_bytes: int
    created_at: datetime
    download_url: str

class UploadInfoResponse(BaseModel):
    resume_count: int
    resume_upload_remaining: int
