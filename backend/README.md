# ML Pipeline Thing - Backend API

A lightweight FastAPI-based ML pipeline orchestration system for managing machine learning workflows, experiments, and artifacts.

## Documentation

- [API Documentation](https://api.ml-pipeline-thing.gowtham.io/docs)

## Features

- **Pipeline Management** - Create, execute, and monitor ML pipelines
- **Run Tracking** - Track pipeline executions with detailed metrics
- **Artifact Storage** - Manage models, datasets, and other ML artifacts
- **Stage-based Execution** - Break pipelines into manageable stages
- **Comprehensive Artifact System** - Support for models, datasets, metrics, plots, and more
- **Resource Monitoring** - Track memory and CPU usage across pipeline execution

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Poetry (recommended) or pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ml-pipeline-thing/backend
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Configure database**
   ```bash
   # Create PostgreSQL database
   createdb ml_pipeline_thing
   
   # Run migrations
   poetry run alembic upgrade head
   ```

5. **Start the server**
   ```bash
   # Development
   poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 9095
   
   # Production
   poetry run gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:9095
   ```

## Project Structure

```
backend/
├── alembic.ini                 # Alembic configuration for database migrations
├── Dockerfile                  # Docker container configuration
├── Makefile                    # Build and deployment automation
├── poetry.lock                 # Poetry dependency lock file
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # This file
├── src/                        # Main source code
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── server.py               # Server configuration and startup
│   ├── controller/             # API route handlers (controllers)
│   │   ├── __init__.py
│   │   ├── health.py           # Health check endpoints
│   │   └── v1/                 # API version 1 endpoints
│   │       ├── __init__.py
│   │       ├── pipelines.py    # Pipeline management endpoints
│   │       └── runs.py         # Pipeline run endpoints
│   ├── core/                   # Core application components
│   │   ├── config/             # Configuration management
│   │   │   ├── __init__.py
│   │   │   ├── environments.py # Environment-specific settings
│   │   │   └── settings.py     # Application settings
│   │   ├── database/           # Database configuration and setup
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base database model
│   │   │   ├── database.py     # Database connection and session
│   │   │   ├── init.py         # Database initialization
│   │   │   └── migrations/     # Database migration files
│   │   │       ├── env.py      # Alembic environment configuration
│   │   │       ├── README      # Migration documentation
│   │   │       ├── script.py.mako # Migration template
│   │   │       └── versions/   # Migration version files
│   │   │           └── 4f4e17d47c12_initial_migration.py
│   │   └── exceptions/         # Custom exception classes
│   │       └── exceptions.py   # Application-specific exceptions
│   ├── models/                 # Data models and schemas
│   │   ├── __init__.py
│   │   ├── core.py             # Core model definitions
│   │   ├── dto/                # Data Transfer Objects (API schemas)
│   │   │   ├── __init__.py
│   │   │   ├── artifact.py     # Artifact API schemas
│   │   │   ├── health.py       # Health check schemas
│   │   │   ├── pagination.py   # Pagination schemas
│   │   │   ├── pipeline.py     # Pipeline API schemas
│   │   │   └── run.py          # Run API schemas
│   │   └── schema/             # Database schema models
│   │       ├── __init__.py
│   │       ├── artifact.py     # Artifact database models
│   │       ├── pipeline.py     # Pipeline and stage models
│   │       └── run.py          # Run and stage run models
│   └── services/               # Business logic layer
│       ├── __init__.py
│       ├── pipeline_service.py # Pipeline business logic
│       └── run_service.py      # Run business logic
└── tests/                      # Test suite
    ├── __init__.py
    ├── conftest.py             # Pytest configuration and fixtures
    ├── test_health.py          # Health endpoint tests
    ├── test_pipelines.py       # Pipeline endpoint tests
    └── test_runs.py            # Run endpoint tests
```

### Key Components Explained

#### **Controllers (`src/controller/`)**
- **API Route Handlers**: Handle HTTP requests and responses
- **Request Validation**: Validate incoming API requests
- **Response Formatting**: Format API responses according to standards
- **Version Management**: Organized by API versions (v1, v2, etc.)

#### **Core (`src/core/`)**
- **Configuration Management**: Environment-specific settings and configuration
- **Database Layer**: Database connection, models, and migration management
- **Exception Handling**: Custom exceptions for better error handling
- **Base Classes**: Common base classes used throughout the application

#### **Models (`src/models/`)**
- **Database Schemas (`schema/`)**: SQLAlchemy ORM models for database tables
- **DTOs (`dto/`)**: Pydantic models for API request/response validation
- **Core Models**: Shared model definitions and utilities

#### **Services (`src/services/`)**
- **Business Logic**: Core application logic and rules
- **Data Processing**: Handle data transformations and validations
- **External Integrations**: Interface with external services and APIs
- **Transaction Management**: Handle complex business transactions

#### **Database Structure**
- **Migrations**: Version-controlled database schema changes
- **Base Model**: Common fields and methods for all database models
- **Session Management**: Database connection and transaction handling

#### **Testing (`tests/`)**
- **Unit Tests**: Test individual components and functions
- **Integration Tests**: Test API endpoints and database interactions
- **Fixtures**: Reusable test data and setup utilities
- **Configuration**: Test-specific configuration and setup

## Configuration

Key configuration options in `src/core/config/settings.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/ml_pipeline_thing` | PostgreSQL connection string |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `9095` | Server port |
| `MAX_CONCURRENT_PIPELINES` | `5` | Maximum concurrent pipeline executions |
| `PIPELINE_TIMEOUT` | `3600` | Pipeline timeout in seconds |

## API Endpoints

### Health
- `GET /health` - Health check endpoint

### Pipelines
- `GET /api/v1/pipelines` - List all pipelines
- `POST /api/v1/pipelines` - Create a new pipeline
- `GET /api/v1/pipelines/{id}` - Get pipeline details
- `PUT /api/v1/pipelines/{id}` - Update pipeline
- `DELETE /api/v1/pipelines/{id}` - Delete pipeline

### Runs
- `GET /api/v1/runs` - List all runs
- `GET /api/v1/runs/{id}` - Get run details
- `POST /api/v1/runs/{id}/cancel` - Cancel a running pipeline

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black src/
poetry run isort src/
```

### Database Migrations
```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head
```

## Database Schema

```mermaid
erDiagram
    pipelines {
        uuid id PK
        string name
        text description
        enum status
        json config
        datetime started_at
        datetime completed_at
        float execution_time
        float memory_usage
        float cpu_usage
        datetime created_at
        datetime updated_at
    }
    
    pipeline_stages {
        uuid id PK
        uuid pipeline_id FK
        string name
        enum stage_type
        string custom_name
        enum status
        int order
        json config
        json dependencies
        datetime started_at
        datetime completed_at
        float execution_time
        string output_path
        json metrics
        text logs
        datetime created_at
        datetime updated_at
    }
    
    pipeline_runs {
        uuid id PK
        uuid pipeline_id FK
        enum status
        enum trigger_type
        string triggered_by
        datetime started_at
        datetime completed_at
        float execution_time
        json run_config
        string environment
        float max_memory_usage
        float max_cpu_usage
        int success_count
        int failed_count
        text error_message
        json output_data
        json tags
        text notes
        datetime created_at
        datetime updated_at
    }
    
    stage_runs {
        uuid id PK
        uuid pipeline_run_id FK
        uuid stage_id FK
        enum status
        int attempt_number
        datetime started_at
        datetime completed_at
        float execution_time
        float memory_usage
        float cpu_usage
        json output_data
        text error_message
        text logs
        datetime created_at
        datetime updated_at
    }
    
    artifacts {
        uuid id PK
        string name
        text description
        enum artifact_type
        enum status
        string file_path
        string file_name
        int file_size
        enum storage_type
        json storage_config
        uuid stage_id FK
        uuid stage_run_id FK
        json artifact_metadata
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    datasets {
        uuid id PK
        uuid artifact_id FK
        string format
        int row_count
        int column_count
        json schema
        datetime created_at
        datetime updated_at
    }
    
    models {
        uuid id PK
        uuid artifact_id FK
        string model_type
        string algorithm
        string framework
        string model_format
        uuid training_dataset_id FK
        json training_config
        json metrics
        datetime created_at
        datetime updated_at
    }
    
    pipelines ||--o{ pipeline_stages : contains
    pipelines ||--o{ pipeline_runs : executes
    pipeline_runs ||--o{ stage_runs : contains
    pipeline_stages ||--o{ stage_runs : executes
    pipeline_stages ||--o{ artifacts : produces
    stage_runs ||--o{ artifacts : generates
    artifacts ||--o| datasets : specializes
    artifacts ||--o| models : specializes
    datasets ||--o{ models : trains
```

### Stage Types

The system supports various stage types for different ML pipeline phases:

#### Data Pipeline Stages
- `DATA_INGESTION` - Load data from various sources
- `DATA_VALIDATION` - Validate data quality and schema
- `DATA_PREPROCESSING` - Clean and transform data
- `FEATURE_ENGINEERING` - Create new features
- `DATA_SPLITTING` - Split data into train/validation/test sets

#### Model Pipeline Stages
- `MODEL_TRAINING` - Train machine learning models
- `MODEL_VALIDATION` - Validate model performance
- `MODEL_EVALUATION` - Evaluate model on test data
- `MODEL_TESTING` - Comprehensive model testing

#### Deployment Pipeline Stages
- `MODEL_REGISTRATION` - Register models in model registry
- `MODEL_DEPLOYMENT` - Deploy models to production
- `MODEL_MONITORING` - Monitor deployed models

#### Analysis Stages
- `EXPLORATORY_DATA_ANALYSIS` - EDA and data exploration
- `HYPERPARAMETER_TUNING` - Optimize model hyperparameters
- `MODEL_COMPARISON` - Compare different models

#### Infrastructure Stages
- `ENVIRONMENT_SETUP` - Set up execution environment
- `RESOURCE_PROVISIONING` - Provision compute resources
- `CLEANUP` - Clean up resources after execution

#### Custom Stages
- `CUSTOM` - User-defined custom stages

### Artifact Types

The system supports various artifact types produced by pipeline stages:

- `MODEL` - Trained machine learning models
- `DATASET` - Processed datasets and data files
- `METRICS` - Performance metrics and evaluation results
- `PLOT` - Visualizations and charts
- `LOG` - Execution logs and debugging information
- `CONFIG` - Configuration files and settings
- `REPORT` - Analysis reports and documentation
- `OTHER` - Miscellaneous artifacts

### Storage Types

Artifacts can be stored in different storage backends:

- `LOCAL` - Local file system storage
- `S3` - Amazon S3 storage
- `GCS` - Google Cloud Storage
- `AZURE` - Azure Blob Storage
