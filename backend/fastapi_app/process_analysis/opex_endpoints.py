# Implement OPEX-related API endpoints

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis, EmptyDataError
from backend.fastapi_app.models.economic_analysis import (
    OpexInput, EconomicFactors
)

# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Operational Expenditure"])


@router.post("/calculate")
async def calculate_opex(input_data: OpexInput) -> Dict[str, Any]:
    """
    Calculate total operational expenditure and its components
    
    Args:
        input_data: OpexInput model containing all required OPEX calculation data
        
    Returns:
        Dictionary containing OPEX calculations and breakdowns
        
    Raises:
        HTTPException: If validation fails or calculation errors occur
    """
    try:
        logger.info(f"Received OPEX calculation request for process type: {input_data.process_type}")

        # Initialize OPEX analysis
        opex_analysis = OperationalExpenditureAnalysis()
        logger.debug("Initialized OperationalExpenditureAnalysis")

        # Add utilities
        for utility in input_data.utilities:
            logger.debug(f"Processing utility: {utility.name}")
            opex_analysis.add_utility(utility.model_dump())

        # Add raw materials
        for material in input_data.raw_materials:
            logger.debug(f"Processing raw material: {material.name}")
            opex_analysis.add_raw_material(material.model_dump())

        # Set labor data
        logger.debug(f"Setting labor data for {input_data.labor_config.num_workers} workers")
        opex_analysis.set_labor_data(input_data.labor_config.model_dump())

        # Set maintenance factors
        maintenance_data = {
            "equipment_cost": input_data.equipment_costs,
            "maintenance_factor": input_data.economic_factors.maintenance_factor
        }
        logger.debug(f"Setting maintenance factors: {maintenance_data}")
        opex_analysis.set_maintenance_factors(maintenance_data)

        # Calculate total OPEX
        logger.debug("Calculating total OPEX")
        opex_result = opex_analysis.calculate_total_opex()
        logger.debug(f"OPEX calculation completed")

        # Format response
        response = {
            "opex_summary": {
                "total_opex": opex_result["total_opex"],
                "raw_material_costs": opex_result["raw_material_costs"],
                "utility_costs": opex_result["utility_costs"],
                "labor_costs": opex_result["labor_costs"],
                "maintenance_costs": opex_result["maintenance_costs"]
            },
            "breakdowns": {
                "raw_materials": opex_result["raw_materials_breakdown"],
                "utilities": opex_result["utilities_breakdown"],
                "labor": opex_result["labor_breakdown"]
            },
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume
        }

        logger.info(f"OPEX calculation successful for {input_data.process_type}")
        return response

    except EmptyDataError as ede:
        logger.error(f"Missing required data in OPEX calculation: {str(ede)}")
        raise HTTPException(
            status_code=422,
            detail={"error": "Missing required data", "message": str(ede)}
        )
    except ValueError as ve:
        logger.error(f"Validation error in OPEX calculation: {str(ve)}")
        raise HTTPException(
            status_code=422,
            detail={"error": "Validation error", "message": str(ve)}
        )
    except Exception as e:
        logger.error(f"Error in OPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for OPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0,
        maintenance_factor=0.05,
        installation_factor=0.2,  # Not used in OPEX but required by model
        indirect_costs_factor=0.15  # Not used in OPEX but required by model
    )
