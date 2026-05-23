"""
Simulation and scenario Pydantic schemas for API request/response validation
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, computed_field

from app.models.simulation import SimulationScenario, SimulationExecution, SimulationLog, RouteOptimization


class SimulationConstraint(BaseModel):
    """Constraint applied to simulation"""
    type: str = Field(..., description="Constraint type")
    parameter: str = Field(..., description="Parameter name")
    operator: str = Field(..., description="Constraint operator (eq, lt, gt, lte, gte)")
    value: Any = Field(..., description="Constraint value")
    description: Optional[str] = Field(None, description="Human-readable constraint description")

    @field_validator('operator')
    @classmethod
    def validate_operator(cls, v):
        """Validate constraint operator"""
        valid_operators = ['eq', 'lt', 'gt', 'lte', 'gte', 'in', 'not_in']
        if v not in valid_operators:
            raise ValueError(f'Operator must be one of: {", ".join(valid_operators)}')
        return v


class SimulationParameters(BaseModel):
    """Parameters for simulation execution"""
    operational_mode: str = Field(..., description="Operational mode (efficiency/carbon_neutral/cost_reduction)")
    spatial_radius: Decimal = Field(..., gt=0, description="Spatial radius in kilometers")
    fleet_capacity_load: Decimal = Field(..., ge=0, le=100, description="Fleet capacity load percentage")
    time_horizon: int = Field(..., gt=0, description="Time horizon in hours")
    constraints: Optional[List[SimulationConstraint]] = Field(None, description="Simulation constraints")
    optimization_weights: Optional[Dict[str, Decimal]] = Field(None, description="Optimization weights")
    weather_conditions: Optional[str] = Field(None, description="Weather conditions to consider")
    traffic_patterns: Optional[str] = Field(None, description="Traffic patterns to consider")

    @field_validator('operational_mode')
    @classmethod
    def validate_operational_mode(cls, v):
        """Validate operational mode"""
        valid_modes = ['efficiency', 'carbon_neutral', 'cost_reduction', 'balanced']
        if v not in valid_modes:
            raise ValueError(f'Operational mode must be one of: {", ".join(valid_modes)}')
        return v

    @field_validator('optimization_weights')
    @classmethod
    def validate_weights(cls, v):
        """Validate that optimization weights sum to 1.0"""
        if v is not None:
            total_weight = sum(v.values())
            if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
                raise ValueError('Optimization weights must sum to 1.0')
        return v


class SimulationScenarioBase(BaseModel):
    """Base simulation scenario schema"""
    name: str = Field(..., max_length=255, description="Scenario name")
    description: Optional[str] = Field(None, description="Scenario description")
    parameters: SimulationParameters = Field(..., description="Simulation parameters")
    tags: Optional[List[str]] = Field(None, description="Scenario tags for categorization")
    version: str = Field("1.0", max_length=20, description="Scenario version")
    is_public: bool = Field(False, description="Whether scenario is publicly accessible")


class SimulationScenarioCreate(SimulationScenarioBase):
    """Schema for creating a simulation scenario"""
    pass


class SimulationScenarioUpdate(BaseModel):
    """Schema for updating a simulation scenario"""
    name: Optional[str] = Field(None, max_length=255, description="Scenario name")
    description: Optional[str] = Field(None, description="Scenario description")
    parameters: Optional[SimulationParameters] = Field(None, description="Simulation parameters")
    tags: Optional[List[str]] = Field(None, description="Scenario tags for categorization")
    version: Optional[str] = Field(None, max_length=20, description="Scenario version")
    is_public: Optional[bool] = Field(None, description="Whether scenario is publicly accessible")


class SimulationScenarioResponse(SimulationScenarioBase):
    """Schema for simulation scenario response"""
    id: UUID = Field(..., description="Scenario unique identifier")
    created_by: UUID = Field(..., description="User who created the scenario")
    execution_count: int = Field(..., description="Number of times scenario has been executed")
    last_executed: Optional[datetime] = Field(None, description="Last execution timestamp")
    average_execution_time_ms: Optional[Decimal] = Field(None, description="Average execution time")
    success_rate: Optional[Decimal] = Field(None, description="Execution success rate percentage")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class Waypoint(BaseModel):
    """Waypoint in a route"""
    latitude: Decimal = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: Decimal = Field(..., ge=-180, le=180, description="Longitude coordinate")
    address: Optional[str] = Field(None, description="Human-readable address")
    stop_type: str = Field(..., description="Type of stop (pickup/delivery/checkpoint)")
    estimated_time_minutes: Optional[int] = Field(None, ge=0, description="Estimated time at this waypoint")
    priority: int = Field(1, ge=1, le=5, description="Waypoint priority")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional waypoint data")

    @field_validator('stop_type')
    @classmethod
    def validate_stop_type(cls, v):
        """Validate stop type"""
        valid_types = ['pickup', 'delivery', 'checkpoint', 'depot', 'maintenance']
        if v not in valid_types:
            raise ValueError(f'Stop type must be one of: {", ".join(valid_types)}')
        return v


class SimulationExecutionBase(BaseModel):
    """Base simulation execution schema"""
    scenario_id: UUID = Field(..., description="Scenario identifier")
    execution_name: Optional[str] = Field(None, max_length=255, description="Execution name")
    execution_parameters: Optional[Dict[str, Any]] = Field(None, description="Runtime parameters")


class SimulationExecutionCreate(SimulationExecutionBase):
    """Schema for creating a simulation execution"""
    pass


class SimulationResults(BaseModel):
    """Simulation execution results"""
    efficiency_score: Decimal = Field(..., ge=0, le=100, description="Efficiency score percentage")
    cost_savings: Decimal = Field(..., description="Cost savings amount")
    carbon_reduction: Decimal = Field(..., ge=0, description="Carbon reduction in kg CO2")
    fuel_savings_liters: Decimal = Field(..., ge=0, description="Fuel savings in liters")
    distance_reduction_km: Decimal = Field(..., ge=0, description="Distance reduction in kilometers")
    time_savings_minutes: Decimal = Field(..., ge=0, description="Time savings in minutes")
    routes_optimized: int = Field(..., ge=0, description="Number of routes optimized")
    waypoints_processed: int = Field(..., ge=0, description="Number of waypoints processed")


class SimulationExecutionResponse(SimulationExecutionBase):
    """Schema for simulation execution response"""
    id: UUID = Field(..., description="Execution unique identifier")
    status: str = Field(..., description="Execution status")
    started_at: datetime = Field(..., description="Execution start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Execution completion timestamp")
    execution_time_ms: Optional[int] = Field(None, description="Execution time in milliseconds")
    results: Optional[SimulationResults] = Field(None, description="Execution results")
    summary: Optional[Dict[str, Any]] = Field(None, description="Execution summary")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detailed error information")
    executed_by: UUID = Field(..., description="User who executed the simulation")
    progress_percent: Optional[Decimal] = Field(None, ge=0, le=100, description="Execution progress percentage")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def progress_percent(self) -> Optional[Decimal]:
        """Calculate progress based on status"""
        if self.status == 'completed':
            return Decimal('100.0')
        elif self.status in ['failed', 'cancelled']:
            return None
        elif self.status == 'running':
            return None  # Would need to be set externally
        return None


class SimulationLogBase(BaseModel):
    """Base simulation log schema"""
    level: str = Field(..., description="Log level (DEBUG/INFO/WARNING/ERROR)")
    message: str = Field(..., description="Log message")
    data: Optional[Dict[str, Any]] = Field(None, description="Structured log data")
    step_number: Optional[int] = Field(None, ge=0, description="Execution step number")
    step_name: Optional[str] = Field(None, max_length=100, description="Execution step name")
    memory_usage_mb: Optional[Decimal] = Field(None, ge=0, description="Memory usage in MB")
    cpu_usage_percent: Optional[Decimal] = Field(None, ge=0, le=100, description="CPU usage percentage")

    @field_validator('level')
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {", ".join(valid_levels)}')
        return v.upper()


class SimulationLogResponse(SimulationLogBase):
    """Schema for simulation log response"""
    id: UUID = Field(..., description="Log entry unique identifier")
    execution_id: UUID = Field(..., description="Execution identifier")
    timestamp: datetime = Field(..., description="Log timestamp")

    class Config:
        from_attributes = True


class RouteOptimizationBase(BaseModel):
    """Base route optimization schema"""
    route_name: str = Field(..., max_length=255, description="Route name")
    fleet_unit_id: Optional[UUID] = Field(None, description="Fleet unit identifier")
    original_route: Optional[Dict[str, Any]] = Field(None, description="Original route data")
    optimized_route: Dict[str, Any] = Field(..., description="Optimized route data")
    waypoints: List[Waypoint] = Field(..., min_items=2, description="Route waypoints")
    constraints: Optional[List[SimulationConstraint]] = Field(None, description="Route constraints")


class RouteOptimizationResponse(RouteOptimizationBase):
    """Schema for route optimization response"""
    id: UUID = Field(..., description="Route optimization unique identifier")
    execution_id: UUID = Field(..., description="Execution identifier")
    distance_reduction_km: Optional[Decimal] = Field(None, description="Distance reduction in kilometers")
    time_reduction_minutes: Optional[Decimal] = Field(None, description="Time reduction in minutes")
    fuel_savings_liters: Optional[Decimal] = Field(None, description="Fuel savings in liters")
    cost_savings: Optional[Decimal] = Field(None, description="Cost savings amount")
    efficiency_improvement_percent: Optional[Decimal] = Field(None, description="Efficiency improvement percentage")
    carbon_reduction_kg: Optional[Decimal] = Field(None, description="Carbon reduction in kg CO2")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def efficiency_improvement_percent(self) -> Optional[Decimal]:
        """Calculate efficiency improvement percentage"""
        if (self.distance_reduction_km and self.original_route and 
            'total_distance_km' in self.original_route):
            original_distance = self.original_route['total_distance_km']
            if original_distance > 0:
                return round((self.distance_reduction_km / original_distance) * 100, 2)
        return None


class SimulationStatistics(BaseModel):
    """Statistics for simulation scenarios and executions"""
    total_scenarios: int = Field(..., description="Total number of scenarios")
    public_scenarios: int = Field(..., description="Number of public scenarios")
    total_executions: int = Field(..., description="Total number of executions")
    successful_executions: int = Field(..., description="Number of successful executions")
    failed_executions: int = Field(..., description="Number of failed executions")
    average_execution_time_ms: Decimal = Field(..., description="Average execution time")
    total_cost_savings: Decimal = Field(..., description="Total cost savings achieved")
    total_carbon_reduction: Decimal = Field(..., description="Total carbon reduction achieved")
    most_used_scenario: Optional[str] = Field(None, description="Most frequently used scenario")


class SimulationDashboard(BaseModel):
    """Comprehensive simulation dashboard data"""
    statistics: SimulationStatistics = Field(..., description="Simulation statistics")
    recent_executions: List[SimulationExecutionResponse] = Field(..., description="Recent executions")
    popular_scenarios: List[SimulationScenarioResponse] = Field(..., description="Popular scenarios")
    top_optimizations: List[RouteOptimizationResponse] = Field(..., description="Top route optimizations")
    generated_at: datetime = Field(..., description="Dashboard generation timestamp")