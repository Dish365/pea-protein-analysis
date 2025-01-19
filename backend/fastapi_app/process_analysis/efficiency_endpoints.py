from fastapi import APIRouter, HTTPException
from typing import Dict
from pydantic import BaseModel

from analytics.environmental.services.efficiency_calculator import EfficiencyCalculator

router = APIRouter(tags=["environmental-efficiency"])

class EfficiencyRequest(BaseModel):
    economic_data: Dict[str, float]
    quality_data: Dict[str, float]
    environmental_impacts: Dict[str, float]
    resource_inputs: Dict[str, float]

# Initialize calculator
efficiency_calculator = EfficiencyCalculator()

@router.post("/calculate")
async def calculate_efficiency(request: EfficiencyRequest):
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

@router.get("/indicators")
async def get_efficiency_indicators():
    """Get available efficiency indicators and their descriptions"""
    return {
        "economic": [
            "production_cost",
            "value_added",
            "profitability"
        ],
        "quality": [
            "protein_recovery",
            "protein_purity",
            "functional_score"
        ],
        "environmental": [
            "resource_efficiency",
            "impact_efficiency",
            "quality_efficiency"
        ]
    } 