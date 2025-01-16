from typing import Any, Callable, Dict, Optional
import asyncio
import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Base class for analysis errors"""

    def __init__(self, message: str, error_code: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class ValidationError(AnalysisError):
    """Error for input validation failures"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class ComputationError(AnalysisError):
    """Error for computation failures"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "COMPUTATION_ERROR", details)


class IntegrationError(AnalysisError):
    """Error for integration failures"""

    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, "INTEGRATION_ERROR", details)


def handle_error(error: Exception) -> Dict[str, Any]:
    """Convert exception to standardized error response"""
    if isinstance(error, AnalysisError):
        error_response = {
            "error_code": error.error_code,
            "message": str(error),
            "details": error.details,
            "timestamp": error.timestamp.isoformat(),
        }
    else:
        error_response = {
            "error_code": "UNKNOWN_ERROR",
            "message": str(error),
            "details": {"type": type(error).__name__},
            "timestamp": datetime.utcnow().isoformat(),
        }

    logger.error(f"Error occurred: {error_response}")
    return {"error": error_response}


async def retry_operation(
    operation: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> Any:
    """Retry an operation with exponential backoff"""
    last_error = None
    current_delay = delay

    for attempt in range(max_retries):
        try:
            return operation()
        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

            if attempt < max_retries - 1:
                await asyncio.sleep(current_delay)
                current_delay *= backoff_factor

    logger.error(f"Operation failed after {max_retries} attempts")
    raise last_error


def validate_input(required_fields: Dict[str, type]):
    """Decorator for input validation"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            input_data = kwargs.get("input_data") or args[-1]

            for field, field_type in required_fields.items():
                if field not in input_data:
                    raise ValidationError(
                        f"Missing required field: {field}",
                        {"field": field, "required_type": str(field_type)},
                    )

                if not isinstance(input_data[field], field_type):
                    raise ValidationError(
                        f"Invalid type for field: {field}",
                        {
                            "field": field,
                            "expected_type": str(field_type),
                            "received_type": str(type(input_data[field])),
                        },
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_execution_time(logger_name: str = __name__):
    """Decorator to log function execution time"""
    logger = logging.getLogger(logger_name)

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            try:
                result = await func(*args, **kwargs)
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
                return result
            except Exception as e:
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                logger.error(
                    f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}"
                )
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
                return result
            except Exception as e:
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                logger.error(
                    f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}"
                )
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
