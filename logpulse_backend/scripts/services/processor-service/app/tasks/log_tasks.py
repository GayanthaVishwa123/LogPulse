from datetime import datetime, timezone
from typing import Any, Dict

from app.core.celery_app import celery_app


@celery_app.task(name="process_log_entry")
def process_log_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Background Task: Normalizes incoming logs and prepares them for storage/streaming.
    """
    # 1. Normalize Log Level
    raw_level = str(entry.get("level", "INFO")).upper()
    level_mappings = {
        "WARNING": "WARN",
        "CRITICAL": "ERROR",
        "FATAL": "ERROR",
        "INFORMATION": "INFO",
    }
    normalized_level = level_mappings.get(raw_level, raw_level)

    # 2. Standardize Timestamp (UTC)
    timestamp = entry.get("timestamp")
    if not timestamp:
        timestamp = datetime.now(timezone.utc).isoformat()

    # 3. Construct Normalized Log Payload
    normalized_entry = {
        "service": str(entry.get("service", "unknown-service")).lower().strip(),
        "level": normalized_level,
        "message": str(entry.get("message", "")).strip(),
        "timestamp": timestamp,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "metadata": entry.get("metadata", {}),
    }

    # Worker Log output
    print(
        f"[Celery Worker] Processed log: {normalized_entry['service']} | {normalized_entry['level']}"
    )

    return {"processed": True, "entry": normalized_entry}
