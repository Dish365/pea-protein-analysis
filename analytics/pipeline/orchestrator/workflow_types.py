from enum import Enum
from typing import List
import logging

logger = logging.getLogger(__name__)

class WorkflowType(str, Enum):
    """Workflow types supported by the pipeline"""
    BASELINE = "baseline"
    RF_TREATMENT = "rf_treatment" 
    IR_TREATMENT = "ir_treatment"

    @classmethod
    def values(cls) -> List[str]:
        """Get list of valid workflow type values"""
        return [member.value for member in cls]

    @classmethod 
    def from_str(cls, value: str) -> 'WorkflowType':
        """Convert string to WorkflowType, case-insensitive"""
        try:
            logger.debug(f"Converting string '{value}' to WorkflowType")
            logger.debug(f"Available workflow types: {cls.values()}")
            
            normalized_value = value.lower().strip()
            logger.debug(f"Normalized value: '{normalized_value}'")
            
            for member in cls:
                logger.debug(f"Checking against member: {member.value}")
                if member.value == normalized_value:
                    logger.debug(f"Match found: {member}")
                    return member
                
            error_msg = f"Invalid workflow type: '{value}'"
            logger.error(f"{error_msg}. Valid types are: {cls.values()}")
            raise ValueError(error_msg)
            
        except Exception as e:
            logger.error(f"Error converting workflow type: {str(e)}")
            raise ValueError(
                f"Invalid workflow type: '{value}'. "
                f"Valid types are: {cls.values()}"
            ) 