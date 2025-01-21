from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import numpy as np
import math
from datetime import datetime

from analytics.economic.profitability_analyzer import ProfitabilityAnalysis, ProjectParameters
from analytics.economic.services.cost_estimation import (
    estimate_total_investment,
    estimate_annual_costs,
)
from analytics.economic.services.cost_tracking import CostTracker
from backend.fastapi_app.models.economic_analysis import (
    ProfitabilityInput, EconomicFactors
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Profitability Analysis"])

# Initialize services
cost_tracker = CostTracker()
profitability_analyzer = ProfitabilityAnalysis()

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
    """Input model for sensitivity analysis"""
    base_cash_flows: List[float]
    discount_rate: float
    production_volume: float
    sensitivity_range: Optional[float] = 0.2
    steps: Optional[int] = 10

@router.post("/analyze")
async def analyze_profitability_metrics(input_data: ProfitabilityInput):
    """Calculate profitability metrics including Monte Carlo simulation"""
    try:
        logger.debug(f"Received profitability analysis request with data: {input_data}")
        
        # Set up project parameters
        parameters = ProjectParameters(
            discount_rate=input_data.economic_factors.discount_rate,
            project_duration=input_data.economic_factors.project_duration,
            production_volume=input_data.economic_factors.production_volume,
            monte_carlo_iterations=input_data.monte_carlo_iterations,
            uncertainty=input_data.uncertainty
        )
        
        # Set project data in analyzer
        profitability_analyzer.set_project_data(
            capex=input_data.capex,
            opex=input_data.opex,
            revenue={"year_" + str(i): cf for i, cf in enumerate(input_data.cash_flows)},
            parameters=parameters
        )
        
        # Track costs with better structure
        cost_tracker.track_costs({
            "type": "profitability_analysis",
            "capex": {
                "total_investment": input_data.capex["total_investment"],
                "equipment_cost": input_data.capex.get("equipment_cost", 0),
                "installation_cost": input_data.capex.get("installation_cost", 0),
                "indirect_cost": input_data.capex.get("indirect_cost", 0)
            },
            "opex": {
                "total_annual_cost": input_data.opex["total_annual_cost"],
                **input_data.opex  # Include any additional opex details
            },
            "parameters": {
                "discount_rate": input_data.economic_factors.discount_rate,
                "project_duration": input_data.economic_factors.project_duration,
                "production_volume": input_data.economic_factors.production_volume
            }
        })
        
        # Calculate metrics using Rust implementation if Monte Carlo requested
        use_rust = input_data.monte_carlo_iterations > 0
        metrics = profitability_analyzer.calculate_profitability_metrics(
            use_rust=use_rust,
            target_npv=0.0  # For MCSP calculation
        )
        
        # Sanitize results before returning
        sanitized_metrics = sanitize_dict(metrics)
        
        # Ensure ROI values are properly sanitized
        if 'roi' in sanitized_metrics:
            roi_metrics = sanitized_metrics['roi']
            if isinstance(roi_metrics, dict):
                if 'annualized_roi' in roi_metrics and isinstance(roi_metrics['annualized_roi'], complex):
                    roi_metrics['annualized_roi'] = abs(roi_metrics['annualized_roi'])
        
        result = {
            "metrics": sanitized_metrics,
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume
        }
            
        logger.debug(f"Final response: {result}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as e:
        logger.error(f"Error in profitability analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})

def sanitize_float(value: Any) -> float:
    """Convert numpy floats to Python floats and handle NaN/Infinity/complex values"""
    if isinstance(value, complex):
        return abs(value)  # Return magnitude of complex number
    if isinstance(value, (np.floating, float)):
        if math.isnan(value) or math.isinf(value):
            return 0.0
        return float(value)
    return value

def sanitize_dict(d: Dict) -> Dict:
    """Recursively sanitize dictionary values"""
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = sanitize_dict(v)
        elif isinstance(v, (list, tuple)):
            result[k] = [sanitize_float(x) if isinstance(x, (np.floating, float)) else x for x in v]
        else:
            result[k] = sanitize_float(v)
    return result

@router.post("")
async def analyze_comprehensive_profitability(input_data: ComprehensiveAnalysisInput):
    """Calculate comprehensive economic metrics including investment costs and profitability"""
    try:
        # Calculate investments and costs first
        total_investment = estimate_total_investment(
            equipment_costs=input_data.capex.get("equipment_cost", 0),
            installation_costs=input_data.capex.get("installation_cost", 0),
            indirect_costs=input_data.capex.get("indirect_cost", 0)
        )
        
        annual_costs = estimate_annual_costs(
            capex=total_investment["total_investment"],
            opex=input_data.opex,
            project_years=input_data.project_duration,
            interest_rate=input_data.discount_rate
        )

        # Track costs with comprehensive structure
        cost_tracker.track_costs({
            "type": "comprehensive_analysis",
            "investment": total_investment,
            "annual": annual_costs,
            "parameters": {
                "project_duration": input_data.project_duration,
                "discount_rate": input_data.discount_rate,
                "production_volume": input_data.production_volume
            }
        })

        # Set up project parameters for analysis
        parameters = ProjectParameters(
            discount_rate=input_data.discount_rate,
            project_duration=input_data.project_duration,
            production_volume=input_data.production_volume
        )
        
        # Set project data in analyzer
        profitability_analyzer.set_project_data(
            capex={"total_investment": total_investment["total_investment"]},
            opex={"total_annual_cost": annual_costs["total_annual_cost"]},
            revenue={"year_" + str(i): cf for i, cf in enumerate(input_data.cash_flows)},
            parameters=parameters
        )

        # Calculate profitability metrics
        metrics = profitability_analyzer.calculate_profitability_metrics(use_rust=False)

        # Sanitize and structure the response
        result = {
            "investment_analysis": sanitize_dict(total_investment),
            "annual_costs": sanitize_dict(annual_costs),
            "profitability_metrics": sanitize_dict(metrics)
        }

        return result

    except ValueError as e:
        logger.error(f"Validation error in comprehensive analysis: {str(e)}")
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)})

