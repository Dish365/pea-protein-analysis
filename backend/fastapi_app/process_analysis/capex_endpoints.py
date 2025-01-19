from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis

router = APIRouter(tags=["Capital Expenditure"])


class Equipment(BaseModel):
    name: str
    cost: float
    efficiency: float
    maintenance_cost: float
    energy_consumption: float
    processing_capacity: float


class IndirectFactor(BaseModel):
    name: str
    cost: float
    percentage: float


class CapexAnalysisInput(BaseModel):
    equipment_list: List[Equipment]
    indirect_factors: List[IndirectFactor]
    installation_factor: Optional[float] = 0.2
    indirect_costs_factor: Optional[float] = 0.15


@router.post("/calculate")
async def calculate_capex(input_data: CapexAnalysisInput):
    """
    Calculate total capital expenditure and its components
    """
    try:
        # Initialize CAPEX analysis
        capex_analysis = CapitalExpenditureAnalysis()

        # Add equipment
        for equipment in input_data.equipment_list:
            capex_analysis.add_equipment(equipment.dict())

        # Add indirect factors
        for factor in input_data.indirect_factors:
            capex_analysis.add_indirect_factor(factor.dict())

        # Calculate total CAPEX
        capex_result = capex_analysis.calculate_total_capex(
            installation_factor=input_data.installation_factor,
            indirect_costs_factor=input_data.indirect_costs_factor,
        )

        # Get detailed breakdowns
        equipment_breakdown = capex_analysis.get_equipment_breakdown()
        indirect_factors_breakdown = capex_analysis.get_indirect_factors_breakdown()

        return {
            "capex_summary": capex_result,
            "equipment_breakdown": equipment_breakdown,
            "indirect_factors_breakdown": indirect_factors_breakdown,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/factors")
async def get_default_factors():
    """
    Get default installation and indirect cost factors
    """
    return {
        "installation_factor": 0.2,  # 20% of equipment cost
        "indirect_costs_factor": 0.15,  # 15% of direct costs
    }


# ...existing code...

