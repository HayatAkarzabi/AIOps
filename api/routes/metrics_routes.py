# Routes for system metrics.

from fastapi import APIRouter
from services.metrics_service import get_all_metrics

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    """
    GET /metrics
    Returns a list of simulated system metrics
    (e.g., CPU, memory, disk I/O, network).
    """
    metrics = get_all_metrics()
    return metrics
