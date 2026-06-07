# Main entry point for the AIOps FastAPI application.
# Run with: uvicorn api.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules
from api.routes.health_routes import router as health_router
from api.routes.metrics_routes import router as metrics_router
from api.routes.logs_routes import router as logs_router
from api.routes.anomalies_routes import router as anomalies_router
from api.routes.forecasts_routes import router as forecasts_router
from api.routes.alerts_routes import router as alerts_router

# Create the FastAPI app instance
app = FastAPI(
    title="AIOps Platform API",
    description="Smart Operational Intelligence Platform - REST API",
    version="1.0.0",
)

# Allow requests from the frontend (different port / domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route routers under the root prefix
app.include_router(health_router)
app.include_router(metrics_router)
app.include_router(logs_router)
app.include_router(anomalies_router)
app.include_router(forecasts_router)
app.include_router(alerts_router)


# Optional: root welcome message
@app.get("/")
async def root():
    return {
        "message": "Welcome to the AIOps Platform API",
        "docs": "/docs",
        "endpoints": ["/health", "/metrics", "/logs", "/anomalies", "/forecasts", "/alerts"],
    }
