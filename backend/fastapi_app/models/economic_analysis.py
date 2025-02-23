"""
Shared economic analysis models to ensure consistency across endpoints.
"""

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum


class ProcessType(str, Enum):
    BASELINE = 'baseline'
    RF = 'rf'
    IR = 'ir'


class EconomicFactors(BaseModel):
    """Core economic factors used across all calculations"""
    installation_factor: float = Field(0.2, ge=0, le=1)
    indirect_costs_factor: float = Field(0.15, ge=0, le=1)
    maintenance_factor: float = Field(0.05, ge=0, le=1)
    project_duration: int = Field(..., gt=0)
    discount_rate: float = Field(..., gt=0, lt=1)
    production_volume: float = Field(..., gt=0)


class Equipment(BaseModel):
    """Unified equipment model for both CAPEX and OPEX calculations"""
    name: str
    base_cost: float = Field(..., gt=0, description="Total equipment cost in USD")
    efficiency_factor: float = Field(..., gt=0, le=1, description="Equipment efficiency factor (0-1)")
    installation_complexity: float = Field(1.0, ge=0.5, le=2.0, description="Installation complexity multiplier")
    maintenance_cost: float = Field(..., gt=0, description="Annual maintenance cost in USD")
    energy_consumption: float = Field(..., gt=0, description="Energy consumption in kWh")
    processing_capacity: float = Field(..., gt=0, description="Processing capacity in kg/h")
    capacity_units: str = Field("kg/h", description="Processing capacity units")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Equipment name cannot be empty")
        return v.strip()

    @field_validator('base_cost')
    def validate_base_cost(cls, v):
        return v  # No automatic scaling


