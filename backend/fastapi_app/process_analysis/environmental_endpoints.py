from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel

from analytics.environmental.services.impact_calculator import ImpactCalculator
from analytics.environmental.services.allocation_engine import AllocationEngine
from analytics.environmental.services.efficiency_calculator import EfficiencyCalculator

router = APIRouter(tags=["environmental"])

# Request/Response Models
class ImpactCalculationRequest(BaseModel):
    electricity_kwh: float
    water_kg: float
    transport_ton_km: float
    product_kg: float
    equipment_kg: float
    cooling_kwh: float
    waste_kg: float

class AllocationRequest(BaseModel):
    impacts: Dict[str, float]
    product_values: Dict[str, float]
    mass_flows: Dict[str, float]
    method: str = "hybrid"
    hybrid_weights: Optional[Dict[str, float]] = None

class EfficiencyRequest(BaseModel):
    economic_data: Dict[str, float]
    quality_data: Dict[str, float]
    environmental_impacts: Dict[str, float]
    resource_inputs: Dict[str, float]

# Initialize services
impact_calculator = ImpactCalculator()
allocation_engine = AllocationEngine()
efficiency_calculator = EfficiencyCalculator()

@router.post("/calculate-impacts")
async def calculate_environmental_impacts(request: ImpactCalculationRequest):
    """Calculate environmental impacts for the process"""
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

@router.post("/allocate-impacts")
async def allocate_environmental_impacts(request: AllocationRequest):
    """Allocate environmental impacts between products"""
    try:
        allocation_engine.configure_allocation(
            product_values=request.product_values,
            mass_flows=request.mass_flows,
            hybrid_weights=request.hybrid_weights
        )
        
        allocated_impacts = allocation_engine.allocate_impacts(
            impacts=request.impacts,
            method=request.method
        )
        
        return {
            "status": "success",
            "allocated_impacts": allocated_impacts,
            "allocation_factors": allocation_engine.get_allocation_factors(request.method)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/calculate-efficiency")
async def calculate_eco_efficiency(request: EfficiencyRequest):
    """Calculate eco-efficiency metrics"""
    try:
        efficiency_metrics = efficiency_calculator.calculate_efficiency_metrics(
            economic_data=request.economic_data,
            quality_data=request.quality_data,
            environmental_impacts=request.environmental_impacts,
            resource_inputs=request.resource_inputs
        )
        
        return {
            "status": "success",
            "efficiency_metrics": efficiency_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
