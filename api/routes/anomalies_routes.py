# Routes for anomaly detection results.

from fastapi import APIRouter
from services.anomaly_service import get_all_anomalies

router = APIRouter()

@router.get("/anomalies")
async def get_anomalies():
    """
    GET /anomalies
    Returns a list of simulated anomalies detected
    in the system metrics.
    """
    anomalies = get_all_anomalies()
    return anomalies
