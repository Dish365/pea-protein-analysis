from fastapi import APIRouter, HTTPException
from typing import Dict, List
from pydantic import BaseModel

from analytics.environmental.eco_efficiency.indicators import EconomicIndicators
from analytics.environmental.eco_efficiency.quality import QualityIndicators
from analytics.environmental.eco_efficiency.relative import RelativeEfficiencyCalculator

router = APIRouter(prefix="/efficiency", tags=["efficiency"])

# Request Models
class EconomicIndicatorRequest(BaseModel):
    capex: float
    opex: float
    production_volume: float
    product_prices: Dict[str, float]
    production_volumes: Dict[str, float]
    raw_material_cost: float
    revenue: float
    total_cost: float

class QualityIndicatorRequest(BaseModel):
    recovered_protein: float
    initial_protein: float
    protein_content: float
    total_mass: float
    properties: Dict[str, float]
    target_values: Dict[str, float]

class RelativeEfficiencyRequest(BaseModel):
    economic_value: float
    environmental_impact: Dict[str, float]
    product_output: float
    resource_input: Dict[str, float]
    quality_score: float
    production_cost: float

# Initialize calculators
economic_calculator = EconomicIndicators()
quality_calculator = QualityIndicators()
relative_calculator = RelativeEfficiencyCalculator()

@router.post("/economic-indicators")
async def calculate_economic_indicators(request: EconomicIndicatorRequest):
    """Calculate economic performance indicators"""
    try:
        production_cost = economic_calculator.calculate_production_cost(
            request.capex,
            request.opex,
            request.production_volume
        )
        
        value_added = economic_calculator.calculate_value_added(
            request.product_prices,
            request.production_volumes,
            request.raw_material_cost
        )
        
        profitability = economic_calculator.calculate_profitability(
            request.revenue,
            request.total_cost
        )
        
        return {
            "status": "success",
            "indicators": economic_calculator.get_indicators()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/quality-indicators")
async def calculate_quality_indicators(request: QualityIndicatorRequest):
    """Calculate product quality indicators"""
    try:
        recovery = quality_calculator.calculate_protein_recovery(
            request.recovered_protein,
            request.initial_protein
        )
        
        purity = quality_calculator.calculate_protein_purity(
            request.protein_content,
            request.total_mass
        )
        
        functional_score = quality_calculator.calculate_functional_properties(
            request.properties,
            request.target_values
        )
        
        return {
            "status": "success",
            "indicators": quality_calculator.get_indicators()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/relative-efficiency")
async def calculate_relative_efficiency(request: RelativeEfficiencyRequest):
    """Calculate relative efficiency metrics"""
    try:
        env_efficiency = relative_calculator.calculate_environmental_efficiency(
            request.economic_value,
            request.environmental_impact
        )
        
        resource_efficiency = relative_calculator.calculate_resource_efficiency(
            request.product_output,
            request.resource_input
        )
        
        quality_efficiency = relative_calculator.calculate_quality_efficiency(
            request.quality_score,
            request.production_cost
        )
        
        return {
            "status": "success",
            "metrics": relative_calculator.get_efficiency_metrics()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 