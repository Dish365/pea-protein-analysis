from fastapi import APIRouter, HTTPException

from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from backend.fastapi_app.models.economic_analysis import CapexInput, EconomicFactors

router = APIRouter(tags=["Capital Expenditure"])


@router.post("/calculate")
async def calculate_capex(input_data: CapexInput):
    """Calculate total capital expenditure and its components"""
    try:
        # Initialize CAPEX analysis
        capex_analysis = CapitalExpenditureAnalysis()

        # Add equipment
        for equipment in input_data.equipment_list:
            capex_analysis.add_equipment(equipment.dict())

        # Calculate total CAPEX
        capex_result = capex_analysis.calculate_total_capex(
            installation_factor=input_data.economic_factors.installation_factor,
            indirect_costs_factor=input_data.economic_factors.indirect_costs_factor,
        )

        # Get detailed breakdowns
        equipment_breakdown = capex_analysis.get_equipment_breakdown()

        return {
            "capex_summary": capex_result,
            "equipment_breakdown": equipment_breakdown,
            "process_type": input_data.process_type,
            "production_volume": input_data.economic_factors.production_volume
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/factors")
async def get_default_factors() -> EconomicFactors:
    """Get default economic factors for CAPEX calculations"""
    return EconomicFactors(
        project_duration=10,
        discount_rate=0.1,
        production_volume=1000.0
    )


