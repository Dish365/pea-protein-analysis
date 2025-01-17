# Implement OPEX-related API endpoints

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis

router = APIRouter()


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


@router.post("/opex/calculate")
async def calculate_opex(input_data: OpexAnalysisInput):
    """
    Calculate total operational expenditure and its components
    """
    try:
        # Initialize OPEX analysis
        opex_analysis = OperationalExpenditureAnalysis()

        # Add utilities
        for utility in input_data.utilities:
            opex_analysis.add_utility(utility.dict())

        # Add raw materials
        for material in input_data.raw_materials:
            opex_analysis.add_raw_material(material.dict())

        # Set equipment costs for maintenance calculation
        opex_analysis.set_equipment_costs(input_data.equipment_costs)

        # Set labor configuration
        opex_analysis.set_labor_config(input_data.labor_config.dict())

        # Calculate total OPEX
        opex_result = opex_analysis.calculate_total_opex(
            maintenance_factor=input_data.maintenance_factor
        )

        # Get detailed breakdowns
        utilities_breakdown = opex_analysis.get_utilities_breakdown()
        materials_breakdown = opex_analysis.get_materials_breakdown()
        labor_breakdown = opex_analysis.get_labor_breakdown()

        return {
            "opex_summary": opex_result,
            "utilities_breakdown": utilities_breakdown,
            "materials_breakdown": materials_breakdown,
            "labor_breakdown": labor_breakdown,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/opex/factors")
async def get_default_factors():
    """
    Get default factors for OPEX calculations
    """
    return {
        "maintenance_factor": 0.05,  # 5% of equipment cost
        "default_weeks_per_year": 52,
        "default_hours_per_week": 40,
    }
