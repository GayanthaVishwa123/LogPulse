from celery import Celery

from .config import Settings

settings = Settings()

# 1. Initialize Celery App
celery_app = Celery(
    "processor",
    broker=settings.broker_url,
    backend=settings.result_backend,
)

# 2. Celery Configurations
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    imports=("app.tasks.log_tasks",),
)

# 3. Explicitly import task file so the @celery_app.task decorator executes
import app.tasks.log_tasks
