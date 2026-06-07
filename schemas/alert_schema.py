# Schema for alerts
from pydantic import BaseModel
from typing import Optional

class AlertResponse(BaseModel):
    """Represents an alert fired by a monitoring rule."""
    rule_name: str
    severity: str  # low, medium, high, critical
    status: str  # active, acknowledged, resolved
    message: str
    timestamp: str
