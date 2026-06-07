# Routes for log entries.

from fastapi import APIRouter
from services.logs_service import get_all_logs

router = APIRouter()

@router.get("/logs")
async def get_logs():
    """
    GET /logs
    Returns a list of simulated log entries
    from various system services.
    """
    logs = get_all_logs()
    return logs
