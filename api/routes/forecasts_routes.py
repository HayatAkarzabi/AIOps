# Routes for forecast predictions.

from fastapi import APIRouter
from services.forecasting_service import get_all_forecasts

router = APIRouter()

@router.get("/forecasts")
async def get_forecasts():
    """
    GET /forecasts
    Returns a list of simulated forecast predictions
    for key system metrics.
    """
    forecasts = get_all_forecasts()
    return forecasts
