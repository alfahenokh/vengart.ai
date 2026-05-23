"""
Analytics and forecasting models
"""
from sqlalchemy import Column, String, DateTime, Numeric, JSON, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class WasteForecast(Base):
    """Waste volume forecast model"""
    __tablename__ = "waste_forecasts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region = Column(String(100), nullable=False, index=True)
    
    # Time range for forecast
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Forecast data stored as JSON array
    predictions = Column(JSON, nullable=False)
    
    # Model metadata
    accuracy = Column(Numeric(5, 2), nullable=True)  # Percentage accuracy
    model_version = Column(String(50), nullable=True)
    confidence_interval = Column(Numeric(5, 2), nullable=True)
    
    # Additional metadata
    parameters = Column(JSON, nullable=True)  # Model parameters used
    factors = Column(JSON, nullable=True)     # Factors considered in prediction
    
    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<WasteForecast(region='{self.region}', start_date='{self.start_date}')>"


class KPIMetric(Base):
    """Key Performance Indicator metrics"""
    __tablename__ = "kpi_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # efficiency, cost, environmental, etc.
    
    # Metric values
    value = Column(Numeric(15, 4), nullable=False)
    unit = Column(String(20), nullable=False)
    target = Column(Numeric(15, 4), nullable=True)
    
    # Trend analysis
    previous_value = Column(Numeric(15, 4), nullable=True)
    change_percent = Column(Numeric(5, 2), nullable=True)
    trend = Column(String(10), nullable=True)  # up, down, stable
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    
    # Additional metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<KPIMetric(name='{self.name}', value='{self.value}', unit='{self.unit}')>"


class AnalyticsReport(Base):
    """Generated analytics reports"""
    __tablename__ = "analytics_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False)  # kpi, forecast, efficiency, etc.
    
    # Report parameters
    parameters = Column(JSON, nullable=False)
    filters = Column(JSON, nullable=True)
    
    # Report data
    data = Column(JSON, nullable=False)
    summary = Column(JSON, nullable=True)
    
    # File information (if exported)
    file_path = Column(String(500), nullable=True)
    file_format = Column(String(10), nullable=True)  # pdf, excel, csv
    file_size = Column(Numeric(10, 0), nullable=True)  # bytes
    
    # Generation metadata
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    generation_time_ms = Column(Numeric(10, 0), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", backref="analytics_reports")
    
    def __repr__(self):
        return f"<AnalyticsReport(name='{self.name}', type='{self.report_type}')>"