class IndirectFactor(BaseModel):
    """Model for indirect cost factors in CAPEX calculations"""
    name: str = Field(..., description="Name of the indirect cost factor")
    cost: float = Field(..., gt=0, description="Base cost to apply percentage to")
    percentage: float = Field(..., gt=0, lt=1, description="Percentage as decimal (0-1)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class CapexInput(BaseModel):
    """Unified capital expenditure input model"""
    equipment_list: List[Equipment]
    indirect_factors: List[IndirectFactor] = Field(
        default_factory=list,
        description="List of indirect cost factors including engineering, construction, and contingency. If empty, defaults will be used."
    )
    economic_factors: EconomicFactors
    process_type: ProcessType

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "equipment_list": [{
                    "name": "main_equipment",
                    "base_cost": 50000.0,
                    "efficiency_factor": 0.85,
                    "installation_complexity": 1.2,
                    "maintenance_cost": 5000.0,
                    "energy_consumption": 1000.0,
                    "processing_capacity": 100.0
                }],
                "indirect_factors": [
                    {
                        "name": "engineering",
                        "cost": 50000.0,
                        "percentage": 0.15
                    },
                    {
                        "name": "contingency",
                        "cost": 50000.0,
                        "percentage": 0.10
                    }
                ],
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


class Utility(BaseModel):
    """Utility consumption and cost model"""
    name: str
    consumption: float = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    unit: str
    operating_hours: float = Field(..., gt=0, description="Annual operating hours")
    annual_cost: Optional[float] = None

    @field_validator('annual_cost')
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        if v is None:
            data = info.data
            return (
                data['consumption'] * 
                data['unit_price'] * 
                data['operating_hours']
            ) if all(k in data for k in ['consumption', 'unit_price', 'operating_hours']) else 0.0
        return v


class RawMaterial(BaseModel):
    """Raw material model with cost calculation"""
    name: str
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    unit: str
    protein_content: Optional[float] = Field(None, ge=0, le=1, description="Protein content as decimal (0-1)")
    annual_cost: Optional[float] = None

    @field_validator('annual_cost')
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        if v is None:
            data = info.data
            return data['quantity'] * data['unit_price'] if all(k in data for k in ['quantity', 'unit_price']) else 0.0
        return v


class LaborConfig(BaseModel):
    """Labor configuration with cost calculation"""
    hourly_wage: float = Field(..., gt=0)
    hours_per_week: float = Field(..., gt=0)
    weeks_per_year: float = Field(..., gt=0)
    num_workers: int = Field(..., gt=0)
    benefits_factor: float = Field(..., gt=0, lt=1, description="Benefits as a percentage of base salary (0-1)")
    annual_cost: Optional[float] = None

    @field_validator('annual_cost')
    @classmethod
    def calculate_annual_cost(cls, v: Optional[float], info: ValidationInfo) -> float:
        if v is None:
            data = info.data
            if all(k in data for k in ['hourly_wage', 'hours_per_week', 'weeks_per_year', 'num_workers', 'benefits_factor']):
                base_salary = (data['hourly_wage'] * data['hours_per_week'] * 
                             data['weeks_per_year'] * data['num_workers'])
                return base_salary * (1 + data['benefits_factor'])  # Add benefits
        return v or 0.0


class OpexInput(BaseModel):
    """Unified operational expenditure input model"""
    utilities: List[Utility]
    raw_materials: List[RawMaterial]
    labor_config: LaborConfig
    equipment_costs: float = Field(..., gt=0)
    economic_factors: EconomicFactors
    process_type: ProcessType


class BusinessMetricsResponse(BaseModel):
    """Response model for business metrics analysis"""
    timestamp: str
    metrics: Dict[str, Any]


class UncertaintyConfig(BaseModel):
    """Configuration for uncertainty in Monte Carlo analysis"""
    price: float = Field(0.15, gt=0, lt=1, description="Price uncertainty factor (0-1)")
    cost: float = Field(0.12, gt=0, lt=1, description="Cost uncertainty factor (0-1)")
    production: float = Field(0.10, gt=0, lt=1, description="Production uncertainty factor (0-1)")


class RevenueData(BaseModel):
    """Revenue data model for profitability analysis"""
    product_price: float = Field(..., gt=0, description="Product price per unit")
    annual_production: float = Field(..., gt=0, description="Annual production volume")
    yield_efficiency: float = Field(
        0.95, gt=0, le=1,
        description="Process yield efficiency (0-1)"
    )

    @field_validator('product_price', 'annual_production', 'yield_efficiency')
    @classmethod
    def validate_numeric(cls, v: float) -> float:
        """Ensure numeric values are properly converted"""
        try:
            return float(v)
        except (TypeError, ValueError):
            raise ValueError(f"Value {v} must be a valid number")


class ComprehensiveAnalysisInput(BaseModel):
    """Unified input model for comprehensive economic analysis"""
    equipment_list: List[Equipment]
    utilities: List[Utility]
    raw_materials: List[RawMaterial]
    labor_config: LaborConfig
    revenue_data: RevenueData
    economic_factors: EconomicFactors
    process_type: ProcessType
    indirect_factors: List[IndirectFactor] = Field(
        default_factory=list,
        description="List of indirect cost factors. If empty, defaults will be used."
    )
    monte_carlo_iterations: Optional[int] = Field(1000, ge=0)
    uncertainty: Optional[UncertaintyConfig] = Field(
        default_factory=lambda: UncertaintyConfig(price=0.15, cost=0.12, production=0.10),
        description="Uncertainty factors for Monte Carlo analysis"
    )
    random_seed: Optional[int] = Field(42, description="Random seed for Monte Carlo simulation reproducibility")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "equipment_list": [{
                    "name": "extraction_unit",
                    "base_cost": 100000.0,
                    "efficiency_factor": 0.85,
                    "installation_complexity": 1.2,
                    "maintenance_cost": 10000.0,
                    "energy_consumption": 2000.0,
                    "processing_capacity": 200.0
                }],
                "utilities": [{
                    "name": "electricity",
                    "consumption": 50000.0,
                    "unit_price": 0.12,
                    "unit": "kWh",
                    "operating_hours": 8000
                }],
                "raw_materials": [{
                    "name": "pea_biomass",
                    "quantity": 1000.0,
                    "unit_price": 2.5,
                    "unit": "kg"
                }],
                "labor_config": {
                    "hourly_wage": 25.0,
                    "hours_per_week": 40,
                    "weeks_per_year": 50,
                    "num_workers": 5,
                    "benefits_factor": 0.35  # 35% benefits on top of base salary
                },
                "revenue_data": {
                    "product_price": 10.0,
                    "annual_production": 500000.0,
                    "yield_efficiency": 0.95
                },
                "economic_factors": {
                    "installation_factor": 0.3,
                    "indirect_costs_factor": 0.45,
                    "maintenance_factor": 0.02,
                    "project_duration": 10,
                    "discount_rate": 0.1,
                    "production_volume": 1000.0
                },
                "indirect_factors": [
                    {
                        "name": "engineering",
                        "cost": 100000.0,
                        "percentage": 0.15
                    },
                    {
                        "name": "construction",
                        "cost": 100000.0,
                        "percentage": 0.20
                    }
                ],
                "process_type": "baseline",
                "monte_carlo_iterations": 1000,
                "uncertainty": {
                    "price": 0.15,
                    "cost": 0.12,
                    "production": 0.10
                },
                "random_seed": 42
            }]
        }
    }


