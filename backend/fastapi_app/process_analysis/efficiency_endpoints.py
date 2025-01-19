from fastapi import APIRouter, HTTPException, Response
from typing import Dict, Optional, List, Any
from pydantic import BaseModel, Field, field_validator
import logging
import math
import json

from analytics.environmental.services.efficiency_calculator import EfficiencyCalculator
from .services.rust_handler import RustHandler

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["eco-efficiency"])

class EconomicMetrics(BaseModel):
    capex: Dict[str, float] = Field(..., description="Capital expenditure breakdown including equipment_cost, installation_cost, indirect_cost, total_capex")
    opex: Dict[str, float] = Field(..., description="Operational expenditure breakdown including utilities_cost, materials_cost, labor_cost, maintenance_cost, total_opex")
    npv: float = Field(..., description="Net Present Value in USD")
    roi: float = Field(..., description="Return on Investment in %")
    payback_period: float = Field(..., description="Payback period in years")
    profitability_index: float = Field(..., description="Profitability index")
    sensitivity_analysis: Optional[Dict[str, Any]] = Field(None, description="Sensitivity analysis results")

class QualityMetrics(BaseModel):
    protein_recovery: float = Field(..., description="Protein recovery rate in %")
    separation_efficiency: float = Field(..., description="Overall separation efficiency in %")
    process_efficiency: float = Field(..., description="Process efficiency metric in %")
    particle_size_distribution: Dict[str, float] = Field(..., description="Particle size distribution metrics (D10, D50, D90)")

class EnvironmentalImpacts(BaseModel):
    gwp: float = Field(..., description="Global Warming Potential in CO2eq")
    hct: float = Field(..., description="Human Carcinogenic Toxicity in CTUh")
    frs: float = Field(..., description="Fossil Resource Scarcity in kg oil eq")
    water_consumption: float = Field(..., description="Water consumption impact in m3")
    allocated_impacts: Dict[str, Any] = Field(..., description="Allocated environmental impacts with method, factors, and results")

class ResourceInputs(BaseModel):
    energy_consumption: float = Field(..., description="Total energy consumption in kWh")
    water_usage: float = Field(..., description="Total water usage in m3")
    raw_material_input: float = Field(..., description="Raw material input in kg")

class EcoEfficiencyRequest(BaseModel):
    economic_data: EconomicMetrics
    quality_metrics: QualityMetrics
    environmental_impacts: EnvironmentalImpacts
    resource_inputs: ResourceInputs
    process_type: str = Field(..., description="Process type (baseline/RF/IR)")

    @field_validator('process_type')
    @classmethod
    def validate_process_type(cls, v: str) -> str:
        valid_types = ['baseline', 'RF', 'IR']
        if v.lower() not in [t.lower() for t in valid_types]:
            raise ValueError(f"Process type must be one of {valid_types}")
        return v.lower()

    @field_validator('*')
    @classmethod
    def validate_non_negative(cls, v: Any, field: Field) -> Any:
        if isinstance(v, (int, float)) and field.name not in ['roi', 'profitability_index']:
            if v < 0:
                raise ValueError(f"{field.name} cannot be negative")
        return v

# Initialize services
efficiency_calculator = EfficiencyCalculator()
rust_handler = RustHandler()
logger.info("Initialized Eco-efficiency services")

