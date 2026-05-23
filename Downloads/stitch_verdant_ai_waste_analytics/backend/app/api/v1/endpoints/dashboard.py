"""
Dashboard API endpoints for system overview and operational metrics
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal

from app.core.database import get_async_db
from app.models.fleet import FleetUnit, FleetUnitStatus, FleetUnitType
from app.models.analytics import KPIMetric, WasteForecast
from app.schemas.fleet import FleetUnitResponse, FleetStatusSummary
from app.schemas.analytics import KPIMetricResponse

router = APIRouter()


# TODO: Add Redis caching for performance optimization
# from app.core.cache import cache_response


@router.get("/overview", summary="Get system overview metrics")
async def get_system_overview(
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get comprehensive system overview with aggregated metrics.
    
    Returns:
    - Total fleet statistics
    - Key performance indicators
    - Recent forecast summary
    - Operational efficiency metrics
    
    **Validates: Requirements 3.1, 3.3, 10.4**
    """
    # Get fleet statistics
    fleet_stats_query = select(
        func.count(FleetUnit.id).label('total_units'),
        func.count(case((FleetUnit.status == FleetUnitStatus.ACTIVE, 1))).label('active_units'),
        func.count(case((FleetUnit.status == FleetUnitStatus.IDLE, 1))).label('idle_units'),
        func.count(case((FleetUnit.status == FleetUnitStatus.MAINTENANCE, 1))).label('maintenance_units'),
        func.count(case((FleetUnit.status == FleetUnitStatus.OFFLINE, 1))).label('offline_units'),
        func.sum(FleetUnit.maximum_capacity).label('total_capacity'),
        func.sum(FleetUnit.current_capacity).label('utilized_capacity'),
        func.count(case((FleetUnit.assigned_route.isnot(None), 1))).label('units_with_routes')
    )
    
    fleet_result = await db.execute(fleet_stats_query)
    fleet_stats = fleet_result.first()
    
    # Calculate utilization percentage
    total_capacity = float(fleet_stats.total_capacity or 0)
    utilized_capacity = float(fleet_stats.utilized_capacity or 0)
    utilization_percent = (utilized_capacity / total_capacity * 100) if total_capacity > 0 else 0
    
    # Get recent KPI metrics (last 24 hours)
    recent_time = datetime.utcnow() - timedelta(hours=24)
    kpi_query = select(KPIMetric).where(
        KPIMetric.calculated_at >= recent_time
    ).order_by(KPIMetric.calculated_at.desc()).limit(10)
    
    kpi_result = await db.execute(kpi_query)
    recent_kpis = kpi_result.scalars().all()
    
    # Get forecast summary
    forecast_query = select(
        func.count(WasteForecast.id).label('total_forecasts'),
        func.avg(WasteForecast.accuracy).label('average_accuracy')
    ).where(
        WasteForecast.generated_at >= recent_time
    )
    
    forecast_result = await db.execute(forecast_query)
    forecast_stats = forecast_result.first()
    
    # Calculate operational efficiency score (0-100)
    # Based on: fleet utilization (40%), active units ratio (30%), routes assigned (30%)
    active_ratio = (fleet_stats.active_units / fleet_stats.total_units * 100) if fleet_stats.total_units > 0 else 0
    route_ratio = (fleet_stats.units_with_routes / fleet_stats.total_units * 100) if fleet_stats.total_units > 0 else 0
    efficiency_score = (
        utilization_percent * 0.4 +
        active_ratio * 0.3 +
        route_ratio * 0.3
    )
    
    return {
        "timestamp": datetime.utcnow(),
        "fleet_summary": {
            "total_units": fleet_stats.total_units or 0,
            "active_units": fleet_stats.active_units or 0,
            "idle_units": fleet_stats.idle_units or 0,
            "maintenance_units": fleet_stats.maintenance_units or 0,
            "offline_units": fleet_stats.offline_units or 0,
            "total_capacity": float(fleet_stats.total_capacity or 0),
            "utilized_capacity": float(fleet_stats.utilized_capacity or 0),
            "utilization_percent": round(utilization_percent, 2),
            "units_with_routes": fleet_stats.units_with_routes or 0
        },
        "kpi_summary": {
            "total_metrics": len(recent_kpis),
            "metrics": [
                {
                    "name": kpi.name,
                    "value": float(kpi.value),
                    "unit": kpi.unit,
                    "trend": kpi.trend,
                    "change_percent": float(kpi.change_percent) if kpi.change_percent else None
                }
                for kpi in recent_kpis[:5]  # Top 5 metrics
            ]
        },
        "forecast_summary": {
            "total_forecasts": forecast_stats.total_forecasts or 0,
            "average_accuracy": float(forecast_stats.average_accuracy or 0)
        },
        "operational_efficiency": {
            "score": round(efficiency_score, 2),
            "status": "excellent" if efficiency_score >= 80 else "good" if efficiency_score >= 60 else "warning" if efficiency_score >= 40 else "critical",
            "components": {
                "fleet_utilization": round(utilization_percent, 2),
                "active_ratio": round(active_ratio, 2),
                "route_assignment_ratio": round(route_ratio, 2)
            }
        }
    }


