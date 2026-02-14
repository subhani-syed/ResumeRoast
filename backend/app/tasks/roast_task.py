from app.celery_app import celery_app
from app.db import SessionLocal
from app import models
from app.services.llm import roast_resume
from app.services.redact import redact_resume_text
from datetime import datetime

@celery_app.task(bind=True,max_retries=3)
def process_roast_job(self, job_id: str):
    """
    Background task to generate a resume roast.
    """
    db = SessionLocal()
    job = None

    try:
        job = db.query(models.Job).filter_by(job_id=job_id).first()
        if not job:
            raise Exception(f"Job not found: {job_id}")
        
        job.status = models.JobStatus.running
        db.commit()

        resume = db.query(models.Resume).filter_by(resume_id=job.resume_id).first()

        if not resume:
            raise Exception(f"Resume not found: {job.resume_id}")

        if not resume.raw_resume_text:
            raise Exception("Resume text is empty")

        job.progress_percent = 20
        db.commit()

        redacted_text = redact_resume_text(resume.raw_resume_text)
        roast_text = roast_resume(redacted_text)

        job.progress_percent = 80
        db.commit()

        roast = (
            db.query(models.Roast)
            .filter_by(job_id=job.job_id)
            .first()
        )

        if not roast:
            raise Exception(f"Roast record not found for job_id={job.job_id}")

        roast.roast_text = roast_text
        roast.status = models.JobStatus.success
        roast.updated_at = datetime.utcnow()

        job.status = models.JobStatus.success
        job.progress_percent = 100
        db.commit()

        return {"status": "success"}

    except Exception as e:
        if job:
            job.status = models.JobStatus.failed
            job.error_message = str(e)
            db.commit()
        raise

    finally:
        db.close()
