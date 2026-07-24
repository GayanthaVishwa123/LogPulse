from .core.celery_app import celery_app


@celery_app.task
def process_log_entry(entry: dict) -> dict:
    # Placeholder for log normalization and enrichment logic
    return {"processed": True, "entry": entry}
