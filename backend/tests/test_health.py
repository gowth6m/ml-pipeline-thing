from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
    assert "memoryUsage" in data
    assert "database" in data
    assert "uptime" in data

    # Check memory_usage structure
    memory_usage = data["memoryUsage"]
    assert "used" in memory_usage
    assert "available" in memory_usage
    assert "percent" in memory_usage


def test_api_docs_accessible(client: TestClient):
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/redoc")
    assert response.status_code == 200


def test_openapi_spec(client: TestClient):
    """Test that OpenAPI spec is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    spec = response.json()
    assert "openapi" in spec
    assert "info" in spec
    assert "paths" in spec

    # Check that our endpoints are documented
    paths = spec["paths"]
    assert "/v1/pipelines/" in paths
    assert "/v1/pipelines/{pipeline_id}" in paths
    assert "/v1/pipelines/{pipeline_id}/trigger_run" in paths
