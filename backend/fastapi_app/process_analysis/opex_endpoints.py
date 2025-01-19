# Implement OPEX-related API endpoints

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging

from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Operational Expenditure"])


class Utility(BaseModel):
    name: str
    consumption: float
    unit_price: float
    unit: str


class RawMaterial(BaseModel):
    name: str
    quantity: float
    unit_price: float
    unit: str


class LaborConfig(BaseModel):
    hourly_wage: float
    hours_per_week: float
    weeks_per_year: float
    num_workers: int


class OpexAnalysisInput(BaseModel):
    utilities: List[Utility]
    raw_materials: List[RawMaterial]
    equipment_costs: float
    labor_config: LaborConfig
    maintenance_factor: Optional[float] = 0.05


@router.post("/calculate")
async def calculate_opex(input_data: OpexAnalysisInput):
    """
    Calculate total operational expenditure and its components
    """
    try:
        logger.debug(f"Received OPEX calculation request with data: {input_data}")

        # Initialize OPEX analysis
        opex_analysis = OperationalExpenditureAnalysis()
        logger.debug("Initialized OperationalExpenditureAnalysis")

        # Add utilities
        for utility in input_data.utilities:
            utility_data = utility.dict()
            utility_data.update({
                "consumption": float(utility.consumption),
                "unit_price": float(utility.unit_price)
            })
            logger.debug(f"Processing utility: {utility_data}")
            opex_analysis.add_utility(utility_data)

        # Add raw materials
        for material in input_data.raw_materials:
            material_data = material.dict()
            material_data.update({
                "quantity": float(material.quantity),
                "unit_price": float(material.unit_price)
            })
            logger.debug(f"Processing raw material: {material_data}")
            opex_analysis.add_raw_material(material_data)

        # Set labor data
        labor_data = {
            "hourly_wage": float(input_data.labor_config.hourly_wage),
            "hours_per_week": float(input_data.labor_config.hours_per_week),
            "weeks_per_year": float(input_data.labor_config.weeks_per_year),
            "num_workers": float(input_data.labor_config.num_workers)
        }
        logger.debug(f"Setting labor data: {labor_data}")
        opex_analysis.set_labor_data(labor_data)

        # Set maintenance factors
        maintenance_factors = {
            "equipment_cost": float(input_data.equipment_costs),
            "maintenance_factor": float(input_data.maintenance_factor)
        }
        logger.debug(f"Setting maintenance factors: {maintenance_factors}")
        opex_analysis.set_maintenance_factors(maintenance_factors)

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
            "labor_breakdown": labor_breakdown
        }
        logger.debug(f"Final response: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in OPEX calculation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/factors")
async def get_default_factors():
    """
    Get default factors for OPEX calculations
    """
    return {
        "maintenance_factor": 0.05,  # 5% of equipment cost
        "default_weeks_per_year": 52,
        "default_hours_per_week": 40,
    }
