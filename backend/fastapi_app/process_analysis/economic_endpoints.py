from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from analytics.economic.services.cost_tracking import CostTracker
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Economic Analysis"])
cost_tracker = CostTracker()

@router.get("/cost-tracking")
async def get_cost_tracking(
    start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
):
    """
    Get cost tracking summary and trends
    """
    try:
        logger.debug(f"Retrieving cost tracking data with start_date={start_date}, end_date={end_date}")
        
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must be before end date")
            
        summary = cost_tracker.get_cost_summary(start_date, end_date)
        trends = cost_tracker.get_cost_trends()
        
        logger.debug(f"Successfully retrieved cost tracking data: summary={summary}, trends={trends}")
        return {"cost_summary": summary, "cost_trends": trends}

    except ValueError as e:
        logger.error(f"Validation error in cost tracking: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving cost tracking data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})
