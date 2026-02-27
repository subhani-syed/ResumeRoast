import enum
from typing import Optional
from datetime import datetime
from app.db import Base
from sqlalchemy import (
    String, Text, Integer, Boolean, ForeignKey,
    DateTime, Index
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import uuid

def utcnow():
    return datetime.utcnow()

class Tier(Base):
    __tablename__ = "tiers"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)
    display_name = mapped_column(String, nullable=False)

    max_resume_uploads = mapped_column(Integer, default=2)
    max_roasts_daily = mapped_column(Integer, default=2)

    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=utcnow)

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    google_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    auth_provider: Mapped[str] = mapped_column(String(50), default="email")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    resumes = relationship("Resume", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    jobs = relationship("Job", back_populates="user")

    tier_id = mapped_column(Integer, ForeignKey("tiers.id"), nullable=False)
    tier = relationship("Tier", lazy="joined")

class Resume(Base):
    __tablename__ = "resumes"

    resume_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(Text, nullable=False)
    thumbnail_key: Mapped[str] = mapped_column(Text, nullable=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    raw_resume_text: Mapped[str] = mapped_column(Text,nullable=True)
    file_size_bytes: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    is_deleted = mapped_column(Boolean, default=False, nullable=False)
    deleted_at = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="resumes")
    jobs = relationship("Job", back_populates="resume")

    __table_args__ = (Index("ix_resumes_user_id", "user_id"),)

class JobStatus(str, enum.Enum):
    pending = "PENDING"
    running = "RUNNING"
    success = "SUCCESS"
    failed = "FAILED"

class Job(Base):
    __tablename__ = "jobs"

    job_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.resume_id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # QUEUED, STARTED, SUCCESS, FAILURE
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str] = mapped_column(Text,nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    started_at: Mapped[datetime] = mapped_column(DateTime,nullable=True)
    finished_at: Mapped[datetime] = mapped_column(DateTime,nullable=True)

    resume = relationship("Resume", back_populates="jobs")
    user = relationship("User", back_populates="jobs")
    roast = relationship("Roast", back_populates="job", uselist=False)

    __table_args__ = (
        Index("ix_jobs_resume_id", "resume_id"),
        Index("ix_jobs_user_id", "user_id"),
    )

class Roast(Base):
    __tablename__ = "roasts"

    roast_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id: Mapped[str] = mapped_column(ForeignKey("jobs.job_id"), nullable=False, unique=True)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.resume_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    roast_text: Mapped[str] = mapped_column(Text, nullable=True)
    # model_name: Mapped[str] = mapped_column(String(100))
    # tokens_used: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    job = relationship("Job", back_populates="roast")
    resume = relationship("Resume")

    __table_args__ = (Index("ix_roasts_resume_id", "resume_id"),)

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime,default=utcnow)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    # ip_address: Mapped[str] = mapped_column(String(50))
    # user_agent: Mapped[str] = mapped_column(String(255))

    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index("ix_user_sessions_user_id", "user_id"),
        Index("ix_user_sessions_expires_at", "expires_at"),
    )
    
