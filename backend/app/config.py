from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    S3_BUCKET_NAME: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str

    MAX_RESUMES_PER_USER: int = 5

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
