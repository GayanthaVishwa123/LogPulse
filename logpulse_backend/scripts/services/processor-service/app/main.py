from typing import Any, Dict, List, Optional

from app.core.celery_app import celery_app
from app.database import get_db  # 💡 DB Session Dependency එක
from app.models import LogModel  # 💡 Log Database Model එක
from fastapi import Depends, FastAPI, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# 1. Initialize FastAPI app
app = FastAPI(title="Processor Service", version="1.0.0")

# 2. Configure CORS Middleware for Frontend
origins = [
    "http://localhost:5173",  # Vite React Frontend
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


# 3. Pydantic Schemas for Request & Response
class LogIngestSchema(BaseModel):
    service: str
    level: str
    message: str
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class LogResponseSchema(BaseModel):
    id: int
    service: str
    level: str
    message: str
    created_at: Any
    metadata_info: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# --- Endpoints ---


# Healthcheck Endpoint
@app.get("/healthz", status_code=status.HTTP_200_OK)
def healthz():
    return {"status": "ok"}


# Ingest Log Endpoint (Push to Celery Queue)
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


# Fetch Real Logs Endpoint (Read from Postgres DB)
@app.get(
    "/api/v1/logs",
    status_code=status.HTTP_200_OK,
    response_model=List[LogResponseSchema],
)
async def get_logs(
    limit: int = Query(default=100, le=500), db: Session = Depends(get_db)
):
    # DB එකෙන් අලුත්ම logs 100 Fetch කිරීම
    logs = db.query(LogModel).order_by(LogModel.id.desc()).limit(limit).all()
    return logs
