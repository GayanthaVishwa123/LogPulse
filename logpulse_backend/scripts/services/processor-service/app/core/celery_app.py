from celery import Celery

from .config import Settings

settings = Settings()

celery_app = Celery(
    "processor",
    broker=settings.broker_url,
    backend=settings.result_backend,
)
