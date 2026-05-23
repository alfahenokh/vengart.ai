"""
API v1 Router Configuration
Aggregates all v1 API endpoints
"""
from fastapi import APIRouter

# Import routers
from .endpoints import health, dashboard

# Import additional routers (will be created in subsequent tasks)
# from .endpoints import auth, analytics, simulation, resources

api_router = APIRouter()

# Include health/status endpoints
api_router.include_router(health.router, tags=["health"])

# Include dashboard endpoints
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# Include routers when they are created
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
# api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
# api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
