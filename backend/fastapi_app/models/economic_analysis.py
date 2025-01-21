"""
Shared economic analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Dict, List, Optional
from enum import Enum


class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'


class IndirectFactor(BaseModel):
    """Model for indirect cost factors in CAPEX calculations."""
    name: str = Field(..., description="Name of the indirect cost factor")
    cost: float = Field(..., gt=0, description="Base cost to apply percentage to")
    percentage: float = Field(..., gt=0, lt=1, description="Percentage as decimal (0-1)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class Equipment(BaseModel):
    """Base equipment model used across CAPEX calculations."""
    name: str
    cost: float = Field(..., gt=0, description="Equipment cost in USD")
    efficiency: float = Field(..., gt=0, le=1, description="Equipment efficiency factor")
    maintenance_cost: float = Field(..., gt=0, description="Annual maintenance cost in USD")
    energy_consumption: float = Field(..., gt=0, description="Energy consumption in kWh")
    processing_capacity: float = Field(..., gt=0, description="Processing capacity in kg/h")


class Utility(BaseModel):
    """Utility consumption and cost model."""
    name: str
    consumption: float = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    unit: str
    annual_cost: Optional[float] = None

    @field_validator('annual_cost')
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        """Calculate annual cost if not provided"""
        if v is None:
            data = info.data
            if 'consumption' in data and 'unit_price' in data:
                return data['consumption'] * data['unit_price']
        return v or 0.0


class RawMaterial(BaseModel):
    """Raw material model with cost calculation."""
    name: str
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    unit: str
    annual_cost: Optional[float] = None

    @field_validator("annual_cost")
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        """Calculate annual cost if not provided"""
        if v is None:
            data = info.data
            if 'quantity' in data and 'unit_price' in data:
                return data['quantity'] * data['unit_price']
        return v or 0.0


class LaborConfig(BaseModel):
    """Labor configuration with cost calculation."""
    hourly_wage: float = Field(..., gt=0)
    hours_per_week: float = Field(..., gt=0)
    weeks_per_year: float = Field(..., gt=0)
    num_workers: int = Field(..., gt=0)
    annual_cost: Optional[float] = None

    @field_validator("annual_cost")
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        """Calculate annual cost if not provided"""
        if v is None:
            data = info.data
            if all(k in data for k in ["hourly_wage", "hours_per_week", "weeks_per_year", "num_workers"]):
                return (
                    data["hourly_wage"] 
                    * data["hours_per_week"] 
                    * data["weeks_per_year"] 
                    * data["num_workers"]
                )
        return v or 0.0


class EconomicFactors(BaseModel):
    """Shared economic factors across calculations."""
    installation_factor: float = Field(0.2, ge=0, le=1)
    indirect_costs_factor: float = Field(0.15, ge=0, le=1)
    maintenance_factor: float = Field(0.05, ge=0, le=1)
    project_duration: int = Field(..., gt=0)
    discount_rate: float = Field(..., gt=0, lt=1)
    production_volume: float = Field(..., gt=0)


class CapexInput(BaseModel):
    """Capital expenditure input model."""
    equipment_list: List[Equipment]
    indirect_factors: List[IndirectFactor] = Field(
        default_factory=list,
        description="List of indirect cost factors. If empty, defaults will be used."
    )
    economic_factors: EconomicFactors
    process_type: ProcessType

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "equipment_list": [{
                    "name": "main_equipment",
                    "cost": 50000.0,
                    "efficiency": 0.85,
                    "maintenance_cost": 5000.0,
                    "energy_consumption": 1000.0,
                    "processing_capacity": 100.0
                }],
                "indirect_factors": [],
                "economic_factors": {
                    "installation_factor": 0.2,
                    "indirect_costs_factor": 0.15,
                    "maintenance_factor": 0.05,
                    "project_duration": 10,
                    "discount_rate": 0.1,
                    "production_volume": 1000.0
                },
                "process_type": "baseline"
            }]
        }
    }


class OpexInput(BaseModel):
    """Operational expenditure input model."""
    utilities: List[Utility]
    raw_materials: List[RawMaterial]
    labor_config: LaborConfig
    equipment_costs: float = Field(..., gt=0)
    economic_factors: EconomicFactors
    process_type: ProcessType


class ProfitabilityInput(BaseModel):
    """Profitability analysis input model."""
    capex: Dict[str, float]
    opex: Dict[str, float]
    economic_factors: EconomicFactors
    process_type: ProcessType
    cash_flows: List[float]
    monte_carlo_iterations: Optional[int] = Field(1000, ge=0)
    uncertainty: Optional[float] = Field(0.1, gt=0, lt=1) 