class SensitivityAnalysisInput(BaseModel):
    """Input model for sensitivity analysis"""
    base_cash_flows: List[float] = Field(..., description="Base case cash flows including initial investment")
    variables: List[str] = Field(
        default=["discount_rate", "production_volume", "operating_costs", "revenue"],
        description="Variables to analyze sensitivity for"
    )
    ranges: Dict[str, List[float]] = Field(
        default={
            "discount_rate": [0.05, 0.15],
            "production_volume": [500.0, 1500.0],
            "operating_costs": [0.8, 1.2],
            "revenue": [0.8, 1.2]
        },
        description="Range [min, max] for each variable"
    )
    steps: Optional[int] = Field(
        default=10,
        ge=5,
        le=100,
        description="Number of steps for sensitivity analysis"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "base_cash_flows": [-500000.0, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0],
                "variables": ["discount_rate", "production_volume"],
                "ranges": {
                    "discount_rate": [0.05, 0.15],
                    "production_volume": [500.0, 1500.0]
                },
                "steps": 10
            }]
        }
    }

    @field_validator('variables')
    @classmethod
    def validate_variables(cls, v: List[str]) -> List[str]:
        """Validate that variables are from the allowed set"""
        allowed_vars = {"discount_rate", "production_volume", "operating_costs", "revenue"}
        invalid_vars = set(v) - allowed_vars
        if invalid_vars:
            raise ValueError(f"Invalid variables: {invalid_vars}. Must be from: {allowed_vars}")
        return v

    @field_validator('ranges')
    @classmethod
    def validate_ranges(cls, v: Dict[str, List[float]], info: ValidationInfo) -> Dict[str, List[float]]:
        """Validate that ranges are provided for all variables and are valid"""
        variables = info.data.get('variables', [])
        
        # Check all variables have ranges
        missing_ranges = set(variables) - set(v.keys())
        if missing_ranges:
            raise ValueError(f"Missing ranges for variables: {missing_ranges}")
        
        # Validate each range
        for var, range_values in v.items():
            if len(range_values) != 2:
                raise ValueError(f"Range for {var} must have exactly 2 values [min, max]")
            if range_values[0] >= range_values[1]:
                raise ValueError(f"Invalid range for {var}: min must be less than max")
            
            # Specific validations for different variables
            if var == "discount_rate":
                if not (0 < range_values[0] < range_values[1] < 1):
                    raise ValueError("Discount rate must be between 0 and 1")
            elif var in ["operating_costs", "revenue"]:
                if not (0 < range_values[0] < range_values[1]):
                    raise ValueError(f"{var} multipliers must be positive")
            elif var == "production_volume":
                if not (0 < range_values[0] < range_values[1]):
                    raise ValueError("Production volume must be positive")
        
        return v 