@router.post("/calculate")
async def calculate_eco_efficiency(request: EcoEfficiencyRequest):
    """Calculate comprehensive eco-efficiency metrics using both Python and Rust implementations"""
    try:
        logger.debug(f"Received eco-efficiency calculation request for process: {request.process_type}")
        
        # Calculate base efficiency metrics using Python implementation
        base_metrics = efficiency_calculator.calculate_efficiency_metrics(
            economic_data=request.economic_data.dict(),
            quality_data=request.quality_metrics.dict(),
            environmental_impacts=request.environmental_impacts.dict(),
            resource_inputs=request.resource_inputs.dict()
        )
        
        # Use Rust for performance-critical calculations
        try:
            # Calculate eco-efficiency matrix using Rust
            economic_values = [
                request.economic_data.npv,
                request.economic_data.roi
            ]
            environmental_impacts = [
                request.environmental_impacts.gwp,
                request.environmental_impacts.hct,
                request.environmental_impacts.frs,
                request.environmental_impacts.water_consumption
            ]
            
            efficiency_matrix = rust_handler.calculate_eco_efficiency_matrix(
                economic_values=economic_values,
                environmental_impacts=environmental_impacts
            )
            
            logger.debug(f"Rust efficiency matrix calculation successful: {efficiency_matrix}")
            
        except Exception as e:
            logger.error(f"Rust calculation failed, falling back to Python: {str(e)}")
            efficiency_matrix = None
        
        # Combine results
        response_data = {
            "status": "success",
            "process_type": request.process_type,
            "efficiency_metrics": {
                "economic_indicators": base_metrics["economic_indicators"],
                "quality_indicators": base_metrics["quality_indicators"],
                "efficiency_metrics": base_metrics["efficiency_metrics"]
            },
            "performance_indicators": {
                "eco_efficiency_index": calculate_eco_efficiency_index(
                    base_metrics, request.process_type
                ),
                "relative_performance": calculate_relative_performance(
                    base_metrics, request.process_type
                )
            }
        }
        
        # Add Rust calculations if available
        if efficiency_matrix:
            response_data["rust_calculations"] = {
                "efficiency_matrix": efficiency_matrix,
                "matrix_indicators": interpret_efficiency_matrix(efficiency_matrix)
            }
        
        logger.info("Eco-efficiency calculation completed successfully")
        return response_data
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        error_msg = f"Error in eco-efficiency calculation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/indicators")
async def get_efficiency_indicators():
    """Get available eco-efficiency indicators and their descriptions"""
    return {
        "economic_based": {
            "npv_efficiency": "NPV per environmental impact",
            "profit_efficiency": "Net profit per environmental impact",
            "cost_efficiency": "Production cost per environmental impact"
        },
        "quality_based": {
            "purity_efficiency": "Product purity per environmental impact",
            "yield_efficiency": "Product yield per environmental impact",
            "protein_efficiency": "Protein recovery per environmental impact"
        },
        "resource_based": {
            "energy_efficiency": "Product output per energy input",
            "water_efficiency": "Product output per water consumption",
            "material_efficiency": "Product output per raw material input"
        },
        "process_specific": {
            "baseline_reference": "Reference process eco-efficiency",
            "rf_improvement": "RF process relative improvement",
            "ir_improvement": "IR process relative improvement"
        }
    }

@router.get("/reference-values/{process_type}")
async def get_reference_values(process_type: str):
    """Get reference values for eco-efficiency calculations by process type"""
    try:
        if process_type not in ['baseline', 'RF', 'IR']:
            raise HTTPException(
                status_code=422,
                detail="Invalid process type. Must be one of: baseline, RF, IR"
            )
            
        return {
            "economic_reference": get_economic_reference(process_type),
            "environmental_reference": get_environmental_reference(process_type),
            "quality_reference": get_quality_reference(process_type)
        }
        
    except Exception as e:
        error_msg = f"Error retrieving reference values: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

# Helper functions
def calculate_eco_efficiency_index(metrics: Dict, process_type: str) -> float:
    """Calculate overall eco-efficiency index"""
    weights = {
        'economic': 0.4,
        'environmental': 0.4,
        'quality': 0.2
    }
    
    economic_score = sum(metrics["economic_indicators"].values()) / len(metrics["economic_indicators"])
    quality_score = sum(metrics["quality_indicators"].values()) / len(metrics["quality_indicators"])
    efficiency_score = sum(metrics["efficiency_metrics"].values()) / len(metrics["efficiency_metrics"])
    
    return (
        weights['economic'] * economic_score +
        weights['environmental'] * efficiency_score +
        weights['quality'] * quality_score
    )

def calculate_relative_performance(metrics: Dict, process_type: str) -> Dict[str, float]:
    """Calculate relative performance compared to baseline"""
    if process_type == 'baseline':
        return {"relative_improvement": 1.0}
    
    baseline_reference = get_reference_values('baseline')
    current_index = calculate_eco_efficiency_index(metrics, process_type)
    baseline_index = calculate_eco_efficiency_index(baseline_reference, 'baseline')
    
    return {
        "relative_improvement": current_index / baseline_index if baseline_index > 0 else 0
    }

def interpret_efficiency_matrix(matrix: List[float]) -> Dict[str, float]:
    """Interpret the Rust-calculated efficiency matrix"""
    return {
        "npv_efficiency": matrix[0],
        "profit_efficiency": matrix[1],
        "average_efficiency": sum(matrix) / len(matrix)
    }

# Reference value functions
def get_economic_reference(process_type: str) -> Dict[str, float]:
    """Get economic reference values for process type"""
    references = {
        'baseline': {'npv': 1000000, 'roi': 20},
        'RF': {'npv': 1200000, 'roi': 24},
        'IR': {'npv': 1100000, 'roi': 22}
    }
    return references[process_type]

def get_environmental_reference(process_type: str) -> Dict[str, float]:
    """Get environmental reference values for process type"""
    references = {
        'baseline': {'gwp': 100, 'water': 1000},
        'RF': {'gwp': 90, 'water': 900},
        'IR': {'gwp': 95, 'water': 950}
    }
    return references[process_type]

def get_quality_reference(process_type: str) -> Dict[str, float]:
    """Get quality reference values for process type"""
    references = {
        'baseline': {'protein_recovery': 0.75, 'separation_efficiency': 0.85},
        'RF': {'protein_recovery': 0.80, 'separation_efficiency': 0.90},
        'IR': {'protein_recovery': 0.78, 'separation_efficiency': 0.88}
    }
    return references[process_type] 