from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    S3_BUCKET_NAME: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str

    MAX_RESUMES_PER_USER: int = 5
    S3_PRESIGNED_URL_EXPIRE_SECONDS:int = 300

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    GROQ_API_KEY:str
    LLM_MODEL:str

    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str
    GOOGLE_REDIRECT_URI:str

    FRONTEND_CALLBACK_URL:str

    SECRET_KEY:str

    REDIS_URL:str
    TTL_SECONDS:int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
