# Schema for detected anomalies
from pydantic import BaseModel
from typing import Optional

class AnomalyResponse(BaseModel):
    """Represents an anomaly detected in a metric."""
    metric_name: str
    anomaly_score: float
    severity: str  # low, medium, high, critical
    timestamp: str
    description: Optional[str] = None
