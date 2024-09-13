import os
from dotenv import load_dotenv


load_dotenv(os.getenv("ENV_FILE", ".env"))


class Config:
    """database url"""

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
