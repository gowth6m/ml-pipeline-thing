import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.database import Base, get_db
from src.server import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client with test database"""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_pipeline_data():
    """Sample pipeline data for testing"""
    return {
        "name": "Test ML Pipeline Thing API",
        "description": "A test machine learning pipeline",
        "config": {"timeout": 3600},
        "stages": [
            {
                "name": "Data Ingestion",
                "stageType": "DATA_INGESTION",
                "order": 0,
                "config": {"source": "database"},
                "dependencies": [],
            },
            {
                "name": "Data Preprocessing",
                "stageType": "DATA_PREPROCESSING",
                "order": 1,
                "config": {"normalize": True},
                "dependencies": ["0"],
            },
            {
                "name": "Model Training",
                "stageType": "MODEL_TRAINING",
                "order": 2,
                "config": {"algorithm": "random_forest"},
                "dependencies": ["1"],
            },
        ],
    }


@pytest.fixture
def sample_trigger_data():
    """Sample trigger data for testing"""
    return {
        "runConfig": {"batchSize": 100},
        "environment": "development",
        "triggeredBy": "test_user",
        "tags": ["test", "ml"],
        "notes": "Test run",
    }