@router.get("/network-status", summary="Get network status and fleet distribution")
async def get_network_status(
    db: AsyncSession = Depends(get_async_db),
    zone: Optional[str] = Query(None, description="Filter by operational zone")
):
    """
    Get real-time network status with fleet distribution and throughput metrics.
    
    Returns:
    - Fleet distribution by type and status
    - Geographic distribution by zone
    - Network throughput metrics
    - Capacity utilization by zone
    
    **Validates: Requirements 3.1, 3.3, 10.4**
    """
    # Base query for fleet units
    base_query = select(FleetUnit)
    if zone:
        base_query = base_query.where(FleetUnit.zone == zone)
    
    # Get all fleet units
    result = await db.execute(base_query)
    fleet_units = result.scalars().all()
    
    # Aggregate by type
    type_distribution = {}
    for unit_type in FleetUnitType:
        units_of_type = [u for u in fleet_units if u.type == unit_type]
        type_distribution[unit_type.value] = {
            "count": len(units_of_type),
            "active": len([u for u in units_of_type if u.status == FleetUnitStatus.ACTIVE]),
            "total_capacity": float(sum(u.maximum_capacity for u in units_of_type)),
            "utilized_capacity": float(sum(u.current_capacity for u in units_of_type))
        }
    
    # Aggregate by status
    status_distribution = {}
    for status in FleetUnitStatus:
        units_with_status = [u for u in fleet_units if u.status == status]
        status_distribution[status.value] = {
            "count": len(units_with_status),
            "percentage": round(len(units_with_status) / len(fleet_units) * 100, 2) if fleet_units else 0
        }
    
    # Aggregate by zone
    zone_distribution = {}
    for unit in fleet_units:
        unit_zone = unit.zone or "unassigned"
        if unit_zone not in zone_distribution:
            zone_distribution[unit_zone] = {
                "count": 0,
                "active": 0,
                "total_capacity": 0,
                "utilized_capacity": 0
            }
        zone_distribution[unit_zone]["count"] += 1
        if unit.status == FleetUnitStatus.ACTIVE:
            zone_distribution[unit_zone]["active"] += 1
        zone_distribution[unit_zone]["total_capacity"] += float(unit.maximum_capacity)
        zone_distribution[unit_zone]["utilized_capacity"] += float(unit.current_capacity)
    
    # Calculate network throughput (based on active units and their capacity)
    active_units = [u for u in fleet_units if u.status == FleetUnitStatus.ACTIVE]
    total_throughput = sum(float(u.current_capacity) for u in active_units)
    max_throughput = sum(float(u.maximum_capacity) for u in active_units)
    throughput_efficiency = (total_throughput / max_throughput * 100) if max_throughput > 0 else 0
    
    return {
        "timestamp": datetime.utcnow(),
        "network_summary": {
            "total_units": len(fleet_units),
            "active_units": len(active_units),
            "zones_covered": len([z for z in zone_distribution.keys() if z != "unassigned"]),
            "network_health": "healthy" if throughput_efficiency >= 60 else "degraded" if throughput_efficiency >= 30 else "critical"
        },
        "type_distribution": type_distribution,
        "status_distribution": status_distribution,
        "zone_distribution": zone_distribution,
        "throughput_metrics": {
            "current_throughput": round(total_throughput, 2),
            "max_throughput": round(max_throughput, 2),
            "efficiency_percent": round(throughput_efficiency, 2),
            "unit": "tons"  # Default unit, should be dynamic based on fleet configuration
        }
    }


