from typing import Any, Dict, Optional

from app.core.celery_app import celery_app
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Initialize FastAPI app
app = FastAPI(title="Processor Service", version="1.0.0")

# 2. Configure CORS Middleware for React (Vite) / Next.js Frontend
origins = [
    "http://localhost:5173",  # 💡 Vite React Frontend (CORS Fix)
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # Next.js / React
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. Pydantic Schema for Input Log Validation
class LogIngestSchema(BaseModel):
    service: str
    level: str
    message: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# --- Endpoints ---


# Healthcheck Endpoint
@app.get("/healthz", status_code=status.HTTP_200_OK)
def healthz():
    return {"status": "ok"}


# Ingest Log Endpoint
@app.post("/api/v1/logs", status_code=status.HTTP_202_ACCEPTED)
async def ingest_log(payload: LogIngestSchema):
    task = celery_app.send_task(
        "process_log_entry",
        args=[payload.model_dump()],
    )

    return {
        "status": "queued",
        "task_id": task.id,
        "message": "Log accepted and pushed to Celery worker queue",
    }


# Fetch Logs Endpoint
@app.get("/api/v1/logs", status_code=status.HTTP_200_OK)
async def get_logs():
    return [
        {
            "id": 1,
            "timestamp": "2026-07-26 12:18:43",
            "level": "INFO",
            "service": "auth-service",
            "message": "User login succeeded for user@example.com",
        },
        {
            "id": 2,
            "timestamp": "2026-07-26 12:18:44",
            "level": "WARN",
            "service": "processor-service",
            "message": "Event batch delayed by 120ms due to queue throttling.",
        },
        {
            "id": 3,
            "timestamp": "2026-07-26 12:18:46",
            "level": "ERROR",
            "service": "auth-service",
            "message": "Failed JWT validation for token request from /api/v1/auth/refresh.",
        },
    ]
