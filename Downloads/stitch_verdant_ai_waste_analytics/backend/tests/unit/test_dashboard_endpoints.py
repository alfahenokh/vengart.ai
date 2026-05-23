"""
Unit tests for dashboard API endpoints
Tests the dashboard endpoints for system overview, network status, and node performance
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timedelta
from decimal import Decimal
import sys
from pathlib import Path
from uuid import uuid4

# Add backend directory to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))


# Mock database functions before importing app
@pytest.fixture(autouse=True)
def mock_database():
    """Mock database functions to avoid connection issues"""
    with patch('main.check_database_connection', new_callable=AsyncMock) as mock_check:
        mock_check.return_value = True
        with patch('main.init_db', new_callable=AsyncMock):
            with patch('main.close_db', new_callable=AsyncMock):
                with patch('app.core.db_utils.check_database_connection', new_callable=AsyncMock) as mock_check2:
                    mock_check2.return_value = True
                    yield


@pytest.fixture
def client(mock_database):
    """Create a test client"""
    from main import app
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def mock_fleet_data():
    """Create mock fleet data for testing"""
    from app.models.fleet import FleetUnitStatus, FleetUnitType, CapacityUnit
    
    mock_units = []
    for i in range(10):
        unit = MagicMock()
        unit.id = uuid4()
        unit.identifier = f"UNIT-{i:04d}"
        unit.type = FleetUnitType.COLLECTION if i % 3 == 0 else FleetUnitType.TRANSPORT if i % 3 == 1 else FleetUnitType.PROCESSING
        unit.status = FleetUnitStatus.ACTIVE if i % 4 != 3 else FleetUnitStatus.MAINTENANCE
        unit.latitude = Decimal("40.7128") + Decimal(i) * Decimal("0.01")
        unit.longitude = Decimal("-74.0060") + Decimal(i) * Decimal("0.01")
        unit.address = f"Address {i}"
        unit.zone = f"Zone-{i % 3}"
        unit.current_capacity = Decimal(50 + i * 10)
        unit.maximum_capacity = Decimal(100 + i * 10)
        unit.capacity_unit = CapacityUnit.TONS
        unit.assigned_route = {"route_id": f"route-{i}"} if i % 2 == 0 else None
        unit.metadata = {}
        unit.created_at = datetime.utcnow() - timedelta(days=30)
        unit.updated_at = datetime.utcnow() - timedelta(hours=1)
        unit.last_update = datetime.utcnow() - timedelta(minutes=5)
        mock_units.append(unit)
    
    return mock_units


@pytest.fixture
def mock_kpi_data():
    """Create mock KPI data for testing"""
    mock_kpis = []
    for i in range(5):
        kpi = MagicMock()
        kpi.id = uuid4()
        kpi.name = f"KPI-{i}"
        kpi.category = "efficiency" if i % 2 == 0 else "cost"
        kpi.value = Decimal(80 + i * 5)
        kpi.unit = "percent" if i % 2 == 0 else "dollars"
        kpi.target = Decimal(90)
        kpi.previous_value = Decimal(75 + i * 5)
        kpi.change_percent = Decimal(5)
        kpi.trend = "up"
        kpi.calculated_at = datetime.utcnow() - timedelta(hours=i)
        kpi.updated_at = datetime.utcnow() - timedelta(hours=i)
        mock_kpis.append(kpi)
    
    return mock_kpis


class TestDashboardOverview:
    """Test dashboard overview endpoint"""
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_overview_endpoint_structure(self, mock_db, client, mock_fleet_data, mock_kpi_data):
        """Test that overview endpoint returns correct structure"""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock fleet statistics query
        mock_fleet_result = MagicMock()
        mock_fleet_stats = MagicMock()
        mock_fleet_stats.total_units = 10
        mock_fleet_stats.active_units = 7
        mock_fleet_stats.idle_units = 2
        mock_fleet_stats.maintenance_units = 1
        mock_fleet_stats.offline_units = 0
        mock_fleet_stats.total_capacity = Decimal(1500)
        mock_fleet_stats.utilized_capacity = Decimal(900)
        mock_fleet_stats.units_with_routes = 5
        mock_fleet_result.first.return_value = mock_fleet_stats
        
        # Mock KPI query
        mock_kpi_result = MagicMock()
        mock_kpi_result.scalars.return_value.all.return_value = mock_kpi_data
        
        # Mock forecast query
        mock_forecast_result = MagicMock()
        mock_forecast_stats = MagicMock()
        mock_forecast_stats.total_forecasts = 5
        mock_forecast_stats.average_accuracy = Decimal(95.5)
        mock_forecast_result.first.return_value = mock_forecast_stats
        
        # Set up execute to return different results based on call order
        mock_session.execute.side_effect = [
            mock_fleet_result,
            mock_kpi_result,
            mock_forecast_result
        ]
        
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "fleet_summary" in data
        assert "kpi_summary" in data
        assert "forecast_summary" in data
        assert "operational_efficiency" in data
        
        # Verify fleet summary structure
        fleet_summary = data["fleet_summary"]
        assert "total_units" in fleet_summary
        assert "active_units" in fleet_summary
        assert "utilization_percent" in fleet_summary
        
        # Verify operational efficiency structure
        efficiency = data["operational_efficiency"]
        assert "score" in efficiency
        assert "status" in efficiency
        assert "components" in efficiency


class TestNetworkStatus:
    """Test network status endpoint"""
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_network_status_endpoint(self, mock_db, client, mock_fleet_data):
        """Test network status endpoint returns correct data"""
        # Mock database session
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_fleet_data
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/network-status")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "network_summary" in data
        assert "type_distribution" in data
        assert "status_distribution" in data
        assert "zone_distribution" in data
        assert "throughput_metrics" in data
        
        # Verify network summary
        network_summary = data["network_summary"]
        assert "total_units" in network_summary
        assert "active_units" in network_summary
        assert "network_health" in network_summary
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_network_status_with_zone_filter(self, mock_db, client, mock_fleet_data):
        """Test network status endpoint with zone filter"""
        # Mock database session
        mock_session = AsyncMock()
        
        # Filter mock data by zone
        filtered_data = [u for u in mock_fleet_data if u.zone == "Zone-0"]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = filtered_data
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/network-status?zone=Zone-0")
        assert response.status_code == 200
        
        data = response.json()
        assert "zone_distribution" in data


class TestNodePerformance:
    """Test node performance endpoints"""
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_nodes_endpoint(self, mock_db, client, mock_fleet_data):
        """Test nodes endpoint returns list of fleet units"""
        # Mock database session
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_fleet_data
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/nodes")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # Verify each node has required fields
        if len(data) > 0:
            node = data[0]
            assert "id" in node
            assert "identifier" in node
            assert "type" in node
            assert "status" in node
            assert "current_capacity" in node
            assert "maximum_capacity" in node
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_nodes_endpoint_with_filters(self, mock_db, client, mock_fleet_data):
        """Test nodes endpoint with status filter"""
        from app.models.fleet import FleetUnitStatus
        
        # Mock database session
        mock_session = AsyncMock()
        
        # Filter mock data by status
        filtered_data = [u for u in mock_fleet_data if u.status == FleetUnitStatus.ACTIVE]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = filtered_data
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/nodes?status=active")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_nodes_endpoint_pagination(self, mock_db, client, mock_fleet_data):
        """Test nodes endpoint pagination"""
        # Mock database session
        mock_session = AsyncMock()
        
        # Simulate pagination
        paginated_data = mock_fleet_data[:5]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = paginated_data
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/nodes?limit=5&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_node_details_endpoint(self, mock_db, client, mock_fleet_data):
        """Test node details endpoint for specific node"""
        # Mock database session
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_fleet_data[0]
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        node_id = mock_fleet_data[0].identifier
        response = client.get(f"/api/v1/dashboard/nodes/{node_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "identifier" in data
        assert data["identifier"] == node_id
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_node_details_not_found(self, mock_db, client):
        """Test node details endpoint returns 404 for non-existent node"""
        # Mock database session
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/nodes/NONEXISTENT")
        assert response.status_code == 404


class TestPerformanceSummary:
    """Test performance summary endpoint"""
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_performance_summary_endpoint(self, mock_db, client, mock_fleet_data, mock_kpi_data):
        """Test performance summary endpoint"""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock fleet query
        mock_fleet_result = MagicMock()
        mock_fleet_result.scalars.return_value.all.return_value = mock_fleet_data
        
        # Mock KPI query
        mock_kpi_result = MagicMock()
        mock_kpi_result.scalars.return_value.all.return_value = mock_kpi_data
        
        mock_session.execute.side_effect = [mock_fleet_result, mock_kpi_result]
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/performance-summary")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "time_window_hours" in data
        assert "fleet_performance" in data
        assert "kpi_metrics" in data
        assert "performance_indicators" in data
        
        # Verify fleet performance structure
        fleet_perf = data["fleet_performance"]
        assert "total_units" in fleet_perf
        assert "active_units" in fleet_perf
        assert "uptime_percent" in fleet_perf
        assert "average_utilization" in fleet_perf
    
    @patch('app.api.v1.endpoints.dashboard.get_async_db')
    async def test_performance_summary_custom_time_window(self, mock_db, client, mock_fleet_data, mock_kpi_data):
        """Test performance summary with custom time window"""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock fleet query
        mock_fleet_result = MagicMock()
        mock_fleet_result.scalars.return_value.all.return_value = mock_fleet_data
        
        # Mock KPI query
        mock_kpi_result = MagicMock()
        mock_kpi_result.scalars.return_value.all.return_value = mock_kpi_data
        
        mock_session.execute.side_effect = [mock_fleet_result, mock_kpi_result]
        mock_db.return_value = mock_session
        
        response = client.get("/api/v1/dashboard/performance-summary?hours=48")
        assert response.status_code == 200
        
        data = response.json()
        assert data["time_window_hours"] == 48


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
