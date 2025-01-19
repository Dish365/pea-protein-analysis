from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from analytics.economic.services.cost_tracking import CostTracker

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
        summary = cost_tracker.get_cost_summary(start_date, end_date)
        trends = cost_tracker.get_cost_trends()

        return {"cost_summary": summary, "cost_trends": trends}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
