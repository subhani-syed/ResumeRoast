from app.celery_app import celery_app
from app.db import SessionLocal
from app import models
from app.services.llm import generate_roast
from datetime import datetime

@celery_app.task(bind=True)
def process_roast_job(self, job_id: str):
    db = SessionLocal()

    try:
        job = db.query(models.Job).filter_by(job_id=job_id).first()
        job.status = "STARTED"
        db.commit()

        resume = db.query(models.Resume).filter_by(resume_id=job.resume_id).first()

        job.progress_percent = 20
        db.commit()

        roast_text = generate_roast(resume)

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
        roast.status = "SUCCESS"
        roast.updated_at = datetime.utcnow()

        # roast = models.Roast(
        #     job_id=job.job_id,
        #     resume_id=resume.resume_id,
        #     roast_text=roast_text,
        #     status = "SUCCESS"
        # )
        # db.add(roast)

        job.status = "SUCCESS"
        job.progress_percent = 100
        db.commit()

        return {"status": "success"}

    except Exception as e:
        job.status = "FAILURE"
        job.error_message = str(e)
        db.commit()
        raise

    finally:
        db.close()
