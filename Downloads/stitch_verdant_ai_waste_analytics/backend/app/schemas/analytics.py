"""
Analytics and forecasting Pydantic schemas for API request/response validation
"""
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, computed_field

from app.models.analytics import WasteForecast, KPIMetric, AnalyticsReport


class PredictionFactor(BaseModel):
    """Factor that influences waste predictions"""
    name: str = Field(..., description="Factor name")
    weight: Decimal = Field(..., ge=0, le=1, description="Factor weight (0-1)")
    value: Decimal = Field(..., description="Factor value")
    impact: str = Field(..., description="Impact description")


class ForecastPoint(BaseModel):
    """Individual forecast data point"""
    date: date = Field(..., description="Forecast date")
    predicted_volume: Decimal = Field(..., ge=0, description="Predicted waste volume")
    confidence: Decimal = Field(..., ge=0, le=100, description="Prediction confidence percentage")
    lower_bound: Optional[Decimal] = Field(None, ge=0, description="Lower confidence bound")
    upper_bound: Optional[Decimal] = Field(None, ge=0, description="Upper confidence bound")
    factors: Optional[List[PredictionFactor]] = Field(None, description="Factors influencing this prediction")

    @field_validator('upper_bound')
    @classmethod
    def validate_bounds(cls, v, info):
        """Validate that upper bound is greater than lower bound"""
        if v is not None and 'lower_bound' in info.data and info.data['lower_bound'] is not None:
            if v <= info.data['lower_bound']:
                raise ValueError('Upper bound must be greater than lower bound')
        return v


class WasteForecastBase(BaseModel):
    """Base waste forecast schema"""
    region: str = Field(..., max_length=100, description="Geographic region")
    start_date: date = Field(..., description="Forecast start date")
    end_date: date = Field(..., description="Forecast end date")
    model_version: Optional[str] = Field(None, max_length=50, description="ML model version used")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Model parameters")

    @field_validator('end_date')
    @classmethod
    def validate_date_range(cls, v, info):
        """Validate that end date is after start date"""
        if 'start_date' in info.data and v <= info.data['start_date']:
            raise ValueError('End date must be after start date')
        return v


class WasteForecastCreate(WasteForecastBase):
    """Schema for creating a waste forecast"""
    predictions: List[ForecastPoint] = Field(..., min_items=1, description="Forecast predictions")
    accuracy: Optional[Decimal] = Field(None, ge=0, le=100, description="Model accuracy percentage")
    confidence_interval: Optional[Decimal] = Field(None, ge=0, le=100, description="Confidence interval")
    factors: Optional[List[PredictionFactor]] = Field(None, description="Global factors")

    @field_validator('predictions')
    @classmethod
    def validate_predictions_date_range(cls, v, info):
        """Validate that all predictions fall within the forecast date range"""
        if 'start_date' in info.data and 'end_date' in info.data:
            start_date = info.data['start_date']
            end_date = info.data['end_date']
            for prediction in v:
                if not (start_date <= prediction.date <= end_date):
                    raise ValueError(f'Prediction date {prediction.date} is outside forecast range')
        return v


