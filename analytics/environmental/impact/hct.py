from typing import Dict
from .base import BaseEnvironmentalCalculator, ImpactFactor, ValidationConfig

class HCTCalculator(BaseEnvironmentalCalculator):
    """Human Carcinogenic Toxicity Calculator for dry fractionation process"""
    
    @property
    def IMPACT_FACTORS(self) -> Dict[str, ImpactFactor]:
        return {
            'electricity': {
                'value': 2.3e-8,
                'unit': 'CTUh/kWh',
                'description': 'Human toxicity impact from electricity consumption'
            },
            'water_treatment': {
                'value': 1.5e-9,
                'unit': 'CTUh/kg',
                'description': 'Human toxicity impact from water treatment'
            },
            'waste': {
                'value': 5.0e-9,
                'unit': 'CTUh/kg',
                'description': 'Human toxicity impact from waste handling'
            }
        }

    @property
    def VALIDATION_CONFIG(self) -> Dict[str, ValidationConfig]:
        return {
            'electricity': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kWh'
            ),
            'water_treatment': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            ),
            'waste': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            )
        }

    def calculate_total_impact(self,
                             electricity_kwh: float,
                             water_treated_kg: float,
                             waste_kg: float) -> float:
        """Calculate total HCT impact"""
        self.total_impact = (
            self.calculate_impact('electricity', electricity_kwh, 'kWh') +
            self.calculate_impact('water_treatment', water_treated_kg, 'kg') +
            self.calculate_impact('waste', waste_kg, 'kg')
        )
        return self.total_impact 