"""
Verdant AI Integrated Dashboard - Main FastAPI Application
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.db_utils import check_database_connection, get_database_info
from app.middleware import LoggingMiddleware, ErrorHandlerMiddleware, RequestIDMiddleware
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Verdant AI Integrated Dashboard...")
    
    # Check database connection
    if await check_database_connection():
        logger.info("Database connection successful")
        # Initialize database tables
        await init_db()
        logger.info("Database initialized")
    else:
        logger.error("Database connection failed")
        raise Exception("Cannot connect to database")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await close_db()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Integrated dashboard for spatial-temporal waste management intelligence",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware - must be added before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Add custom middleware (order matters - they execute in reverse order)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")



@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Verdant AI Integrated Dashboard API",
        "version": "1.0.0",
        "environment": settings.environment,
        "docs": "/api/docs",
        "api_v1": "/api/v1"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    db_connected = await check_database_connection()
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "database": "connected" if db_connected else "disconnected",
        "environment": settings.environment,
        "version": "1.0.0"
    }


@app.get("/api/v1/database/info")
async def database_info():
    """Get database information - for development/debugging only"""
    try:
        info = await get_database_info()
        if info:
            return info
        else:
            raise HTTPException(status_code=500, detail="Could not retrieve database information")
    except Exception as e:
        logger.error(f"Error getting database info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )