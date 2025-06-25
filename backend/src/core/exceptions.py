from typing import Optional


class APIException(Exception):
    """Base API exception class"""

    def __init__(
        self, detail: str, status_code: int = 400, error_type: str = "api_error"
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_type = error_type
        super().__init__(self.detail)


class PipelineNotFoundError(APIException):
    def __init__(self, pipeline_id: str):
        super().__init__(
            detail=f"Pipeline with id {pipeline_id} not found",
            status_code=404,
            error_type="pipeline_not_found",
        )


class PipelineRunNotFoundError(APIException):
    def __init__(self, run_id: str):
        super().__init__(
            detail=f"Pipeline run with id {run_id} not found",
            status_code=404,
            error_type="run_not_found",
        )


class PipelineValidationError(APIException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=422, error_type="validation_error")


class PipelineExecutionError(APIException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=500, error_type="execution_error")


class DatabaseError(APIException):
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(detail=detail, status_code=500, error_type="database_error")