class WasteForecastResponse(WasteForecastBase):
    """Schema for waste forecast response"""
    id: UUID = Field(..., description="Forecast unique identifier")
    predictions: List[ForecastPoint] = Field(..., description="Forecast predictions")
    accuracy: Optional[Decimal] = Field(None, description="Model accuracy percentage")
    confidence_interval: Optional[Decimal] = Field(None, description="Confidence interval")
    factors: Optional[List[PredictionFactor]] = Field(None, description="Global factors")
    total_predicted_volume: Decimal = Field(..., description="Total predicted volume for the period")
    average_confidence: Decimal = Field(..., description="Average confidence across all predictions")
    generated_at: datetime = Field(..., description="Generation timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def total_predicted_volume(self) -> Decimal:
        """Calculate total predicted volume"""
        return sum(p.predicted_volume for p in self.predictions)

    @computed_field
    @property
    def average_confidence(self) -> Decimal:
        """Calculate average confidence"""
        if self.predictions:
            return sum(p.confidence for p in self.predictions) / len(self.predictions)
        return Decimal('0')


class KPIMetricBase(BaseModel):
    """Base KPI metric schema"""
    name: str = Field(..., max_length=100, description="KPI metric name")
    category: str = Field(..., max_length=50, description="KPI category")
    value: Decimal = Field(..., description="Current metric value")
    unit: str = Field(..., max_length=20, description="Unit of measurement")
    target: Optional[Decimal] = Field(None, description="Target value")
    period_start: datetime = Field(..., description="Measurement period start")
    period_end: datetime = Field(..., description="Measurement period end")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @field_validator('period_end')
    @classmethod
    def validate_period(cls, v, info):
        """Validate that period end is after period start"""
        if 'period_start' in info.data and v <= info.data['period_start']:
            raise ValueError('Period end must be after period start')
        return v


class KPIMetricCreate(KPIMetricBase):
    """Schema for creating a KPI metric"""
    previous_value: Optional[Decimal] = Field(None, description="Previous period value")


class KPIMetricResponse(KPIMetricBase):
    """Schema for KPI metric response"""
    id: UUID = Field(..., description="KPI metric unique identifier")
    previous_value: Optional[Decimal] = Field(None, description="Previous period value")
    change_percent: Optional[Decimal] = Field(None, description="Percentage change from previous period")
    trend: Optional[str] = Field(None, description="Trend direction (up/down/stable)")
    target_achievement_percent: Optional[Decimal] = Field(None, description="Target achievement percentage")
    performance_status: str = Field(..., description="Performance status (excellent/good/warning/critical)")
    calculated_at: datetime = Field(..., description="Calculation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True

    @computed_field
    @property
    def change_percent(self) -> Optional[Decimal]:
        """Calculate percentage change"""
        if self.previous_value is not None and self.previous_value != 0:
            return round(((self.value - self.previous_value) / self.previous_value) * 100, 2)
        return None

    @computed_field
    @property
    def trend(self) -> Optional[str]:
        """Determine trend based on change"""
        change = self.change_percent
        if change is not None:
            if change > 5:
                return "up"
            elif change < -5:
                return "down"
            else:
                return "stable"
        return None

    @computed_field
    @property
    def target_achievement_percent(self) -> Optional[Decimal]:
        """Calculate target achievement percentage"""
        if self.target is not None and self.target != 0:
            return round((self.value / self.target) * 100, 2)
        return None

    @computed_field
    @property
    def performance_status(self) -> str:
        """Determine performance status based on target achievement"""
        achievement = self.target_achievement_percent
        if achievement is not None:
            if achievement >= 100:
                return "excellent"
            elif achievement >= 80:
                return "good"
            elif achievement >= 60:
                return "warning"
            else:
                return "critical"
        return "unknown"


class AnalyticsReportBase(BaseModel):
    """Base analytics report schema"""
    name: str = Field(..., max_length=255, description="Report name")
    report_type: str = Field(..., max_length=50, description="Report type")
    parameters: Dict[str, Any] = Field(..., description="Report parameters")
    filters: Optional[Dict[str, Any]] = Field(None, description="Applied filters")


class AnalyticsReportCreate(AnalyticsReportBase):
    """Schema for creating an analytics report"""
    data: Dict[str, Any] = Field(..., description="Report data")
    summary: Optional[Dict[str, Any]] = Field(None, description="Report summary")
    file_format: Optional[str] = Field(None, description="Export file format")


class AnalyticsReportResponse(AnalyticsReportBase):
    """Schema for analytics report response"""
    id: UUID = Field(..., description="Report unique identifier")
    data: Dict[str, Any] = Field(..., description="Report data")
    summary: Optional[Dict[str, Any]] = Field(None, description="Report summary")
    file_path: Optional[str] = Field(None, description="Export file path")
    file_format: Optional[str] = Field(None, description="Export file format")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    generated_by: UUID = Field(..., description="User who generated the report")
    generation_time_ms: Optional[int] = Field(None, description="Generation time in milliseconds")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")

    class Config:
        from_attributes = True


class ForecastSummary(BaseModel):
    """Summary of forecast data"""
    total_forecasts: int = Field(..., description="Total number of forecasts")
    regions_covered: int = Field(..., description="Number of regions with forecasts")
    average_accuracy: Decimal = Field(..., description="Average forecast accuracy")
    latest_forecast_date: Optional[date] = Field(None, description="Date of latest forecast")
    total_predicted_volume: Decimal = Field(..., description="Total predicted volume across all forecasts")


class KPISummary(BaseModel):
    """Summary of KPI metrics"""
    total_metrics: int = Field(..., description="Total number of KPI metrics")
    categories: List[str] = Field(..., description="List of KPI categories")
    excellent_count: int = Field(..., description="Number of metrics with excellent performance")
    good_count: int = Field(..., description="Number of metrics with good performance")
    warning_count: int = Field(..., description="Number of metrics with warning status")
    critical_count: int = Field(..., description="Number of metrics with critical status")
    average_target_achievement: Decimal = Field(..., description="Average target achievement percentage")


class AnalyticsDashboard(BaseModel):
    """Comprehensive analytics dashboard data"""
    forecast_summary: ForecastSummary = Field(..., description="Forecast data summary")
    kpi_summary: KPISummary = Field(..., description="KPI metrics summary")
    recent_forecasts: List[WasteForecastResponse] = Field(..., description="Recent forecasts")
    key_metrics: List[KPIMetricResponse] = Field(..., description="Key performance metrics")
    generated_at: datetime = Field(..., description="Dashboard generation timestamp")