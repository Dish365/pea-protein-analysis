# Implement OPEX-related API endpoints

from fastapi import APIRouter, HTTPException
import logging

from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis
from backend.fastapi_app.models.economic_analysis import (
    OpexInput, Utility, RawMaterial, LaborConfig, EconomicFactors
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Operational Expenditure"])


@router.post("/calculate")
async def calculate_opex(input_data: OpexInput):
    """Calculate total operational expenditure and its components"""
    try:
        logger.debug(f"Received OPEX calculation request with data: {input_data}")

        # Initialize OPEX analysis
        opex_analysis = OperationalExpenditureAnalysis()
        logger.debug("Initialized OperationalExpenditureAnalysis")

        # Add utilities
        for utility in input_data.utilities:
            logger.debug(f"Processing utility: {utility}")
            opex_analysis.add_utility(utility.dict())

        # Add raw materials
        for material in input_data.raw_materials:
            logger.debug(f"Processing raw material: {material}")
            opex_analysis.add_raw_material(material.dict())

        # Set labor data
        logger.debug(f"Setting labor data: {input_data.labor_config}")
        opex_analysis.set_labor_data(input_data.labor_config.dict())

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
        logger.debug(f"OPEX calculation result: {opex_result}")

        # Get detailed breakdowns
        utilities_breakdown = opex_analysis.get_utilities_breakdown()
        raw_materials_breakdown = opex_analysis.get_raw_materials_breakdown()
        labor_breakdown = opex_analysis.get_labor_breakdown()
        
        logger.debug(f"Utilities breakdown: {utilities_breakdown}")
        logger.debug(f"Raw materials breakdown: {raw_materials_breakdown}")
        logger.debug(f"Labor breakdown: {labor_breakdown}")

        result = {
            "opex_summary": opex_result,
            "utilities_breakdown": utilities_breakdown,
            "raw_materials_breakdown": raw_materials_breakdown,
            "labor_breakdown": labor_breakdown,
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume
        }
        logger.debug(f"Final response: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in OPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for OPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )
