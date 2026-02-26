from io import BytesIO
from uuid import uuid4
from datetime import datetime
from typing import List
from app.dependency import get_current_user, get_db
from app.schemas import ResumeResponse, ResumeDetailResponse, UploadInfoResponse
from app.models import User, Resume, Roast, Job, JobStatus
from app.utils.s3 import s3_client, generate_presigned_url
from app.tasks.roast_task import process_roast_job
from app.tasks.thumbnail import generate_thumbnail_task
from app.config import settings
from app.utils.text_extraction import extract_text_from_file
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

S3_BUCKET = settings.S3_BUCKET_NAME
MAX_RESUMES = settings.MAX_RESUMES_PER_USER

router = APIRouter(prefix="/resume", tags=["auth"])


@router.get("/", response_model=List[ResumeResponse])
def get_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all resumes uploaded by the authenticated user.

    This endpoint returns a list of resume metadata records belonging
    to the currently authenticated user, ordered by most recent first.

    Authentication:
        Requires a valid authenticated session.

    Returns:
        List[ResumeResponse]: A list of resume metadata including:
            - id: Unique resume identifier
            - original_filename: Name of the uploaded file
            - content_type: MIME type of the file
            - created_at: Upload timestamp
    """
    resumes = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .order_by(Resume.created_at.desc())
        .all()
    )
    response = []

    for resume in resumes:
        thumbnail_url = None

        if resume.thumbnail_key:
            thumbnail_url = generate_presigned_url(
                bucket=resume.s3_bucket,
                key=resume.thumbnail_key,
                expires_in=3600,
            )

        response.append({
            "id": resume.resume_id,
            "filename": resume.original_filename,
            "content_type": resume.mime_type,
            "created_at": resume.created_at,
            "thumbnail": str(thumbnail_url)
        })
    return response


@router.get("/upload", response_model=UploadInfoResponse)
def get_upload_information(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve resume upload quota information for the authenticated user.

    Returns:
        UploadInfoResponse:
            - resume_count: Total resumes uploaded by the user.
            - resume_upload_remaining: Remaining upload capacity.
    """
    resume_count = (
        db.query(func.count(Resume.resume_id))
        .filter(
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .scalar()
    )
    resume_remaining = max(0, MAX_RESUMES - resume_count)

    return {
        "resume_count": resume_count,
        "resume_upload_remaining": resume_remaining
    }


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve metadata and a temporary download URL for a specific resume.

    This endpoint returns detailed metadata for a resume owned by the
    authenticated user, along with a time-limited presigned S3 URL
    for secure file download.

    Path Parameters:
        resume_id (str): Unique identifier of the resume.

    Returns:
        ResumeDetailResponse: Resume metadata and secure download URL.
    """
    resume = (
        db.query(Resume)
        .filter(
            Resume.resume_id == resume_id,
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .first()
    )

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    download_url = generate_presigned_url(
        bucket=resume.s3_bucket,
        key=resume.s3_key,
        expires_in=settings.S3_PRESIGNED_URL_EXPIRE_SECONDS,
    )

    return {
        "resume_id": resume.resume_id,
        "filename": resume.original_filename,
        "mime_type": resume.mime_type,
        "file_size_bytes": resume.file_size_bytes,
        "created_at": resume.created_at,
        "download_url": download_url,
    }


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a resume owned by the authenticated user.

    Returns:
        dict: Confirmation message indicating successful soft deletion.
    """
    resume = db.query(Resume).filter_by(
        resume_id=resume_id,
        user_id=current_user.user_id,
        is_deleted=False
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.is_deleted = True
    resume.deleted_at = datetime.now()

    db.commit()

    return {"detail": "Resume deleted successfully"}


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a resume file for the authenticated user.

    Validates file type, enforces upload quota, stores the file in S3,
    and creates a database record for tracking.
    """
    resume_count = (
        db.query(func.count(Resume.resume_id))
        .filter(
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .scalar()
    )

    if resume_count >= MAX_RESUMES:
        raise HTTPException(
            status_code=400,
            detail=f"You can only upload {MAX_RESUMES} resumes."
        )

    if file.content_type not in [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    resume_id = str(uuid4())

    file.file.seek(0)
    file_bytes = file.file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    file_size_bytes = len(file_bytes)
    raw_text = extract_text_from_file(file_bytes, file.content_type)

    s3_key_path = f"users/{current_user.user_id}/resumes/{resume_id}"
    resume_key = f"{s3_key_path}/resume"
    s3_key = str(resume_key)

    try:
        s3_client.upload_fileobj(
            BytesIO(file_bytes),
            S3_BUCKET,
            resume_key,
            ExtraArgs={
                "ContentType": file.content_type,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload to S3 : {e}")

    resume = Resume(
        resume_id=resume_id,
        user_id=current_user.user_id,
        s3_bucket=S3_BUCKET,
        s3_key=s3_key,
        original_filename=file.filename,
        raw_resume_text=raw_text,
        file_size_bytes=file_size_bytes,
        mime_type=file.content_type,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    generate_thumbnail_task.delay(resume.resume_id)

    return {
        "resume_id": resume.resume_id,
        "filename": resume.original_filename,
    }


@router.get("/{resume_id}/roast")
def get_latest_roast(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the latest successful roast for a given resume.
    """
    resume = (
        db.query(Resume)
        .filter(
            Resume.resume_id == resume_id,
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    latest_roast = (
        db.query(Roast)
        .filter(
            Roast.resume_id == resume_id,
            Roast.status == "SUCCESS"
        )
        .order_by(desc(Roast.created_at))
        .first()
    )
    if not latest_roast:
        raise HTTPException(status_code=200, detail="No roast found")
    return {
        "job_id": latest_roast.job_id,
        "resume_id": latest_roast.resume_id,
        "roast_text": latest_roast.roast_text,
        "created_at": latest_roast.created_at,
    }


@router.post("/{resume_id}/roast")
def create_resume_roast(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Initiate an asynchronous roast generation job for a resume.
    """
    pending = (
        db.query(Roast)
        .filter(Roast.resume_id == resume_id)
        .filter(Roast.status.in_(["pending", "processing"]))
        .first()
    )
    if pending:
        raise HTTPException(
            status_code=409, detail="Roast already in progress")

    resume = (
        db.query(Resume)
        .filter(
            Resume.resume_id == resume_id,
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False
        )
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job_id = uuid4().hex

    job = Job(
        job_id=job_id,
        resume_id=resume_id,
        user_id=current_user.user_id,
        status=JobStatus.pending,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    roast = Roast(
        job_id=job_id,
        resume_id=resume_id,
        status=JobStatus.pending
    )
    db.add(roast)
    db.commit()
    db.refresh(roast)

    process_roast_job.delay(job.job_id)

    return {
        "job_id": roast.job_id,
        "status": roast.status,
        "message": "Roast started",
    }


@router.get("/{resume_id}/roast/{job_id}")
def get_roast(
    resume_id: str,
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific roast for a given resume.
    """
    resume = (
        db.query(Resume)
        .filter(
            Resume.resume_id == resume_id,
            Resume.user_id == current_user.user_id,
            Resume.is_deleted == False

        )
        .first()
    )

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    roast = (
        db.query(Roast)
        .filter(
            Roast.job_id == job_id,
            Roast.resume_id == resume_id
        )
        .first()
    )

    if not roast:
        raise HTTPException(status_code=404, detail="Roast not found")

    return {
        "resume_id": roast.resume_id,
        "status": roast.status,
        "roast_text": roast.roast_text,
        "created_at": roast.created_at,
    }
