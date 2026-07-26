from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry(BaseModel):
    service: str = Field(
        ...,
        examples=["auth-service"],
        description="Name of the microservice sending the log",
    )
    level: LogLevel = Field(default=LogLevel.INFO, description="Log severity level")
    message: str = Field(
        ...,
        examples=["User authentication failed"],
        description="Main log message content",
    )
    timestamp: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="ISO 8601 UTC timestamp (auto-generated if omitted)",
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        examples=[{"user_id": 42, "endpoint": "/api/v1/login"}],
        description="Optional contextual payload",
    )

    class Config:
        # JSON Schema එක Docs (Swagger UI) වල ලස්සනට පෙන්වීමට
        json_schema_extra = {
            "example": {
                "service": "auth-service",
                "level": "ERROR",
                "message": "Failed JWT validation for token",
                "timestamp": "2026-07-26T06:28:51.422Z",
                "metadata": {"ip": "192.168.1.50", "attempt": 3},
            }
        }
