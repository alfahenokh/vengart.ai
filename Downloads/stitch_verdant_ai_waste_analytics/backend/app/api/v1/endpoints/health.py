"""
Health and Status Endpoints
Provides system health checks and status information
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def api_health_check():
    """API v1 health check endpoint"""
    # Import here to avoid module-level database connection
    from app.core.db_utils import check_database_connection
    
    db_connected = await check_database_connection()
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "api_version": "v1",
        "database": "connected" if db_connected else "disconnected"
    }


@router.get("/status")
async def api_status():
    """Detailed API status information"""
    # Import here to avoid module-level database connection
    from app.core.db_utils import check_database_connection
    
    db_connected = await check_database_connection()
    
    return {
        "api_version": "v1",
        "services": {
            "database": "operational" if db_connected else "unavailable",
            "authentication": "operational",
            "websocket": "operational"
        },
        "endpoints": {
            "dashboard": "/api/v1/dashboard",
            "analytics": "/api/v1/analytics",
            "simulation": "/api/v1/simulation",
            "resources": "/api/v1/resources"
        }
    }
