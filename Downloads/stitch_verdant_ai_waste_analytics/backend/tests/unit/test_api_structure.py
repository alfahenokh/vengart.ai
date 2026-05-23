"""
Unit tests for API structure and middleware
Tests the FastAPI application setup, routing, and middleware functionality
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
import sys
from pathlib import Path

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


class TestAPIStructure:
    """Test API structure and routing"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Verdant AI Integrated Dashboard API"
        assert data["version"] == "1.0.0"
        assert "docs" in data
        assert "api_v1" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "environment" in data
        assert "version" in data
    
    def test_api_v1_health_endpoint(self, client):
        """Test API v1 health endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "api_version" in data
        assert data["api_version"] == "v1"
    
    def test_api_v1_status_endpoint(self, client):
        """Test API v1 status endpoint"""
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert "api_version" in data
        assert "services" in data
        assert "endpoints" in data
        assert data["api_version"] == "v1"


class TestMiddleware:
    """Test middleware functionality"""
    
    def test_request_id_header(self, client):
        """Test that X-Request-ID header is added to responses"""
        response = client.get("/")
        assert "X-Request-ID" in response.headers
        # Verify it's a valid UUID format
        request_id = response.headers["X-Request-ID"]
        assert len(request_id) == 36  # UUID format: 8-4-4-4-12
        assert request_id.count("-") == 4
    
    def test_process_time_header(self, client):
        """Test that X-Process-Time header is added to responses"""
        response = client.get("/")
        assert "X-Process-Time" in response.headers
        # Verify it's a valid float
        process_time = float(response.headers["X-Process-Time"])
        assert process_time >= 0
    
    def test_cors_headers(self, client):
        """Test CORS headers are properly configured"""
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestAPIVersioning:
    """Test API versioning structure"""
    
    def test_api_v1_prefix(self, client):
        """Test that API v1 endpoints are accessible under /api/v1/ prefix"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_openapi_docs_accessible(self, client):
        """Test that OpenAPI documentation is accessible"""
        response = client.get("/api/docs")
        assert response.status_code == 200
    
    def test_openapi_json_accessible(self, client):
        """Test that OpenAPI JSON schema is accessible"""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data


class TestErrorHandling:
    """Test error handling middleware"""
    
    def test_404_error(self, client):
        """Test 404 error for non-existent endpoint"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test 405 error for wrong HTTP method"""
        response = client.post("/")
        assert response.status_code == 405


class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_cors_allows_localhost_3000(self, client):
        """Test CORS allows requests from localhost:3000"""
        response = client.get(
            "/api/v1/health",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
    
    def test_cors_allows_localhost_5173(self, client):
        """Test CORS allows requests from localhost:5173 (Vite)"""
        response = client.get(
            "/api/v1/health",
            headers={"Origin": "http://localhost:5173"}
        )
        assert response.status_code == 200
    
    def test_cors_exposes_custom_headers(self, client):
        """Test CORS exposes custom headers"""
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        # Check if custom headers are exposed
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