@router.post("/sensitivity")
async def analyze_sensitivity(input_data: SensitivityAnalysisInput):
    """Perform sensitivity analysis on economic metrics"""
    try:
        if not input_data.base_cash_flows:
            raise HTTPException(
                status_code=400,
                detail="Base cash flows are required for sensitivity analysis"
            )

        # Set up project parameters
        parameters = ProjectParameters(
            discount_rate=input_data.discount_rate,
            project_duration=len(input_data.base_cash_flows) - 1,  # Subtract 1 for initial investment
            production_volume=input_data.production_volume,
            uncertainty=0.1  # Default value
        )
        
        # Calculate initial cash flows for base case
        initial_investment = abs(input_data.base_cash_flows[0])  # First value is initial investment
        annual_cash_flows = input_data.base_cash_flows[1:]  # Rest are annual flows
        
        # Initialize a new analyzer instance for this request
        analyzer = ProfitabilityAnalysis()
        
        # Set up analyzer with base case data
        analyzer.set_project_data(
            capex={"total_investment": initial_investment},
            opex={"total_annual_cost": sum(cf for cf in annual_cash_flows if cf < 0)},  # Sum negative flows as costs
            revenue={"year_" + str(i): cf for i, cf in enumerate(annual_cash_flows)},
            parameters=parameters
        )

        # Perform sensitivity analysis
        sensitivity_results = analyzer.perform_sensitivity_analysis(
            variables=["discount_rate", "production_volume"],
            ranges={
                "discount_rate": (input_data.discount_rate * (1 - input_data.sensitivity_range),
                                input_data.discount_rate * (1 + input_data.sensitivity_range)),
                "production_volume": (input_data.production_volume * (1 - input_data.sensitivity_range),
                                   input_data.production_volume * (1 + input_data.sensitivity_range))
            },
            use_rust=True
        )

        # Sanitize and return results
        return {"sensitivity_analysis": sanitize_dict(sensitivity_results)}

    except ValueError as e:
        logger.error(f"Validation error in sensitivity analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in sensitivity analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for profitability calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )

@router.get("/costs/summary")
async def get_cost_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """Get summary of tracked costs"""
    try:
        summary = cost_tracker.get_cost_summary(start_date, end_date)
        trends = cost_tracker.get_cost_trends()
        
        return {
            "summary": sanitize_dict(summary),
            "trends": sanitize_dict(trends)
        }
    except Exception as e:
        logger.error(f"Error getting cost summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
