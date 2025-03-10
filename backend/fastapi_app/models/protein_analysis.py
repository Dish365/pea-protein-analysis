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
    moisture_compensation_factor: float = Field(0.05, ge=0, le=0.2)
    initial_moisture: float = Field(13.6, ge=0, le=100)
    final_moisture: float = Field(10.2, ge=0, le=100)


class ProcessStep(BaseModel):
    feed_composition: Union[Dict[str, float], str]
    product_composition: Union[Dict[str, float], str]
    mass_flow: Union[Dict[str, float], str]
    processing_moisture: Optional[float] = Field(None, ge=0, le=100, description="Processing moisture content percentage")


class SeparationEfficiencyInput(BaseModel):
    feed_composition: Dict[str, float]
    product_composition: Dict[str, float]
    mass_flow: Dict[str, float]
    process_data: Optional[List[Dict[str, Union[Dict[str, float], str, float]]]] = Field(
        None,
        description="List of process steps with references or direct data, plus processing_moisture"
    )
    target_purity: Optional[float] = None

    @field_validator("feed_composition")
    @classmethod
    def validate_feed_composition(cls, v: Dict[str, float]) -> Dict[str, float]:
        if not v:
            raise ValueError("Feed composition cannot be empty")
        if "protein" not in v:
            raise ValueError("Feed composition must include protein content")
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
        if "protein" not in v:
            raise ValueError("Product composition must include protein content")
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

    @field_validator("process_data")
    @classmethod
    def validate_process_data(cls, v: Optional[List[Dict]], values) -> Optional[List[Dict]]:
        if v is None:
            return v
            
        for step in v:
            required_keys = {"feed_composition", "product_composition", "mass_flow"}
            if not all(key in step for key in required_keys):
                raise ValueError(f"Each process step must contain: {required_keys}")
                
            # Validate references and allow processing_moisture
            for key in step:
                if key in required_keys:
                    value = step[key]
                    if isinstance(value, str) and value not in values.data:
                        raise ValueError(f"Invalid reference '{value}' in process data")
                elif key == "processing_moisture":
                    if not isinstance(step[key], (int, float)):
                        raise ValueError("Processing moisture must be numeric")
                else:
                    raise ValueError(f"Unexpected field '{key}' in process data")
        
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
        gt=0.0,
        lt=10.0,  # Most protein materials have density < 10 g/cm³
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
    final_moisture: Optional[float] = Field(
        None,
        description="Final moisture content percentage",
        ge=0.0,
        le=100.0
    )
    treatment_type: Optional[ProcessType] = Field(
        None,
        description="Pre-treatment type (rf/ir)"
    )

    @field_validator("density")
    @classmethod
    def validate_density(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            if v <= 0:
                raise ValueError("Density must be positive")
            if v >= 10.0:
                raise ValueError("Density value is unrealistic for protein materials")
        return v

    @field_validator("final_moisture")
    @classmethod
    def validate_final_moisture(cls, v: Optional[float], values) -> Optional[float]:
        if v is not None:
            initial = values.data.get("initial_moisture")
            if initial is not None and v >= initial:
                raise ValueError("Final moisture content should be less than initial moisture content")
        return v

    @field_validator("particle_sizes")
    @classmethod
    def validate_particle_sizes(cls, v: List[float]) -> List[float]:
        if len(v) < 2:
            raise ValueError("At least 2 particle sizes are required for analysis")
        if not all(x > 0 for x in v):
            raise ValueError("All particle sizes must be positive")
        if any(x > 10000 for x in v):  # 10mm upper limit
            raise ValueError("Particle sizes exceeding 10000 μm are unrealistic for protein processing")
        return sorted(v)  # Return sorted list for efficiency

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
            # Normalize weights if they don't sum to 1
            total = sum(v)
            if total > 0:
                v = [w/total for w in v]
            else:
                raise ValueError("Sum of weights must be positive")
        return v

    @field_validator("target_ranges")
    @classmethod
    def validate_target_ranges(cls, v: Optional[Dict[str, Tuple[float, float]]]) -> Optional[Dict[str, Tuple[float, float]]]:
        if v is None:
            return v
        valid_keys = {"D10", "D50", "D90", "span", "cv"}
        for key, (min_val, max_val) in v.items():
            if key not in valid_keys:
                raise ValueError(f"Invalid target range key: {key}. Must be one of {valid_keys}")
            if min_val >= max_val:
                raise ValueError(f"Invalid range for {key}: min value must be less than max value")
            if min_val < 0:
                raise ValueError(f"Invalid range for {key}: values cannot be negative")
            if key in {"D10", "D50", "D90"} and max_val > 10000:
                raise ValueError(f"Invalid range for {key}: particle sizes cannot exceed 10000 μm")
        return v


class ProteinAnalysisResponse(BaseModel):
    recovery_metrics: Dict[str, float]
    separation_metrics: Dict[str, Union[float, Dict[str, float]]]
    particle_metrics: Dict[str, float]
    process_performance: Optional[Dict[str, float]]
