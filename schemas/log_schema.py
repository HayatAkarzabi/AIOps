# Schema for log entries
from pydantic import BaseModel
from typing import Optional

class LogResponse(BaseModel):
    """Represents a single log entry."""
    message: str
    level: str  # INFO, WARN, ERROR, DEBUG
    source: Optional[str] = None
    timestamp: str
