from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from backend.fastapi_app.models.economic_analysis import CapexInput, EconomicFactors, IndirectFactor

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
async def calculate_capex(input_data: CapexInput):
    """Calculate total capital expenditure and its components"""
    try:
        # Ensure we have equipment data and it's properly formatted
        if not input_data.equipment_list:
            raise ValueError("Equipment list cannot be empty")
        
        # Validate equipment data
        for equipment in input_data.equipment_list:
            if not isinstance(equipment.cost, (int, float)) or equipment.cost <= 0:
                raise ValueError(f"Invalid cost for equipment {equipment.name}: {equipment.cost}")
            if not isinstance(equipment.efficiency, (int, float)) or not 0 < equipment.efficiency <= 1:
                raise ValueError(f"Invalid efficiency for equipment {equipment.name}: {equipment.efficiency}")
            if not isinstance(equipment.processing_capacity, (int, float)) or equipment.processing_capacity <= 0:
                raise ValueError(f"Invalid processing capacity for equipment {equipment.name}: {equipment.processing_capacity}")
            
        # Get equipment cost
        equipment_cost = sum(eq.cost for eq in input_data.equipment_list)
        
        # Track source of factors used
        factors_source = "default"
        
        # Always start with default factors
        valid_factors = get_default_indirect_factors(equipment_cost)
        
        # Override with valid user-provided factors if any exist
        if input_data.indirect_factors:
            user_factors = [
                factor.dict() for factor in input_data.indirect_factors 
                if validate_indirect_factor(factor.dict())
            ]
            if user_factors:
                valid_factors = user_factors
                factors_source = "user"
                logger.info("Using user-provided indirect factors")
            else:
                logger.info("Invalid user factors provided, using defaults")
        
        # Initialize CAPEX analysis
        capex_analysis = CapitalExpenditureAnalysis()

        # Add equipment - ensure we convert Pydantic models to dicts with proper types
        for equipment in input_data.equipment_list:
            capex_analysis.add_equipment({
                "name": str(equipment.name),
                "cost": float(equipment.cost),
                "efficiency": float(equipment.efficiency),
                "maintenance_cost": float(equipment.maintenance_cost),
                "energy_consumption": float(equipment.energy_consumption),
                "processing_capacity": float(equipment.processing_capacity)
            })

        # Calculate total CAPEX
        capex_result = capex_analysis.calculate_total_capex(
            installation_factor=float(input_data.economic_factors.installation_factor),
            indirect_costs_factor=float(input_data.economic_factors.indirect_costs_factor),
            indirect_factors=valid_factors
        )

        # Get detailed breakdowns
        equipment_breakdown = capex_analysis.get_equipment_breakdown()

        # Format the response
        response = {
            "capex_summary": {
                "total_capex": float(capex_result["total_capex"]),
                "equipment_costs": float(capex_result["equipment_costs"]),
                "installation_costs": float(capex_result["installation_costs"]),
                "indirect_costs": float(capex_result["indirect_costs"])
            },
            "equipment_breakdown": equipment_breakdown,
            "process_type": input_data.process_type,
            "production_volume": float(input_data.economic_factors.production_volume),
            "indirect_factors": {
                "source": factors_source,
                "factors": valid_factors
            }
        }

        logger.info(f"CAPEX calculation successful: {response}")
        return response

    except ValueError as ve:
        logger.error(f"Validation error in CAPEX calculation: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in CAPEX calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for CAPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )