# API schemas for request/response validation
from .user import (
    UserBase, UserCreate, UserUpdate, UserResponse, UserProfile, UserPreferences,
    UserLogin, UserLoginResponse, TokenResponse
)
from .fleet import (
    FleetUnitBase, FleetUnitCreate, FleetUnitUpdate, FleetUnitResponse,
    GeoLocation, RouteData, MaintenanceRecordBase, MaintenanceRecordCreate,
    MaintenanceRecordUpdate, MaintenanceRecordResponse
)
from .analytics import (
    WasteForecastBase, WasteForecastCreate, WasteForecastResponse,
    ForecastPoint, PredictionFactor, KPIMetricBase, KPIMetricCreate,
    KPIMetricResponse, AnalyticsReportBase, AnalyticsReportCreate,
    AnalyticsReportResponse
)
from .simulation import (
    SimulationScenarioBase, SimulationScenarioCreate, SimulationScenarioUpdate,
    SimulationScenarioResponse, SimulationParameters, SimulationConstraint,
    SimulationExecutionBase, SimulationExecutionCreate, SimulationExecutionResponse,
    SimulationLogBase, SimulationLogResponse, RouteOptimizationBase,
    RouteOptimizationResponse, Waypoint
)

__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserProfile", 
    "UserPreferences", "UserLogin", "UserLoginResponse", "TokenResponse",
    
    # Fleet schemas
    "FleetUnitBase", "FleetUnitCreate", "FleetUnitUpdate", "FleetUnitResponse",
    "GeoLocation", "RouteData", "MaintenanceRecordBase", "MaintenanceRecordCreate",
    "MaintenanceRecordUpdate", "MaintenanceRecordResponse",
    
    # Analytics schemas
    "WasteForecastBase", "WasteForecastCreate", "WasteForecastResponse",
    "ForecastPoint", "PredictionFactor", "KPIMetricBase", "KPIMetricCreate",
    "KPIMetricResponse", "AnalyticsReportBase", "AnalyticsReportCreate",
    "AnalyticsReportResponse",
    
    # Simulation schemas
    "SimulationScenarioBase", "SimulationScenarioCreate", "SimulationScenarioUpdate",
    "SimulationScenarioResponse", "SimulationParameters", "SimulationConstraint",
    "SimulationExecutionBase", "SimulationExecutionCreate", "SimulationExecutionResponse",
    "SimulationLogBase", "SimulationLogResponse", "RouteOptimizationBase",
    "RouteOptimizationResponse", "Waypoint",
]