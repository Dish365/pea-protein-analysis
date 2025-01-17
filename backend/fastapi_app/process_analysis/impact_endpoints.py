from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

from analytics.environmental.services.impact_calculator import ImpactCalculator
from analytics.environmental.impact.gwp import GWPCalculator
from analytics.environmental.impact.hct import HCTCalculator
from analytics.environmental.impact.frs import FRSCalculator
from analytics.environmental.impact.water import WaterConsumptionCalculator

router = APIRouter(prefix="/impact", tags=["environmental-impact"])

# Request Models
class ProcessDataRequest(BaseModel):
    electricity_kwh: float
    water_kg: float
    transport_ton_km: float
    product_kg: float
    equipment_kg: float
    cooling_kwh: float
    waste_kg: float

# Initialize calculators
impact_calculator = ImpactCalculator()

@router.post("/calculate")
async def calculate_impacts(request: ProcessDataRequest):
    """Calculate all environmental impacts for the process"""
    try:
        impacts = impact_calculator.calculate_process_impacts(
            electricity_kwh=request.electricity_kwh,
            water_kg=request.water_kg,
            transport_ton_km=request.transport_ton_km,
            product_kg=request.product_kg,
            equipment_kg=request.equipment_kg,
            cooling_kwh=request.cooling_kwh,
            waste_kg=request.waste_kg
        )
        
        return {
            "status": "success",
            "impacts": impacts,
            "process_contributions": impact_calculator.get_process_contributions()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/factors")
async def get_impact_factors():
    """Get environmental impact factors used in calculations"""
    return {
        "gwp_factors": GWPCalculator.GWP_FACTORS,
        "hct_factors": HCTCalculator.HCT_FACTORS,
        "frs_factors": FRSCalculator.FRS_FACTORS,
        "water_factors": WaterConsumptionCalculator.WATER_FACTORS
    } 