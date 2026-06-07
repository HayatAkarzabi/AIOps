# Health check endpoint.
# Returns the current status of the API service.

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def get_health():
    """
    GET /health
    Returns a simple health status to confirm the API is running.
    """
    return {
        "status": "healthy",
        "service": "AIOps Platform",
        "version": "1.0.0",
    }
