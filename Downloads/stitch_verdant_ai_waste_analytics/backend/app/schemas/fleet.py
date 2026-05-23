"""
Fleet management Pydantic schemas for API request/response validation
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, computed_field

from app.models.fleet import FleetUnitType, FleetUnitStatus, CapacityUnit


class GeoLocation(BaseModel):
    """Geographic location information"""
    latitude: Decimal = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: Decimal = Field(..., ge=-180, le=180, description="Longitude coordinate")
    address: Optional[str] = Field(None, max_length=255, description="Human-readable address")
    zone: Optional[str] = Field(None, max_length=100, description="Operational zone identifier")

    @field_validator('latitude', 'longitude')
    @classmethod
    def validate_coordinates(cls, v):
        """Validate coordinate precision"""
        if v is not None and v.as_tuple().exponent < -8:
            raise ValueError('Coordinate precision cannot exceed 8 decimal places')
        return v


class RouteData(BaseModel):
    """Route assignment data"""
    route_id: str = Field(..., description="Unique route identifier")
    route_name: str = Field(..., description="Human-readable route name")
    waypoints: List[GeoLocation] = Field(..., description="List of waypoints in the route")
    estimated_duration_minutes: Optional[int] = Field(None, ge=0, description="Estimated route duration")
    estimated_distance_km: Optional[Decimal] = Field(None, ge=0, description="Estimated route distance")
    priority: int = Field(1, ge=1, le=5, description="Route priority (1=lowest, 5=highest)")
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start time")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end time")


class FleetUnitBase(BaseModel):
    """Base fleet unit schema with common fields"""
    identifier: str = Field(..., min_length=1, max_length=20, description="Unique fleet unit identifier")
    type: FleetUnitType = Field(..., description="Type of fleet unit")
    status: FleetUnitStatus = Field(FleetUnitStatus.IDLE, description="Current operational status")
    location: Optional[GeoLocation] = Field(None, description="Current location")
    maximum_capacity: Decimal = Field(..., gt=0, description="Maximum capacity of the unit")
    capacity_unit: CapacityUnit = Field(CapacityUnit.TONS, description="Unit of capacity measurement")
    assigned_route: Optional[RouteData] = Field(None, description="Currently assigned route")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @field_validator('identifier')
    @classmethod
    def validate_identifier(cls, v):
        """Validate identifier format"""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Identifier must contain only letters, numbers, hyphens, and underscores')
        return v.upper()


class FleetUnitCreate(FleetUnitBase):
    """Schema for creating a new fleet unit"""
    current_capacity: Decimal = Field(0, ge=0, description="Current capacity load")

    @field_validator('current_capacity')
    @classmethod
    def validate_current_capacity(cls, v, info):
        """Validate that current capacity doesn't exceed maximum"""
        if 'maximum_capacity' in info.data and v > info.data['maximum_capacity']:
            raise ValueError('Current capacity cannot exceed maximum capacity')
        return v


class FleetUnitUpdate(BaseModel):
    """Schema for updating fleet unit information"""
    type: Optional[FleetUnitType] = Field(None, description="Type of fleet unit")
    status: Optional[FleetUnitStatus] = Field(None, description="Current operational status")
    location: Optional[GeoLocation] = Field(None, description="Current location")
    current_capacity: Optional[Decimal] = Field(None, ge=0, description="Current capacity load")
    maximum_capacity: Optional[Decimal] = Field(None, gt=0, description="Maximum capacity of the unit")
    capacity_unit: Optional[CapacityUnit] = Field(None, description="Unit of capacity measurement")
    assigned_route: Optional[RouteData] = Field(None, description="Currently assigned route")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @field_validator('current_capacity')
    @classmethod
    def validate_current_capacity(cls, v, info):
        """Validate that current capacity doesn't exceed maximum if both are provided"""
        if v is not None and 'maximum_capacity' in info.data and info.data['maximum_capacity'] is not None:
            if v > info.data['maximum_capacity']:
                raise ValueError('Current capacity cannot exceed maximum capacity')
        return v


