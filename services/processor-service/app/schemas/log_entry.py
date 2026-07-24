from pydantic import BaseModel


class LogEntry(BaseModel):
    message: str
    timestamp: str
    level: str
