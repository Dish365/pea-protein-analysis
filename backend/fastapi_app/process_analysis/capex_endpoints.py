from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from backend.fastapi_app.models.economic_analysis import (
    CapexInput, EconomicFactors, IndirectFactor
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Capital Expenditure"])

def get_default_indirect_factors(equipment_cost: float) -> List[Dict[str, Any]]:
    """Get default indirect factors based on equipment cost"""
    return [
        {
            "name": "engineering",
            "cost": equipment_cost,
            "percentage": 0.15
        },
        {
            "name": "contingency",
            "cost": equipment_cost,
            "percentage": 0.10
        },
        {
            "name": "construction",
            "cost": equipment_cost,
            "percentage": 0.20
        }
    ]

def validate_indirect_factor(factor: Dict[str, Any]) -> bool:
    """Validate a single indirect factor"""
    try:
        # Convert dict to IndirectFactor model for validation
        IndirectFactor(**factor)
        return True
    except Exception as e:
        logger.debug(f"Invalid indirect factor: {factor}. Error: {str(e)}")
        return False

@router.post("/calculate")
async def calculate_capex(input_data: CapexInput) -> Dict[str, Any]:
    """Calculate total capital expenditure and its components"""
    try:
        logger.info(f"Received CAPEX calculation request for process type: {input_data.process_type}")
        
        # Initialize CAPEX analysis
        capex_analysis = CapitalExpenditureAnalysis()
        
        # Add equipment
        for equipment in input_data.equipment_list:
            capex_analysis.add_equipment(equipment.model_dump())
        logger.debug(f"Added {len(input_data.equipment_list)} equipment items")
        
        # Handle indirect factors
        factors_source = "default"
        equipment_cost = sum(eq.base_cost for eq in input_data.equipment_list)
        indirect_factors = get_default_indirect_factors(equipment_cost)
        
        if input_data.indirect_factors:
            indirect_factors = [factor.model_dump() for factor in input_data.indirect_factors]
            factors_source = "user"
            logger.info("Using user-provided indirect factors")
        
        # Calculate total CAPEX
        capex_result = capex_analysis.calculate_total_capex(
            installation_factor=input_data.economic_factors.installation_factor,
            indirect_costs_factor=input_data.economic_factors.indirect_costs_factor,
            indirect_factors=indirect_factors
        )
        
        # Format response
        response = {
            "capex_summary": {
                "total_capex": capex_result["total_capex"],
                "equipment_costs": capex_result["equipment_costs"],
                "installation_costs": capex_result["installation_costs"],
                "indirect_costs": capex_result["indirect_costs"]
            },
            "equipment_breakdown": capex_result["equipment_breakdown"],
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume,
            "indirect_factors": {
                "source": factors_source,
                "factors": capex_result["indirect_factors"]
            }
        }
        
        logger.info(f"CAPEX calculation successful for {input_data.process_type}")
        return response

    except ValueError as ve:
        logger.error(f"Validation error in CAPEX calculation: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in CAPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for CAPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )