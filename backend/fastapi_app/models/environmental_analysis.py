"""
Shared environmental analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional, Literal
import math


class ProcessEnvironmentalData(BaseModel):
    """Environmental process data model."""
    electricity_consumption: float = Field(..., gt=0, description="Electricity consumption in kWh")
    cooling_consumption: float = Field(..., gt=0, description="Cooling energy consumption in kWh")
    water_consumption: float = Field(..., gt=0, description="Water consumption in kg")
    transport_consumption: float = Field(..., gt=0, description="Transport in ton-km")
    product_mass: float = Field(..., gt=0, description="Product mass in kg")
    equipment_mass: float = Field(..., gt=0, description="Equipment mass in kg")
    waste_mass: float = Field(..., gt=0, description="Waste mass in kg")
    thermal_ratio: float = Field(0.3, ge=0, le=1, description="Ratio of thermal processing")

    @field_validator('*')
    @classmethod
    def validate_positive_numbers(cls, v: float, field: str) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError(f"{field} cannot be NaN or infinite")
        return v


class ImpactFactors(BaseModel):
    """Environmental impact factors."""
    gwp_factors: Dict[str, float]
    hct_factors: Dict[str, float]
    frs_factors: Dict[str, float]
    water_factors: Dict[str, float]


class ImpactResults(BaseModel):
    """Environmental impact calculation results."""
    gwp: float = Field(..., description="Global Warming Potential")
    hct: float = Field(..., description="Human Carcinogenic Toxicity")
    frs: float = Field(..., description="Fossil Resource Scarcity")
    water_impact: float = Field(..., description="Water Impact")
    process_contributions: Dict[str, Dict[str, float]]


class AllocationMethod(str):
    ECONOMIC = "economic"
    PHYSICAL = "physical"
    HYBRID = "hybrid"


class AllocationWeights(BaseModel):
    """Weights for hybrid allocation."""
    economic: float = Field(..., ge=0, le=1)
    physical: float = Field(..., ge=0, le=1)

    @field_validator('*')
    @classmethod
    def validate_weights(cls, v: float) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Weight cannot be NaN or infinite")
        return v


class AllocationRequest(BaseModel):
    """Environmental impact allocation request."""
    impacts: Dict[str, float]
    product_values: Dict[str, float]
    mass_flows: Dict[str, float]
    method: Literal["economic", "physical", "hybrid"] = "hybrid"
    hybrid_weights: Optional[AllocationWeights] = None

    @field_validator('impacts', 'product_values', 'mass_flows')
    @classmethod
    def validate_positive_values(cls, v: Dict[str, float]) -> Dict[str, float]:
        for key, value in v.items():
            if math.isnan(value) or math.isinf(value):
                raise ValueError(f"Value for {key} cannot be NaN or infinite")
            if value < 0:
                raise ValueError(f"Value for {key} must be positive")
        return v


class AllocationResults(BaseModel):
    """Environmental impact allocation results."""
    allocation_factors: Dict[str, float]
    allocated_impacts: Dict[str, Dict[str, float]]
    method_used: str
    process_type: Optional[str] = None


class EnvironmentalMetrics(BaseModel):
    """Combined environmental metrics."""
    impact_results: ImpactResults
    allocation_results: Optional[AllocationResults] = None
    energy_intensity: float
    water_intensity: float
    waste_ratio: float
    thermal_efficiency: float 