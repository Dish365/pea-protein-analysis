from abc import ABC, abstractmethod
from typing import Dict, TypedDict, Optional, Union, Any
from dataclasses import dataclass
import numpy as np

class ImpactFactor(TypedDict):
    value: float
    unit: str
    description: str

class ProcessContribution(TypedDict):
    value: float
    unit: str
    process: str

@dataclass
class ValidationConfig:
    min_value: float = 0.0
    max_value: float = float('inf')
    allow_zero: bool = True
    required_unit: str = ""

class UnitConverter:
    CONVERSION_FACTORS = {
        # Basic unit conversions
        'kwh_to_mj': 3.6,
        'kg_to_ton': 0.001,
        'ton_to_kg': 1000,
        
        # GWP impact conversions
        'kwh_to_kg_co2_eq_per_kwh': 1.0,  # Direct conversion for GWP electricity
        'kg_to_kg_co2_eq_per_kg': 1.0,    # Direct conversion for GWP water
        'ton_km_to_kg_co2_eq_per_ton_km': 1.0,  # Direct conversion for GWP transport
        
        # HCT impact conversions
        'kwh_to_ctuh_per_kwh': 1.0,  # Direct conversion for HCT electricity
        'kg_to_ctuh_per_kg': 1.0,    # Direct conversion for HCT water and waste
        
        # FRS impact conversions
        'kwh_to_kg_oil_eq_per_kwh': 1.0,  # Direct conversion for FRS electricity
        'kg_to_kg_oil_eq_per_kg': 1.0,    # Direct conversion for FRS mass-based
        
        # Water impact conversions
        'kg_to_m3': 0.001,      # 1 kg water = 0.001 m3
        'm3_to_kg': 1000,       # 1 m3 = 1000 kg water
        'kg_to_kg_water_per_kg': 1.0,     # Direct conversion for water consumption per mass
        'kwh_to_kg_water_per_kwh': 1.0,   # Direct conversion for water consumption per energy
        'kg_to_kg_water_per_m3': 1000.0,  # Water density conversion
        
        # Additional water unit conversions
        'kg_to_kg_water': 1.0,  # Mass of water (direct)
        'kg_water_to_kg': 1.0,  # Mass of water (inverse)
        'kg_water_to_m3': 0.001,  # Water volume conversion
        'm3_to_kg_water': 1000.0  # Water volume conversion (inverse)
    }

    @staticmethod
    def normalize_unit(unit: str) -> str:
        """Normalize unit string for consistent comparison"""
        # Convert to lowercase and standardize separators
        unit = unit.lower().replace('-', '_').replace(' ', '_')
        
        # Handle division notation consistently
        unit = unit.replace('/', '_per_')
        
        # Ensure 'per' is used consistently
        while '__per__' in unit:
            unit = unit.replace('__per__', '_per_')
        while '_per_per_' in unit:
            unit = unit.replace('_per_per_', '_per_')
        if not unit.startswith('per_'):
            unit = unit.replace('per_', '_per_')
            
        # Normalize common unit names and compounds
        replacements = {
            'water': 'h2o',
            'co2_eq': 'co2_eq',
            'co2': 'co2',
            'oil_eq': 'oil_eq',
            'ctuh': 'ctuh',
            'kwh': 'kwh',  # Preserve kWh casing
            'kg_h2o': 'kg_water'  # Standardize water mass units
        }
        for old, new in replacements.items():
            unit = unit.replace(old, new)
            
        # Remove duplicate underscores
        while '__' in unit:
            unit = unit.replace('__', '_')
            
        # Remove leading/trailing underscores
        unit = unit.strip('_')
        
        return unit

    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between units with support for compound units"""
        if from_unit == to_unit:
            return value
        
        # Normalize units for comparison
        from_unit_norm = UnitConverter.normalize_unit(from_unit)
        to_unit_norm = UnitConverter.normalize_unit(to_unit)
        
        if from_unit_norm == to_unit_norm:
            return value
        
        # Try direct conversion
        conversion_key = f"{from_unit_norm}_to_{to_unit_norm}"
        if conversion_key in UnitConverter.CONVERSION_FACTORS:
            return value * UnitConverter.CONVERSION_FACTORS[conversion_key]
        
        # Try inverse conversion
        inverse_key = f"{to_unit_norm}_to_{from_unit_norm}"
        if inverse_key in UnitConverter.CONVERSION_FACTORS:
            return value / UnitConverter.CONVERSION_FACTORS[inverse_key]
        
        # Try compound unit conversion (for units with numerator/denominator)
        if '_per_' in from_unit_norm and '_per_' in to_unit_norm:
            from_parts = from_unit_norm.split('_per_')
            to_parts = to_unit_norm.split('_per_')
            
            if len(from_parts) == 2 and len(to_parts) == 2:
                try:
                    # Convert numerator and denominator separately if needed
                    numerator_conv = (UnitConverter.convert(1.0, from_parts[0], to_parts[0]) 
                                    if from_parts[0] != to_parts[0] else 1.0)
                    denominator_conv = (UnitConverter.convert(1.0, from_parts[1], to_parts[1]) 
                                      if from_parts[1] != to_parts[1] else 1.0)
                    return value * numerator_conv / denominator_conv
                except ValueError:
                    pass
        
        # Try water-specific conversions as fallback
        if ('water' in from_unit.lower() or 'h2o' in from_unit_norm) and \
           ('water' in to_unit.lower() or 'h2o' in to_unit_norm):
            try:
                # Try converting through kg_water as intermediate
                value_kg_water = UnitConverter.convert(value, from_unit, 'kg_water')
                return UnitConverter.convert(value_kg_water, 'kg_water', to_unit)
            except ValueError:
                # Try converting through m3 as intermediate
                try:
                    value_m3 = UnitConverter.convert(value, from_unit, 'm3')
                    return UnitConverter.convert(value_m3, 'm3', to_unit)
                except ValueError:
                    pass
            
        raise ValueError(f"No conversion factor found for {from_unit} to {to_unit}")

class BaseEnvironmentalCalculator(ABC):
    """Base class for all environmental impact calculators"""
    
    @property
    @abstractmethod
    def IMPACT_FACTORS(self) -> Dict[str, ImpactFactor]:
        """Impact factors specific to each calculator"""
        pass

    @property
    @abstractmethod
    def VALIDATION_CONFIG(self) -> Dict[str, ValidationConfig]:
        """Validation configuration for input parameters"""
        pass

    def __init__(self):
        self.total_impact: float = 0.0
        self.process_contributions: Dict[str, ProcessContribution] = {}
        self._validate_factors()

    def _validate_factors(self) -> None:
        """Validate impact factors during initialization"""
        if not isinstance(self.IMPACT_FACTORS, dict):
            raise TypeError("IMPACT_FACTORS must be a dictionary")
        
        for process, factor in self.IMPACT_FACTORS.items():
            if not isinstance(factor, dict):
                raise TypeError(f"Impact factor for {process} must be a dictionary")
            if 'value' not in factor or 'unit' not in factor:
                raise ValueError(f"Impact factor for {process} missing required fields")

    def validate_input(self, value: float, process_name: str) -> None:
        """Validate input values against configuration"""
        config = self.VALIDATION_CONFIG.get(process_name, ValidationConfig())
        
        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid type for {process_name}: {type(value)}")
        
        if np.isnan(value) or np.isinf(value):
            raise ValueError(f"Invalid value for {process_name}: {value}")
            
        if value < config.min_value:
            raise ValueError(f"Value for {process_name} below minimum: {value} < {config.min_value}")
            
        if value > config.max_value:
            raise ValueError(f"Value for {process_name} above maximum: {value} > {config.max_value}")
            
        if not config.allow_zero and value == 0:
            raise ValueError(f"Zero value not allowed for {process_name}")

    def calculate_impact(self, process_name: str, value: float, input_unit: str = "") -> float:
        """Calculate environmental impact for a specific process"""
        self.validate_input(value, process_name)
        
        if process_name not in self.IMPACT_FACTORS:
            raise ValueError(f"Unknown process: {process_name}")
            
        factor = self.IMPACT_FACTORS[process_name]
        
        # Convert units if needed
        if input_unit and input_unit != factor['unit']:
            value = UnitConverter.convert(value, input_unit, factor['unit'])
        
        impact = value * factor['value']
        
        self.process_contributions[process_name] = {
            'value': impact,
            'unit': factor['unit'],
            'process': process_name
        }
        
        return impact

    def get_process_contributions(self) -> Dict[str, ProcessContribution]:
        """Get breakdown of impacts by process"""
        return self.process_contributions

    def get_total_impact(self) -> float:
        """Get total calculated impact"""
        return self.total_impact

    @abstractmethod
    def calculate_total_impact(self, **kwargs) -> float:
        """Calculate total environmental impact"""
        pass 