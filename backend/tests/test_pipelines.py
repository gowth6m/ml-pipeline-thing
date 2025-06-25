from fastapi.testclient import TestClient


class TestPipelineEndpoints:
    """Test pipeline CRUD endpoints"""

    def test_create_pipeline_success(
        self, client: TestClient, sample_pipeline_data: dict
    ):
        """Test successful pipeline creation"""
        response = client.post("/v1/pipelines/", json=sample_pipeline_data)

        assert response.status_code == 201
        data = response.json()

        assert data["name"] == sample_pipeline_data["name"]
        assert data["description"] == sample_pipeline_data["description"]
        assert data["config"] == sample_pipeline_data["config"]
        assert data["status"] == "PENDING"
        assert "id" in data
        assert "createdAt" in data
        assert "updatedAt" in data

        # Check stages
        assert len(data["stages"]) == 3
        stages = data["stages"]
        assert stages[0]["name"] == "Data Ingestion"
        assert stages[0]["stageType"] == "DATA_INGESTION"
        assert stages[0]["order"] == 0
        assert stages[1]["name"] == "Data Preprocessing"
        assert stages[1]["order"] == 1
        assert stages[2]["name"] == "Model Training"
        assert stages[2]["order"] == 2

    def test_create_pipeline_with_invalid_dependencies(self, client: TestClient):
        """Test pipeline creation with invalid stage dependencies"""
        invalid_pipeline_data = {
            "name": "Invalid Pipeline",
            "description": "Pipeline with invalid dependencies",
            "config": {"timeout": 3600},
            "stages": [
                {
                    "name": "Stage 1",
                    "stageType": "DATA_INGESTION",
                    "order": 0,
                    "config": {"source": "database"},
                    "dependencies": [],
                },
                {
                    "name": "Stage 2",
                    "stageType": "DATA_PREPROCESSING",
                    "order": 1,
                    "config": {"normalize": True},
                    "dependencies": ["5"],  # Non-existent stage order
                },
            ],
        }

        response = client.post("/v1/pipelines/", json=invalid_pipeline_data)
        assert response.status_code == 422

    def test_create_pipeline_missing_required_fields(self, client: TestClient):
        """Test pipeline creation with missing required fields"""
        response = client.post("/v1/pipelines/", json={})
        assert response.status_code == 422

    def test_create_pipeline_invalid_stage_type(self, client: TestClient):
        """Test pipeline creation with invalid stage type"""
        invalid_data = {
            "name": "Invalid Pipeline",
            "description": "Pipeline with invalid stage type",
            "stages": [
                {
                    "name": "Invalid Stage",
                    "stageType": "INVALID_TYPE",
                    "order": 0,
                    "dependencies": [],
                }
            ],
        }
        response = client.post("/v1/pipelines/", json=invalid_data)
        assert response.status_code == 422

    def test_create_pipeline_duplicate_stage_orders(self, client: TestClient):
        """Test pipeline creation with duplicate stage orders"""
        duplicate_order_data = {
            "name": "Duplicate Order Pipeline",
            "description": "Pipeline with duplicate stage orders",
            "stages": [
                {
                    "name": "Stage 1",
                    "stageType": "DATA_INGESTION",
                    "order": 0,
                    "dependencies": [],
                },
                {
                    "name": "Stage 2",
                    "stageType": "DATA_PREPROCESSING",
                    "order": 0,  # Duplicate order
                    "dependencies": [],
                },
            ],
        }
        response = client.post("/v1/pipelines/", json=duplicate_order_data)
        assert response.status_code == 422
