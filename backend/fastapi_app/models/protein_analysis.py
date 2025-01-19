from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum


class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'


class ProteinRecoveryInput(BaseModel):
    input_mass: float = Field(..., gt=0, description="Input mass in kg")
    output_mass: float = Field(..., gt=0, description="Output mass in kg")
    initial_protein_content: float = Field(
        ..., gt=0, le=100, description="Initial protein content in %"
    )
    output_protein_content: float = Field(
        ..., gt=0, le=100, description="Output protein content in %"
    )
    process_type: ProcessType = Field(..., description="Process type (baseline/rf/ir)")


class SeparationEfficiencyInput(BaseModel):
    feed_composition: Dict[str, float]
    product_composition: Dict[str, float]
    mass_flow: Dict[str, float]
    process_data: Optional[List[Dict]] = None
    target_purity: Optional[float] = None

    @field_validator("feed_composition")
    @classmethod
    def validate_feed_composition(cls, v: Dict[str, float]) -> Dict[str, float]:
        if not v:
            raise ValueError("Feed composition cannot be empty")
        if not all(isinstance(val, (int, float)) and val >= 0 for val in v.values()):
            raise ValueError("All composition values must be non-negative numbers")
        if abs(sum(v.values()) - 100.0) > 0.1:
            raise ValueError("Composition percentages must sum to 100%")
        return v

    @field_validator("product_composition")
    @classmethod
    def validate_product_composition(cls, v: Dict[str, float]) -> Dict[str, float]:
        if not v:
            raise ValueError("Product composition cannot be empty")
        if not all(isinstance(val, (int, float)) and val >= 0 for val in v.values()):
            raise ValueError("All composition values must be non-negative numbers")
        if abs(sum(v.values()) - 100.0) > 0.1:
            raise ValueError("Composition percentages must sum to 100%")
        return v

    @field_validator("mass_flow")
    @classmethod
    def validate_mass_flow(cls, v: Dict[str, float]) -> Dict[str, float]:
        required_keys = {"input", "output"}
        if not all(key in v for key in required_keys):
            raise ValueError(f"Mass flow must contain all required keys: {required_keys}")
        if not all(isinstance(val, (int, float)) and val > 0 for val in v.values()):
            raise ValueError("All mass flow values must be positive numbers")
        if v["output"] > v["input"]:
            raise ValueError("Output mass cannot be greater than input mass")
        return v


class ParticleSizeInput(BaseModel):
    """Input model for particle size analysis with moisture content tracking."""
    
    particle_sizes: List[float] = Field(
        ...,
        description="List of particle sizes in μm"
    )
    weights: Optional[List[float]] = Field(
        None,
        description="Optional weights for each particle size"
    )
    density: Optional[float] = Field(
        None,
        description="Particle density in g/cm³ for surface area calculations"
    )
    target_ranges: Optional[Dict[str, tuple]] = Field(
        None,
        description="Target ranges for quality evaluation"
    )
    initial_moisture: float = Field(
        ...,
        description="Initial moisture content percentage",
        ge=0.0,
        le=100.0
    )
    treatment_type: Optional[ProcessType] = Field(
        None,
        description="Pre-treatment type (rf/ir)"
    )

    @field_validator("treatment_type")
    @classmethod
    def validate_treatment_type(cls, v: Optional[ProcessType]) -> Optional[ProcessType]:
        if v is not None and v == ProcessType.BASELINE:
            raise ValueError("Treatment type must be either 'rf' or 'ir'")
        return v

    @field_validator("particle_sizes")
    @classmethod
    def validate_particle_sizes(cls, v: List[float]) -> List[float]:
        if len(v) < 2:
            raise ValueError("At least 2 particle sizes are required for analysis")
        if not all(x > 0 for x in v):
            raise ValueError("All particle sizes must be positive")
        return v

    @field_validator("weights")
    @classmethod
    def validate_weights(cls, v: Optional[List[float]], values) -> Optional[List[float]]:
        if v is None:
            return v
        if len(v) != len(values.data.get("particle_sizes", [])):
            raise ValueError("Number of weights must match number of particle sizes")
        if not all(w >= 0 for w in v):
            raise ValueError("All weights must be non-negative")
        if abs(sum(v) - 1.0) > 0.001:  # Allow small floating point variance
            raise ValueError("Weights must sum to 1.0")
        return v

    @field_validator("target_ranges")
    @classmethod
    def validate_target_ranges(cls, v: Optional[Dict[str, Tuple[float, float]]]) -> Optional[Dict[str, Tuple[float, float]]]:
        if v is None:
            return v
        for key, (min_val, max_val) in v.items():
            if min_val >= max_val:
                raise ValueError(f"Invalid range for {key}: min value must be less than max value")
            if min_val < 0:
                raise ValueError(f"Invalid range for {key}: values cannot be negative")
        return v


class ProteinAnalysisResponse(BaseModel):
    recovery_metrics: Dict[str, float]
    separation_metrics: Dict[str, Union[float, Dict[str, float]]]
    particle_metrics: Dict[str, float]
    process_performance: Optional[Dict[str, float]]
