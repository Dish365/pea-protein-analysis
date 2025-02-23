"""
Shared environmental analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, List, Optional, Literal, TypedDict, Union
from enum import Enum
import math

class AllocationMethod(str, Enum):
    """Valid allocation methods"""
    PHYSICAL = "physical"
    ECONOMIC = "economic"
    HYBRID = "hybrid"

class ProcessInputs(BaseModel):
    """Environmental process data model."""
    electricity_kwh: float = Field(..., gt=0, description="Electricity consumption in kWh")
    cooling_kwh: float = Field(..., gt=0, description="Cooling energy consumption in kWh")
    water_kg: float = Field(..., gt=0, description="Water consumption in kg")
    transport_ton_km: float = Field(..., gt=0, description="Transport in ton-km")
    product_kg: float = Field(..., gt=0, description="Product mass in kg")
    equipment_kg: float = Field(..., gt=0, description="Equipment mass in kg")
    waste_kg: float = Field(..., gt=0, description="Waste mass in kg")
    thermal_ratio: float = Field(0.3, ge=0, le=1, description="Ratio of thermal processing")

    @field_validator('*')
    @classmethod
    def validate_positive_numbers(cls, v: float, field: str) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError(f"{field} cannot be NaN or infinite")
        return v

class ImpactFactor(TypedDict):
    """Impact factor definition"""
    value: float
    unit: str
    description: str

class ProcessContribution(TypedDict):
    """Process contribution definition"""
    value: float
    unit: str
    process: str

class ImpactResults(TypedDict):
    """Environmental impact calculation results."""
    gwp: float
    hct: float
    frs: float
    water_consumption: float

class DetailedImpactResults(TypedDict):
    """Detailed impact results including process contributions"""
    total_impacts: ImpactResults
    process_contributions: Dict[str, Dict[str, ProcessContribution]]
    metadata: Dict[str, float]

class AllocationWeights(BaseModel):
    """Weights for hybrid allocation."""
    economic: float = Field(..., ge=0, le=1)
    physical: float = Field(..., ge=0, le=1)

    @model_validator(mode='after')
    def validate_weights_sum(self) -> 'AllocationWeights':
        if not math.isclose(self.economic + self.physical, 1.0, rel_tol=1e-9):
            raise ValueError("Weights must sum to 1.0")
        return self

class AllocationRequest(BaseModel):
    """Environmental impact allocation request."""
    impacts: Dict[str, float]
    product_values: Dict[str, float]
    mass_flows: Dict[str, float]
    method: AllocationMethod = AllocationMethod.HYBRID
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

    @model_validator(mode='after')
    def validate_hybrid_weights(self) -> 'AllocationRequest':
        if self.method == AllocationMethod.HYBRID and self.hybrid_weights is None:
            self.hybrid_weights = AllocationWeights(economic=0.5, physical=0.5)
        return self

class AllocationResults(TypedDict):
    """Environmental impact allocation results."""
    allocation_factors: Dict[str, float]
    allocated_impacts: Dict[str, Dict[str, float]]
    method_used: AllocationMethod

class ProcessAnalysisResponse(BaseModel):
    """Complete process analysis response."""
    status: str = "success"
    impact_results: DetailedImpactResults
    allocation_results: Optional[AllocationResults] = None
    suggested_allocation_method: Optional[AllocationMethod] = None 