@router.get("/nodes", summary="Get node performance data", response_model=List[FleetUnitResponse])
async def get_node_performance(
    db: AsyncSession = Depends(get_async_db),
    status: Optional[FleetUnitStatus] = Query(None, description="Filter by status"),
    type: Optional[FleetUnitType] = Query(None, description="Filter by type"),
    zone: Optional[str] = Query(None, description="Filter by zone"),
    min_utilization: Optional[float] = Query(None, ge=0, le=100, description="Minimum capacity utilization percentage"),
    max_utilization: Optional[float] = Query(None, ge=0, le=100, description="Maximum capacity utilization percentage"),
    limit: int = Query(50, ge=1, le=500, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    Get individual node (fleet unit) performance data with filtering and pagination.
    
    Returns detailed performance metrics for each fleet unit including:
    - Current status and location
    - Capacity utilization
    - Route assignment
    - Last update timestamp
    
    Supports filtering by status, type, zone, and capacity utilization.
    
    **Validates: Requirements 3.1, 3.3, 10.4**
    """
    # Build query with filters
    query = select(FleetUnit)
    
    filters = []
    if status:
        filters.append(FleetUnit.status == status)
    if type:
        filters.append(FleetUnit.type == type)
    if zone:
        filters.append(FleetUnit.zone == zone)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Order by last update (most recent first)
    query = query.order_by(FleetUnit.last_update.desc())
    
    # Apply pagination
    query = query.limit(limit).offset(offset)
    
    # Execute query
    result = await db.execute(query)
    fleet_units = result.scalars().all()
    
    # Convert to response models and apply utilization filters if specified
    response_units = []
    for unit in fleet_units:
        # Calculate utilization
        utilization = (float(unit.current_capacity) / float(unit.maximum_capacity) * 100) if unit.maximum_capacity > 0 else 0
        
        # Apply utilization filters
        if min_utilization is not None and utilization < min_utilization:
            continue
        if max_utilization is not None and utilization > max_utilization:
            continue
        
        # Convert to response model
        unit_dict = {
            "id": unit.id,
            "identifier": unit.identifier,
            "type": unit.type,
            "status": unit.status,
            "location": {
                "latitude": unit.latitude,
                "longitude": unit.longitude,
                "address": unit.address,
                "zone": unit.zone
            } if unit.latitude and unit.longitude else None,
            "current_capacity": unit.current_capacity,
            "maximum_capacity": unit.maximum_capacity,
            "capacity_unit": unit.capacity_unit,
            "assigned_route": unit.assigned_route,
            "metadata": unit.metadata,
            "created_at": unit.created_at,
            "updated_at": unit.updated_at,
            "last_update": unit.last_update
        }
        
        response_units.append(FleetUnitResponse(**unit_dict))
    
    return response_units


@router.get("/nodes/{node_id}", summary="Get specific node performance details", response_model=FleetUnitResponse)
async def get_node_details(
    node_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get detailed performance data for a specific node (fleet unit).
    
    Returns comprehensive information including:
    - Current operational status
    - Real-time location and zone
    - Capacity metrics and utilization
    - Route assignment details
    - Historical update timestamps
    
    **Validates: Requirements 3.1, 3.3**
    """
    # Query by identifier or UUID
    query = select(FleetUnit).where(
        (FleetUnit.identifier == node_id) | (FleetUnit.id == node_id)
    )
    
    result = await db.execute(query)
    unit = result.scalar_one_or_none()
    
    if not unit:
        raise HTTPException(status_code=404, detail=f"Node with identifier '{node_id}' not found")
    
    # Convert to response model
    unit_dict = {
        "id": unit.id,
        "identifier": unit.identifier,
        "type": unit.type,
        "status": unit.status,
        "location": {
            "latitude": unit.latitude,
            "longitude": unit.longitude,
            "address": unit.address,
            "zone": unit.zone
        } if unit.latitude and unit.longitude else None,
        "current_capacity": unit.current_capacity,
        "maximum_capacity": unit.maximum_capacity,
        "capacity_unit": unit.capacity_unit,
        "assigned_route": unit.assigned_route,
        "metadata": unit.metadata,
        "created_at": unit.created_at,
        "updated_at": unit.updated_at,
        "last_update": unit.last_update
    }
    
    return FleetUnitResponse(**unit_dict)


@router.get("/performance-summary", summary="Get aggregated performance summary")
async def get_performance_summary(
    db: AsyncSession = Depends(get_async_db),
    hours: int = Query(24, ge=1, le=168, description="Time window in hours for performance analysis")
):
    """
    Get aggregated performance summary for the specified time window.
    
    Provides temporal analysis of:
    - Fleet performance trends
    - Capacity utilization over time
    - Status change frequency
    - Operational efficiency metrics
    
    **Validates: Requirements 3.1, 3.3, 10.4**
    """
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    # Get current fleet state
    fleet_query = select(FleetUnit)
    result = await db.execute(fleet_query)
    fleet_units = result.scalars().all()
    
    # Get KPI metrics within time window
    kpi_query = select(KPIMetric).where(
        KPIMetric.calculated_at >= time_threshold
    ).order_by(KPIMetric.calculated_at.desc())
    
    kpi_result = await db.execute(kpi_query)
    kpis = kpi_result.scalars().all()
    
    # Calculate performance metrics
    total_units = len(fleet_units)
    active_units = len([u for u in fleet_units if u.status == FleetUnitStatus.ACTIVE])
    
    # Calculate average utilization
    total_capacity = sum(float(u.maximum_capacity) for u in fleet_units)
    utilized_capacity = sum(float(u.current_capacity) for u in fleet_units)
    avg_utilization = (utilized_capacity / total_capacity * 100) if total_capacity > 0 else 0
    
    # Group KPIs by category
    kpi_by_category = {}
    for kpi in kpis:
        if kpi.category not in kpi_by_category:
            kpi_by_category[kpi.category] = []
        kpi_by_category[kpi.category].append({
            "name": kpi.name,
            "value": float(kpi.value),
            "unit": kpi.unit,
            "trend": kpi.trend,
            "calculated_at": kpi.calculated_at
        })
    
    # Calculate uptime percentage (based on active + idle vs maintenance + offline)
    operational_units = len([u for u in fleet_units if u.status in [FleetUnitStatus.ACTIVE, FleetUnitStatus.IDLE]])
    uptime_percent = (operational_units / total_units * 100) if total_units > 0 else 0
    
    return {
        "timestamp": datetime.utcnow(),
        "time_window_hours": hours,
        "fleet_performance": {
            "total_units": total_units,
            "active_units": active_units,
            "operational_units": operational_units,
            "uptime_percent": round(uptime_percent, 2),
            "average_utilization": round(avg_utilization, 2)
        },
        "kpi_metrics": kpi_by_category,
        "performance_indicators": {
            "efficiency_score": round(avg_utilization * 0.6 + uptime_percent * 0.4, 2),
            "health_status": "excellent" if uptime_percent >= 95 else "good" if uptime_percent >= 85 else "warning" if uptime_percent >= 70 else "critical"
        }
    }
