from fastapi import HTTPException
import logging
from typing import Any

logger = logging.getLogger(__name__)

def handle_analysis_error(error: Exception, analysis_type: str) -> Any:
    """
    Consistent error handling for analysis endpoints
    
    Args:
        error: The caught exception
        analysis_type: Type of analysis being performed (for logging)
        
    Raises:
        HTTPException: With appropriate status code and error details
    """
    if isinstance(error, ValueError):
        logger.error(f"Validation error in {analysis_type}: {str(error)}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Validation error",
                "message": str(error),
                "analysis_type": analysis_type
            }
        )
    else:
        logger.error(f"Error in {analysis_type}: {str(error)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(error),
                "analysis_type": analysis_type
            }
        ) 