"""
Fleet management models
"""
from sqlalchemy import Column, String, DateTime, Numeric, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class FleetUnitType(str, enum.Enum):
    """Fleet unit type enumeration"""
    COLLECTION = "collection"
    TRANSPORT = "transport"
    PROCESSING = "processing"


class FleetUnitStatus(str, enum.Enum):
    """Fleet unit status enumeration"""
    ACTIVE = "active"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class CapacityUnit(str, enum.Enum):
    """Capacity unit enumeration"""
    TONS = "tons"
    CUBIC_METERS = "cubic_meters"


class FleetUnit(Base):
    """Fleet unit model for tracking vehicles and equipment"""
    __tablename__ = "fleet_units"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(String(20), unique=True, nullable=False, index=True)
    type = Column(SQLEnum(FleetUnitType), nullable=False)
    status = Column(SQLEnum(FleetUnitStatus), nullable=False, default=FleetUnitStatus.IDLE)
    
    # Location data
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    address = Column(String(255), nullable=True)
    zone = Column(String(100), nullable=True)
    
    # Capacity information
    current_capacity = Column(Numeric(10, 2), nullable=False, default=0)
    maximum_capacity = Column(Numeric(10, 2), nullable=False)
    capacity_unit = Column(SQLEnum(CapacityUnit), nullable=False, default=CapacityUnit.TONS)
    
    # Route assignment (stored as JSON for flexibility)
    assigned_route = Column(JSON, nullable=True)
    
    # Additional metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_update = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<FleetUnit(identifier='{self.identifier}', type='{self.type}', status='{self.status}')>"


class MaintenanceRecord(Base):
    """Maintenance record for fleet units"""
    __tablename__ = "maintenance_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fleet_unit_id = Column(UUID(as_uuid=True), ForeignKey("fleet_units.id"), nullable=False)
    
    # Maintenance details
    maintenance_type = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    
    # Cost and duration
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    actual_cost = Column(Numeric(10, 2), nullable=True)
    estimated_duration_hours = Column(Numeric(5, 2), nullable=True)
    actual_duration_hours = Column(Numeric(5, 2), nullable=True)
    
    # Status
    status = Column(String(50), nullable=False, default="scheduled")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    fleet_unit = relationship("FleetUnit", backref="maintenance_records")
    
    def __repr__(self):
        return f"<MaintenanceRecord(fleet_unit_id='{self.fleet_unit_id}', type='{self.maintenance_type}')>"