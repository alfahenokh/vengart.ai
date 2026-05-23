# Database models
from .user import User, UserRole
from .fleet import FleetUnit, FleetUnitType, FleetUnitStatus, CapacityUnit, MaintenanceRecord
from .analytics import WasteForecast, KPIMetric, AnalyticsReport
from .simulation import SimulationScenario, SimulationExecution, SimulationLog, RouteOptimization

# Import Base for external use
from app.core.database import Base

__all__ = [
    # Base
    "Base",
    
    # User models
    "User",
    "UserRole",
    
    # Fleet models
    "FleetUnit",
    "FleetUnitType", 
    "FleetUnitStatus",
    "CapacityUnit",
    "MaintenanceRecord",
    
    # Analytics models
    "WasteForecast",
    "KPIMetric",
    "AnalyticsReport",
    
    # Simulation models
    "SimulationScenario",
    "SimulationExecution", 
    "SimulationLog",
    "RouteOptimization",
]