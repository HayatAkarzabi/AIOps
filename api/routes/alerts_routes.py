# Routes for alerts.

from fastapi import APIRouter
from services.alert_service import get_all_alerts

router = APIRouter()

@router.get("/alerts")
async def get_alerts():
    """
    GET /alerts
    Returns a list of simulated alerts triggered
    by monitoring rules.
    """
    alerts = get_all_alerts()
    return alerts
