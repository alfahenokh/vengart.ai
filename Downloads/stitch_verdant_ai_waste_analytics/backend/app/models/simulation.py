"""
Simulation and scenario models
"""
from sqlalchemy import Column, String, DateTime, Numeric, JSON, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class SimulationScenario(Base):
    """Simulation scenario configuration"""
    __tablename__ = "simulation_scenarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Scenario parameters stored as JSON
    parameters = Column(JSON, nullable=False)
    
    # Scenario metadata
    tags = Column(JSON, nullable=True)  # Array of tags for categorization
    version = Column(String(20), nullable=True, default="1.0")
    
    # Ownership and sharing
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_public = Column(String(10), nullable=False, default="false")  # true/false as string
    
    # Usage statistics
    execution_count = Column(Integer, nullable=False, default=0)
    last_executed = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="simulation_scenarios")
    
    def __repr__(self):
        return f"<SimulationScenario(name='{self.name}', created_by='{self.created_by}')>"


class SimulationExecution(Base):
    """Simulation execution results"""
    __tablename__ = "simulation_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("simulation_scenarios.id"), nullable=False)
    
    # Execution metadata
    execution_name = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default="running")  # running, completed, failed, cancelled
    
    # Timing information
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    execution_time_ms = Column(Numeric(10, 0), nullable=True)
    
    # Results data
    results = Column(JSON, nullable=True)
    summary = Column(JSON, nullable=True)
    
    # Performance metrics
    efficiency_score = Column(Numeric(5, 2), nullable=True)
    cost_savings = Column(Numeric(12, 2), nullable=True)
    carbon_reduction = Column(Numeric(10, 2), nullable=True)
    
    # Error information (if failed)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # Execution context
    executed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    execution_parameters = Column(JSON, nullable=True)  # Runtime parameters
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scenario = relationship("SimulationScenario", backref="executions")
    user = relationship("User", backref="simulation_executions")
    
    def __repr__(self):
        return f"<SimulationExecution(scenario_id='{self.scenario_id}', status='{self.status}')>"


class SimulationLog(Base):
    """Detailed simulation execution logs"""
    __tablename__ = "simulation_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("simulation_executions.id"), nullable=False)
    
    # Log entry details
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    level = Column(String(10), nullable=False)  # DEBUG, INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    
    # Structured data
    data = Column(JSON, nullable=True)
    step_number = Column(Integer, nullable=True)
    step_name = Column(String(100), nullable=True)
    
    # Performance data
    memory_usage_mb = Column(Numeric(10, 2), nullable=True)
    cpu_usage_percent = Column(Numeric(5, 2), nullable=True)
    
    # Relationships
    execution = relationship("SimulationExecution", backref="logs")
    
    def __repr__(self):
        return f"<SimulationLog(execution_id='{self.execution_id}', level='{self.level}')>"


class RouteOptimization(Base):
    """Route optimization results"""
    __tablename__ = "route_optimizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    execution_id = Column(UUID(as_uuid=True), ForeignKey("simulation_executions.id"), nullable=False)
    
    # Route details
    route_name = Column(String(255), nullable=False)
    fleet_unit_id = Column(UUID(as_uuid=True), ForeignKey("fleet_units.id"), nullable=True)
    
    # Optimization results
    original_route = Column(JSON, nullable=True)  # Original route data
    optimized_route = Column(JSON, nullable=False)  # Optimized route data
    
    # Performance improvements
    distance_reduction_km = Column(Numeric(8, 2), nullable=True)
    time_reduction_minutes = Column(Numeric(8, 2), nullable=True)
    fuel_savings_liters = Column(Numeric(8, 2), nullable=True)
    cost_savings = Column(Numeric(10, 2), nullable=True)
    
    # Route metadata
    waypoints = Column(JSON, nullable=False)  # Array of waypoints
    constraints = Column(JSON, nullable=True)  # Route constraints applied
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    execution = relationship("SimulationExecution", backref="route_optimizations")
    fleet_unit = relationship("FleetUnit", backref="route_optimizations")
    
    def __repr__(self):
        return f"<RouteOptimization(route_name='{self.route_name}', execution_id='{self.execution_id}')>"