from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging

from analytics.economic.services.metrics import get_economic_metrics
from .services.rust_handler import RustHandler
from analytics.economic.services.cost_estimation import (
    estimate_total_investment,
    estimate_annual_costs,
)
from analytics.economic.profitability.mcsp import (
    perform_sensitivity_analysis,
)

from analytics.economic.services.cost_tracking import CostTracker

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Profitability Analysis"])
rust_handler = RustHandler()

class ProfitabilityAnalysisInput(BaseModel):
    cash_flows: List[float]
    discount_rate: float
    initial_investment: float
    gain_from_investment: float
    cost_of_investment: float
    production_volume: float
    monte_carlo_iterations: Optional[int] = 1000
    uncertainty: Optional[float] = 0.1

class ComprehensiveAnalysisInput(BaseModel):
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

# Initialize services
cost_tracker = CostTracker()

@router.post("/analyze")
async def analyze_profitability_metrics(input_data: ProfitabilityAnalysisInput):
    """Calculate profitability metrics for the investment including Monte Carlo simulation"""
    try:
        logger.debug(f"Received profitability analysis request with data: {input_data}")
        
        # Get base economic metrics
        metrics = get_economic_metrics(
            cash_flows=input_data.cash_flows,
            discount_rate=input_data.discount_rate,
            initial_investment=input_data.initial_investment,
            gain_from_investment=input_data.gain_from_investment,
            cost_of_investment=input_data.cost_of_investment,
            production_volume=input_data.production_volume
        )
        
        # Track investment costs
        cost_tracker.track_costs({
            "initial_investment": input_data.initial_investment,
            "cost_of_investment": input_data.cost_of_investment
        })
        
        # Run Monte Carlo simulation if requested
        if input_data.monte_carlo_iterations > 0:
            monte_carlo_results = rust_handler.run_monte_carlo_simulation(
                cash_flows=input_data.cash_flows,
                discount_rate=input_data.discount_rate,
                initial_investment=input_data.initial_investment,
                iterations=input_data.monte_carlo_iterations,
                uncertainty=input_data.uncertainty
            )
            
            result = {
                "metrics": metrics,
                "monte_carlo": monte_carlo_results
            }
        else:
            result = {
                "metrics": metrics
            }
            
        logger.debug(f"Final response: {result}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as e:
        logger.error(f"Error in profitability analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})

@router.post("")
async def analyze_comprehensive_profitability(input_data: ComprehensiveAnalysisInput):
    """Calculate comprehensive economic metrics including investment costs and profitability"""
    try:
        # Calculate total investment
        investment = estimate_total_investment(
            equipment_costs=input_data.capex["equipment_cost"],
            installation_costs=input_data.capex["installation_cost"],
            indirect_costs=input_data.capex["indirect_cost"]
        )

        # Calculate annual costs
        annual_costs = estimate_annual_costs(
            capex=investment["total_investment"],
            opex=input_data.opex,
            project_years=input_data.project_duration,
            interest_rate=input_data.discount_rate
        )

        # Track costs
        cost_tracker.track_costs({
            **investment,
            **annual_costs
        })

        # Calculate profitability metrics
        metrics = get_economic_metrics(
            cash_flows=input_data.cash_flows,
            discount_rate=input_data.discount_rate,
            initial_investment=investment["total_investment"],
            gain_from_investment=sum(input_data.cash_flows[1:]),  # Exclude initial investment
            cost_of_investment=investment["total_investment"],
            production_volume=input_data.production_volume
        )

        return {
            "investment_analysis": investment,
            "annual_costs": annual_costs,
            "profitability_metrics": metrics
        }

    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})

@router.post("/sensitivity")
async def analyze_sensitivity(input_data: SensitivityAnalysisInput):
    """Perform sensitivity analysis on economic metrics"""
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
