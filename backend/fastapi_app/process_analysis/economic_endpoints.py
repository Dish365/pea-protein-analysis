from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

from analytics.economic.services.cost_estimation import (
    estimate_total_investment,
    estimate_annual_costs,
)
from analytics.economic.services.cost_tracking import CostTracker
from analytics.economic.profitability.mcsp import (
    calculate_mcsp,
    perform_sensitivity_analysis,
)
from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period

router = APIRouter()
cost_tracker = CostTracker()


class EconomicAnalysisInput(BaseModel):
    capex: Dict[str, float]
    opex: Dict[str, float]
    production_volume: float
    project_duration: int
    discount_rate: float
    cash_flows: List[float]


class SensitivityAnalysisInput(BaseModel):
    base_cash_flows: List[float]
    discount_rate: float
    production_volume: float
    sensitivity_range: Optional[float] = 0.2
    steps: Optional[int] = 10


@router.post("/economic/profitability/")
async def analyze_profitability(input_data: EconomicAnalysisInput):
    """
    Calculate comprehensive economic metrics including NPV, ROI, payback period, and MCSP
    """
    try:
        # Calculate total investment
        total_investment = estimate_total_investment(
            input_data.capex.get("equipment", 0),
            input_data.capex.get("installation", 0),
            input_data.capex.get("indirect", 0),
        )

        # Calculate annual costs
        annual_costs = estimate_annual_costs(
            sum(input_data.capex.values()),
            input_data.opex,
            input_data.project_duration,
            input_data.discount_rate,
        )

        # Calculate profitability metrics
        npv = calculate_npv(input_data.cash_flows, input_data.discount_rate)
        roi = calculate_roi(sum(input_data.cash_flows), sum(input_data.capex.values()))
        payback = calculate_payback_period(
            sum(input_data.capex.values()), input_data.cash_flows
        )

        # Calculate MCSP
        mcsp_result = calculate_mcsp(
            input_data.cash_flows,
            input_data.discount_rate,
            input_data.production_volume,
        )

        # Track costs
        cost_tracker.track_costs(
            {
                "capex": sum(input_data.capex.values()),
                "opex": sum(input_data.opex.values()),
                "total_investment": total_investment["total_investment"],
            }
        )

        return {
            "total_investment": total_investment,
            "annual_costs": annual_costs,
            "npv": npv,
            "roi": roi,
            "payback_period": payback,
            "mcsp": mcsp_result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/economic/sensitivity/")
async def analyze_sensitivity(input_data: SensitivityAnalysisInput):
    """
    Perform sensitivity analysis on economic metrics
    """
    try:
        sensitivity_results = perform_sensitivity_analysis(
            input_data.base_cash_flows,
            input_data.discount_rate,
            input_data.production_volume,
            input_data.sensitivity_range,
            input_data.steps,
        )

        return {"sensitivity_analysis": sensitivity_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economic/cost-tracking/")
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
