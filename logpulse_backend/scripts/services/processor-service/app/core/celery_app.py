from celery import Celery

from .config import Settings

settings = Settings()

celery_app = Celery(
    "processor",
    broker=settings.broker_url,
    backend=settings.result_backend,
    include=["app.tasks"],
)

# Celery Production Settings
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    # Redis startup connection retries (Celery v6+ සඳහා)
    broker_connection_retry_on_startup=True,
    # Worker එක start වෙද්දී පමණක් tasks load කරගැනීමට (Circular import වැළැක්වීමට)
    imports=("app.tasks",),
)
