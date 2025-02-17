from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from analytics.economic.services.cost_tracking import CostTracker
from backend.fastapi_app.models.economic_analysis import (
    ComprehensiveAnalysisInput, EconomicFactors
)
from .services.profitability_service import ProfitabilityService
from .utils.error_handling import handle_analysis_error

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Profitability Analysis"])

# Initialize services
profitability_service = ProfitabilityService()

class SensitivityAnalysisInput(BaseModel):
    """Input model for sensitivity analysis"""
    base_cash_flows: List[float]
    variables: List[str] = ["discount_rate", "production_volume", "operating_costs", "revenue"]
    ranges: Dict[str, tuple] = {
        "discount_rate": (0.05, 0.15),
        "production_volume": (500.0, 1500.0),
        "operating_costs": (0.8, 1.2),
        "revenue": (0.8, 1.2)
    }
    steps: Optional[int] = 10

async def get_cost_tracker():
    """Dependency injection for cost tracker"""
    return CostTracker()

@router.post("/analyze")
async def analyze_profitability(
    input_data: ComprehensiveAnalysisInput,
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> Dict[str, Any]:
    """
    Perform comprehensive profitability analysis including CAPEX, OPEX, and profitability metrics.
    """
    try:
        result = await profitability_service.analyze_comprehensive(input_data)
        
        # Track analysis in cost tracker
        cost_tracker.track_costs({
            "type": "profitability_analysis",
            "process_type": input_data.process_type,
            "timestamp": datetime.now().isoformat(),
            "metrics": result["profitability_metrics"]
        })
        
        return result
    except Exception as e:
        return handle_analysis_error(e, "profitability analysis")

@router.post("/sensitivity")
async def analyze_sensitivity(input_data: SensitivityAnalysisInput) -> Dict[str, Any]:
    """Perform sensitivity analysis on economic metrics"""
    try:
        return await profitability_service.analyze_sensitivity(input_data)
    except Exception as e:
        return handle_analysis_error(e, "sensitivity analysis")

@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for profitability calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0,
        installation_factor=0.3,
        indirect_costs_factor=0.45,
        maintenance_factor=0.02
    )

@router.get("/costs/summary")
async def get_cost_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    cost_tracker: CostTracker = Depends(get_cost_tracker)
) -> Dict[str, Any]:
    """Get summary of tracked costs"""
    try:
        summary = cost_tracker.get_cost_summary(start_date, end_date)
        trends = cost_tracker.get_cost_trends()
        
        return {
            "summary": summary,
            "trends": trends
        }
    except Exception as e:
        return handle_analysis_error(e, "cost summary")