class FleetUnitResponse(FleetUnitBase):
    """Schema for fleet unit response data"""
    id: UUID = Field(..., description="Fleet unit's unique identifier")
    current_capacity: Decimal = Field(..., description="Current capacity load")
    capacity_utilization_percent: Optional[Decimal] = Field(None, description="Capacity utilization percentage")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    last_update: datetime = Field(..., description="Last status update timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def capacity_utilization_percent(self) -> Optional[Decimal]:
        """Calculate capacity utilization percentage"""
        if self.maximum_capacity > 0:
            return round((self.current_capacity / self.maximum_capacity) * 100, 2)
        return None


class MaintenanceRecordBase(BaseModel):
    """Base maintenance record schema"""
    maintenance_type: str = Field(..., max_length=100, description="Type of maintenance")
    description: Optional[str] = Field(None, max_length=500, description="Maintenance description")
    scheduled_date: datetime = Field(..., description="Scheduled maintenance date")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="Estimated maintenance cost")
    estimated_duration_hours: Optional[Decimal] = Field(None, ge=0, description="Estimated duration in hours")


class MaintenanceRecordCreate(MaintenanceRecordBase):
    """Schema for creating a maintenance record"""
    fleet_unit_id: UUID = Field(..., description="Fleet unit identifier")


class MaintenanceRecordUpdate(BaseModel):
    """Schema for updating maintenance record"""
    maintenance_type: Optional[str] = Field(None, max_length=100, description="Type of maintenance")
    description: Optional[str] = Field(None, max_length=500, description="Maintenance description")
    scheduled_date: Optional[datetime] = Field(None, description="Scheduled maintenance date")
    completed_date: Optional[datetime] = Field(None, description="Actual completion date")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="Estimated maintenance cost")
    actual_cost: Optional[Decimal] = Field(None, ge=0, description="Actual maintenance cost")
    estimated_duration_hours: Optional[Decimal] = Field(None, ge=0, description="Estimated duration in hours")
    actual_duration_hours: Optional[Decimal] = Field(None, ge=0, description="Actual duration in hours")
    status: Optional[str] = Field(None, description="Maintenance status")


class MaintenanceRecordResponse(MaintenanceRecordBase):
    """Schema for maintenance record response"""
    id: UUID = Field(..., description="Maintenance record unique identifier")
    fleet_unit_id: UUID = Field(..., description="Fleet unit identifier")
    completed_date: Optional[datetime] = Field(None, description="Actual completion date")
    actual_cost: Optional[Decimal] = Field(None, description="Actual maintenance cost")
    actual_duration_hours: Optional[Decimal] = Field(None, description="Actual duration in hours")
    status: str = Field(..., description="Maintenance status")
    cost_variance: Optional[Decimal] = Field(None, description="Cost variance (actual - estimated)")
    duration_variance: Optional[Decimal] = Field(None, description="Duration variance in hours")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def cost_variance(self) -> Optional[Decimal]:
        """Calculate cost variance"""
        if self.actual_cost is not None and self.estimated_cost is not None:
            return self.actual_cost - self.estimated_cost
        return None

    @computed_field
    @property
    def duration_variance(self) -> Optional[Decimal]:
        """Calculate duration variance"""
        if self.actual_duration_hours is not None and self.estimated_duration_hours is not None:
            return self.actual_duration_hours - self.estimated_duration_hours
        return None


class FleetStatusSummary(BaseModel):
    """Summary of fleet status across all units"""
    total_units: int = Field(..., description="Total number of fleet units")
    active_units: int = Field(..., description="Number of active units")
    idle_units: int = Field(..., description="Number of idle units")
    maintenance_units: int = Field(..., description="Number of units in maintenance")
    offline_units: int = Field(..., description="Number of offline units")
    total_capacity: Decimal = Field(..., description="Total fleet capacity")
    utilized_capacity: Decimal = Field(..., description="Currently utilized capacity")
    utilization_percent: Decimal = Field(..., description="Overall capacity utilization percentage")
    units_with_routes: int = Field(..., description="Number of units with assigned routes")


class FleetUnitList(BaseModel):
    """Schema for paginated fleet unit list response"""
    units: List[FleetUnitResponse] = Field(..., description="List of fleet units")
    summary: FleetStatusSummary = Field(..., description="Fleet status summary")
    total: int = Field(..., description="Total number of units")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of units per page")
    pages: int = Field(..., description="Total number of pages")