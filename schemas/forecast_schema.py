# Schema for forecast predictions
from pydantic import BaseModel
from typing import Optional

class ForecastResponse(BaseModel):
    """Represents a forecasted value for a metric."""
    metric_name: str
    forecasted_value: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    timestamp: str
