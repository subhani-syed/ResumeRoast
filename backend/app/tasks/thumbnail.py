import io
from app.celery_app import celery_app
from app.db import SessionLocal
from app.models import Resume
from app.utils.s3 import s3_client
from sqlalchemy.orm import Session
from pdf2image import convert_from_bytes
from PIL import Image

@celery_app.task(bind=True)
def generate_thumbnail_task(self, resume_id: str):
    """
    Generate a thumbnail for a resume PDF.

    Steps:
        1. Fetch resume record from DB
        2. Download original file from S3
        3. Convert first page to image
        4. Resize and optimize
        5. Upload thumbnail to S3 in same folder
        6. Optionally update DB
    """

    db: Session = SessionLocal()

    try:
        resume = db.query(Resume).filter(
            Resume.resume_id == resume_id
        ).first()

        if not resume:
            return  # Or log error

        original_key = resume.s3_key
        base_path = original_key.rsplit("/", 1)[0]
        thumbnail_key = f"{base_path}/thumbnail.png"

        response = s3_client.get_object(
            Bucket=resume.s3_bucket,
            Key=original_key,
        )
        file_bytes = response["Body"].read()

        images = convert_from_bytes(file_bytes, first_page=1, last_page=1)
        image = images[0]

        image.thumbnail((400, 400))

        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        s3_client.upload_fileobj(
            buffer,
            resume.s3_bucket,
            thumbnail_key,
            ExtraArgs={"ContentType": "image/png"},
        )

        resume.thumbnail_key = thumbnail_key
        db.commit()

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=10)

    finally:
        db.close()
