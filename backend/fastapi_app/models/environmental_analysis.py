"""
Shared environmental analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, List, Optional, Literal, TypedDict, Union, Any
from enum import Enum
import math

class AllocationMethod(str, Enum):
    """Valid allocation methods"""
    PHYSICAL = "physical"
    ECONOMIC = "economic"
    HYBRID = "hybrid"

class ProcessInputs(BaseModel):
    """Environmental process data model with RF treatment parameters."""
    # RF Pretreatment Parameters
    rf_electricity_kwh: float = Field(..., gt=0, description="RF unit power consumption in kWh")
    rf_temperature_outfeed_c: float = Field(..., gt=0, le=150, description="RF outfeed temperature in °C")
    rf_temperature_electrode_c: float = Field(..., gt=0, le=150, description="RF electrode temperature in °C")
    rf_frequency_mhz: float = Field(27.12, frozen=True, description="RF frequency in MHz (fixed at 27.12 MHz)")
    rf_anode_current_a: float = Field(..., gt=0, description="RF anode current in amperes")
    rf_grid_current_a: float = Field(..., gt=0, description="RF grid current in amperes")
    
    # Process Steps Energy
    air_classifier_milling_kwh: float = Field(..., gt=0, description="Air classifier mill energy consumption in kWh")
    air_classification_kwh: float = Field(..., gt=0, description="Air classification energy consumption in kWh")
    hammer_milling_kwh: float = Field(..., gt=0, description="Hammer mill energy consumption in kWh")
    dehulling_kwh: float = Field(..., gt=0, description="Dehulling energy consumption in kWh")
    
    # Water and Moisture Management
    tempering_water_kg: float = Field(..., gt=0, description="Water used for tempering in kg")
    initial_moisture_content: float = Field(..., ge=0.08, le=0.20, description="Initial moisture content ratio")
    final_moisture_content: float = Field(..., ge=0.08, le=0.20, description="Final moisture content ratio")
    target_moisture_content: float = Field(..., ge=0.08, le=0.20, description="Target moisture content for dehulling")
    
    # Production Parameters
    product_kg: float = Field(..., gt=0, description="Daily production capacity in kg")
    equipment_kg: float = Field(..., gt=0, description="Total equipment mass in kg")
    waste_kg: float = Field(..., ge=0, description="Daily waste generation in kg")
    transport_ton_km: float = Field(..., gt=0, description="Transportation in ton-km")
    
    # Process Configuration
    conveyor_speed_m_min: float = Field(0.17, gt=0, description="RF conveyor speed in m/min")
    material_depth_mm: float = Field(30.0, gt=0, description="RF material bed depth in mm")
    electrode_gap_mm: float = Field(86.9, gt=0, description="RF electrode gap in mm")
    thermal_ratio: float = Field(0.65, ge=0, le=1, description="Ratio of thermal processing")

    @field_validator('*')
    @classmethod
    def validate_positive_numbers(cls, v: float, field: str) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError(f"{field} cannot be NaN or infinite")
        return v

    @model_validator(mode='after')
    def validate_moisture_contents(self) -> 'ProcessInputs':
        """Validate moisture content relationships"""
        if self.final_moisture_content >= self.initial_moisture_content:
            raise ValueError("Final moisture content must be less than initial moisture content")
        if not (0.12 <= self.target_moisture_content <= 0.13):
            raise ValueError("Target moisture content must be between 12-13% for dehulling")
        return self

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
    metadata: Dict[str, Union[float, Dict[str, float]]]
    rf_parameters: Dict[str, float]
    process_breakdown: Dict[str, float]

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
    rf_validation: Dict[str, Any]

    @model_validator(mode='after')
    def validate_impact_results(self) -> 'ProcessAnalysisResponse':
        if not isinstance(self.impact_results, dict):
            raise ValueError("impact_results must be a dictionary")
        if "total_impacts" not in self.impact_results:
            raise ValueError("impact_results must contain total_impacts")
        if "process_contributions" not in self.impact_results:
            raise ValueError("impact_results must contain process_contributions")
        if "metadata" not in self.impact_results:
            raise ValueError("impact_results must contain metadata")
        if "rf_parameters" not in self.impact_results:
            raise ValueError("impact_results must contain rf_parameters")
        if "process_breakdown" not in self.impact_results:
            raise ValueError("impact_results must contain process_breakdown")
        return self 