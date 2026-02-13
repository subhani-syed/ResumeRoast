from app.dependency import get_db
from app.schemas import ResumeJobRead, ResumeRoastRequest
from app.models import User,Resume, Roast, Job, JobStatus
from app.dependency import get_current_user,get_db
from uuid import uuid4
from app.exceptions import PermissionDenied
from app.utils.s3 import s3_client,generate_presigned_url
from app.tasks.roast_task import process_roast_job
from app.config import settings
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func

S3_BUCKET = settings.S3_BUCKET_NAME
MAX_RESUMES = settings.MAX_RESUMES_PER_USER

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/resume", tags=["auth"])

@router.get("/upload")
def get_upload_information(
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)
    ):

    resume_count = (
        db.query(func.count(Resume.resume_id))
        .filter(Resume.user_id == current_user.user_id)
        .scalar()
    )

    return {
        "resume_count": resume_count,
        "resume_upload_remaining": (MAX_RESUMES - resume_count)
    }

@router.post("/upload")
def upload_resume(
    file:UploadFile = File(...),
    current_user:User=Depends(get_current_user),
    db:Session = Depends(get_db)
    ):

    resume_count = (
        db.query(func.count(Resume.resume_id))
        .filter(Resume.user_id == current_user.user_id)
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

    resume_id = str(uuid.uuid4())
    s3_key_path = UPLOAD_DIR / f"users/{current_user.user_id}/resumes/{resume_id}/{file.filename}"
    # s3_key_path = f"users/{current_user.user_id}/resumes/{resume_id}/{file.filename}"
    s3_key = str(s3_key_path)
    # Find the file size in bytes

    try:
        # s3_client.upload_fileobj(
        #     file.file,
        #     S3_BUCKET,
        #     s3_key,
        #     ExtraArgs={
        #         "ContentType": file.content_type,
        #     },
        # )
        s3_key_path.parent.mkdir(parents=True, exist_ok=True)
        with open(s3_key,"wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3 : {e}")

    file_size_bytes = s3_key_path.stat().st_size
    # file_size_bytes = 100
    resume = Resume(
        resume_id=resume_id,
        user_id=current_user.user_id,
        s3_bucket=S3_BUCKET,
        s3_key=s3_key,
        original_filename=file.filename,
        file_size_bytes=file_size_bytes,
        mime_type=file.content_type,
    )

    # Add Thumbnail task to the queue

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.resume_id,
        # "s3_bucket": resume.s3_bucket,
        "s3_key": resume.s3_key,
        "filename": resume.original_filename,
    }

@router.get("/{resume_id}")
def get_resume(
    resume_id:str,
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)
    ):
    
    resume = (
        db.query(Resume)
        .filter(Resume.resume_id == resume_id)
        .first()
    )

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")

    # Generate secure download URL
    # download_url = generate_presigned_url(
    #     bucket=resume.s3_bucket,
    #     key=resume.s3_key,
    #     expires_in=300,  # 5 minutes
    # )

    return {
        "resume_id": resume.resume_id,
        "filename": resume.original_filename,
        "mime_type": resume.mime_type,
        "file_size_bytes": resume.file_size_bytes,
        "created_at": resume.created_at,
        "file_location":resume.s3_key,
        # "download_url": download_url,
    }

@router.get("/")
def get_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    # Returns the Resumes info of the User
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )
    
    return [
        {
            "id": r.resume_id,
            "original_filename": r.original_filename,
            "content_type": r.mime_type,
            "created_at": r.created_at,
        }
        for r in resumes
    ]

@router.get("/{resume_id}/roast")
def get_latest_roast(
    resume_id:str,
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
    ):

    resume = (
        db.query(Resume)
        .filter(Resume.resume_id == resume_id)
        .filter(Resume.user_id == current_user.user_id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    latest_roast = (
        db.query(Roast)
        .filter(Roast.resume_id == resume_id)
        .filter(Roast.status == "SUCCESS")
        .first()
    )
    if not latest_roast:
        return {
            "message": "No Roasts Found"
        }
    
    return {
        "roast_id": latest_roast.roast_id,
        "resume_id": latest_roast.resume_id,
        "roast_text": latest_roast.roast_text,
        "created_at": latest_roast.created_at,
    }

@router.get("/{resume_id}/roast/{roast_id}")
def get_roast(
    resume_id:str,
    roast_id:str,
    current_user:User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    # Gets the Roast fo the specific Resume
    resume = (
        db.query(Resume)
        .filter(Resume.resume_id == resume_id)
        .filter(Resume.user_id == current_user.user_id)
        .first()
    )

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    roast = (
        db.query(Roast)
        .filter(Roast.job_id == roast_id)
        .filter(Roast.resume_id == resume_id)
        .first()
    )

    if not roast:
        raise HTTPException(status_code=404, detail="Roast not found")

    return {
        "roast_id": roast.roast_id,
        "resume_id": roast.resume_id,
        "roast_text": roast.roast_text,
        "created_at": roast.created_at,
    }

@router.post("/{resume_id}/roast")
def create_resume_roast(
    resume_id: str,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    pending = (
        db.query(Roast)
        .filter(Roast.resume_id == resume_id)
        .filter(Roast.status.in_(["pending", "processing"]))
        .first()
    )
    if pending:
        raise HTTPException(status_code=409, detail="Roast already in progress")

    resume = (
        db.query(Resume)
        .filter(Resume.resume_id == resume_id)
        .filter(Resume.user_id == current_user.user_id)
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job_id = uuid4().hex

    job = Job(
        job_id=job_id,
        resume_id = resume_id,
        user_id=current_user.user_id,
        status=JobStatus.pending,
    )
    db.add(job)
    db.commit()
    db.refresh(job)


    roast = Roast(
        job_id = job_id,
        resume_id = resume_id,
        status = JobStatus.pending
    )
    db.add(roast)
    db.commit()
    db.refresh(roast)

    process_roast_job.delay(job.job_id)

    return {
        "roast_id": roast.job_id,
        "status": roast.status,
        "message": "Roast started",
    }
