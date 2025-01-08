from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional

class ProteinRecoveryInput(BaseModel):
    input_mass: float = Field(..., gt=0, description="Input mass in kg")
    output_mass: float = Field(..., gt=0, description="Output mass in kg")
    initial_protein_content: float = Field(..., gt=0, le=100, description="Initial protein content in %")
    output_protein_content: float = Field(..., gt=0, le=100, description="Output protein content in %")
    process_type: str = Field(..., description="Process type (Baseline/RF/IR)")

class SeparationEfficiencyInput(BaseModel):
    feed_composition: Dict[str, float] = Field(
        ..., 
        description="Component percentages in feed"
    )
    product_composition: Dict[str, float] = Field(
        ..., 
        description="Component percentages in product"
    )
    mass_flow: Dict[str, float] = Field(
        ..., 
        description="Input and output mass flows"
    )
    process_data: Optional[List[Dict]] = Field(
        None, 
        description="Step-wise process data"
    )
    target_purity: Optional[float] = Field(
        None, 
        description="Target protein purity percentage"
    )

    @validator('feed_composition')
    def validate_feed_composition(cls, v):
        if 'protein' not in v:
            raise ValueError("Feed composition must include protein content")
        if any(val < 0 or val > 100 for val in v.values()):
            raise ValueError("Component percentages must be between 0 and 100")
        return v

    @validator('mass_flow')
    def validate_mass_flow(cls, v):
        required_keys = {'input', 'output'}
        if not all(key in v for key in required_keys):
            raise ValueError("Mass flow must include both input and output")
        if any(val <= 0 for val in v.values()):
            raise ValueError("Mass flow values must be positive")
        return v

class ParticleSizeInput(BaseModel):
    particle_sizes: List[float] = Field(..., description="List of particle sizes in μm")
    weights: Optional[List[float]] = Field(None, description="Optional weights for each particle size")
    density: Optional[float] = Field(None, description="Particle density in g/cm³")
    target_ranges: Optional[Dict[str, tuple]] = Field(None, description="Target ranges for parameters")

class ProteinAnalysisResponse(BaseModel):
    recovery_metrics: Dict[str, float]
    separation_metrics: Dict[str, float]
    particle_metrics: Dict[str, float]
    process_performance: Optional[Dict[str, float]] 