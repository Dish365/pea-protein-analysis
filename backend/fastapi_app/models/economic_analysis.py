"""
Shared economic analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional
from enum import Enum


class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'


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

    @field_validator("annual_cost")
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], values: Dict) -> float:
        if v is None and all(k in values for k in ["consumption", "unit_price"]):
            return values["consumption"] * values["unit_price"]
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
    def calculate_annual_cost(cls, v: Optional[float], values: Dict) -> float:
        if v is None and all(k in values for k in ["quantity", "unit_price"]):
            return values["quantity"] * values["unit_price"]
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
    def calculate_annual_cost(cls, v: Optional[float], values: Dict) -> float:
        if v is None and all(k in values for k in ["hourly_wage", "hours_per_week", "weeks_per_year", "num_workers"]):
            return (
                values["hourly_wage"] 
                * values["hours_per_week"] 
                * values["weeks_per_year"] 
                * values["num_workers"]
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
    economic_factors: EconomicFactors
    process_type: ProcessType


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