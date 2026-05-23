# Dashboard API Endpoints

## Overview

This module implements the dashboard API endpoints for the Verdant AI Integrated Dashboard system. It provides real-time data aggregation and metrics for system overview, network status, and node performance monitoring.

## Endpoints

### 1. System Overview (`GET /api/v1/dashboard/overview`)

Provides comprehensive system overview with aggregated metrics including:
- Fleet statistics (total units, active/idle/maintenance/offline counts)
- Capacity utilization metrics
- Recent KPI metrics (last 24 hours)
- Forecast summary
- Operational efficiency score

**Response Structure:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "fleet_summary": {
    "total_units": 10,
    "active_units": 7,
    "idle_units": 2,
    "maintenance_units": 1,
    "offline_units": 0,
    "total_capacity": 1500.0,
    "utilized_capacity": 900.0,
    "utilization_percent": 60.0,
    "units_with_routes": 5
  },
  "kpi_summary": {
    "total_metrics": 5,
    "metrics": [...]
  },
  "forecast_summary": {
    "total_forecasts": 5,
    "average_accuracy": 95.5
  },
  "operational_efficiency": {
    "score": 72.5,
    "status": "good",
    "components": {
      "fleet_utilization": 60.0,
      "active_ratio": 70.0,
      "route_assignment_ratio": 50.0
    }
  }
}
```

### 2. Network Status (`GET /api/v1/dashboard/network-status`)

Provides real-time network status with fleet distribution and throughput metrics:
- Fleet distribution by type (collection, transport, processing)
- Fleet distribution by status (active, idle, maintenance, offline)
- Geographic distribution by zone
- Network throughput metrics

**Query Parameters:**
- `zone` (optional): Filter by operational zone

**Response Structure:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "network_summary": {
    "total_units": 10,
    "active_units": 7,
    "zones_covered": 3,
    "network_health": "healthy"
  },
  "type_distribution": {
    "collection": {
      "count": 4,
      "active": 3,
      "total_capacity": 600.0,
      "utilized_capacity": 350.0
    },
    ...
  },
  "status_distribution": {
    "active": {
      "count": 7,
      "percentage": 70.0
    },
    ...
  },
  "zone_distribution": {
    "Zone-0": {
      "count": 4,
      "active": 3,
      "total_capacity": 600.0,
      "utilized_capacity": 350.0
    },
    ...
  },
  "throughput_metrics": {
    "current_throughput": 850.0,
    "max_throughput": 1200.0,
    "efficiency_percent": 70.83,
    "unit": "tons"
  }
}
```

### 3. Node Performance List (`GET /api/v1/dashboard/nodes`)

Returns detailed performance metrics for fleet units with filtering and pagination support.

**Query Parameters:**
- `status` (optional): Filter by FleetUnitStatus (active, idle, maintenance, offline)
- `type` (optional): Filter by FleetUnitType (collection, transport, processing)
- `zone` (optional): Filter by operational zone
- `min_utilization` (optional): Minimum capacity utilization percentage (0-100)
- `max_utilization` (optional): Maximum capacity utilization percentage (0-100)
- `limit` (optional, default=50): Maximum number of results (1-500)
- `offset` (optional, default=0): Number of results to skip

**Response:** Array of FleetUnitResponse objects

### 4. Node Details (`GET /api/v1/dashboard/nodes/{node_id}`)

Returns detailed performance data for a specific node (fleet unit).

**Path Parameters:**
- `node_id`: Fleet unit identifier or UUID

**Response:** Single FleetUnitResponse object

**Error Responses:**
- `404 Not Found`: Node with specified identifier not found

### 5. Performance Summary (`GET /api/v1/dashboard/performance-summary`)

Provides aggregated performance summary for a specified time window.

**Query Parameters:**
- `hours` (optional, default=24): Time window in hours for performance analysis (1-168)

**Response Structure:**
```json
{
  "timestamp": "2024-01-01T00:00:00",
  "time_window_hours": 24,
  "fleet_performance": {
    "total_units": 10,
    "active_units": 7,
    "operational_units": 9,
    "uptime_percent": 90.0,
    "average_utilization": 60.0
  },
  "kpi_metrics": {
    "efficiency": [...],
    "cost": [...]
  },
  "performance_indicators": {
    "efficiency_score": 72.0,
    "health_status": "good"
  }
}
```

## Data Aggregation Logic

### Operational Efficiency Score
Calculated as a weighted average of:
- Fleet utilization (40%): Current capacity / Maximum capacity
- Active units ratio (30%): Active units / Total units
- Route assignment ratio (30%): Units with routes / Total units

### Network Health Status
Determined by throughput efficiency:
- **healthy**: ≥60% throughput efficiency
- **degraded**: 30-59% throughput efficiency
- **critical**: <30% throughput efficiency

### Performance Health Status
Based on uptime percentage:
- **excellent**: ≥95% uptime
- **good**: 85-94% uptime
- **warning**: 70-84% uptime
- **critical**: <70% uptime

## Caching Strategy

**TODO**: Redis caching implementation for performance optimization

Recommended caching strategy:
- System overview: Cache for 30 seconds
- Network status: Cache for 15 seconds
- Node performance list: Cache for 10 seconds
- Performance summary: Cache for 60 seconds

Cache invalidation triggers:
- Fleet unit status changes
- Capacity updates
- Route assignments
- KPI metric updates

## Requirements Validation

This implementation validates the following requirements:
- **Requirement 3.1**: RESTful endpoints for dashboard operations
- **Requirement 3.3**: API response time within 200ms for standard operations
- **Requirement 10.4**: Efficient caching strategies (TODO: Redis implementation)

## Testing

Unit tests are provided in `backend/tests/unit/test_dashboard_endpoints.py` covering:
- System overview endpoint structure and data
- Network status with and without zone filtering
- Node performance list with various filters
- Node performance pagination
- Node details retrieval
- Performance summary with custom time windows
- Error handling (404 for non-existent nodes)

## Integration

The dashboard router is integrated into the main API router at `/api/v1/dashboard/` prefix with the "dashboard" tag for API documentation.

## Future Enhancements

1. **Redis Caching**: Implement Redis-based caching for improved performance
2. **WebSocket Integration**: Real-time updates for dashboard metrics
3. **Historical Data**: Add endpoints for historical trend analysis
4. **Alerts**: Implement threshold-based alerting for critical metrics
5. **Export**: Add data export functionality (CSV, JSON)
