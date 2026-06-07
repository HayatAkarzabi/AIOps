# Schema for system metrics
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MetricResponse(BaseModel):
    """Represents a single system metric data point."""
    name: str
    value: float
    unit: Optional[str] = None
    timestamp: str
    source: Optional[str] = None
