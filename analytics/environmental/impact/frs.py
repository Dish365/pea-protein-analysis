from typing import Dict
from .base import BaseEnvironmentalCalculator, ImpactFactor, ValidationConfig

class FRSCalculator(BaseEnvironmentalCalculator):
    """Fossil Resource Scarcity Calculator for dry fractionation process"""
    
    @property
    def IMPACT_FACTORS(self) -> Dict[str, ImpactFactor]:
        return {
            'electricity': {
                'value': 0.2,
                'unit': 'kg_oil_eq/kWh',
                'description': 'Oil equivalent consumption from electricity usage'
            },
            'thermal_treatment': {
                'value': 0.1,
                'unit': 'kg_oil_eq/kg',
                'description': 'Oil equivalent consumption from thermal processing'
            },
            'mechanical_processing': {
                'value': 0.05,
                'unit': 'kg_oil_eq/kg',
                'description': 'Oil equivalent consumption from mechanical processing'
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
            'thermal_treatment': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            ),
            'mechanical_processing': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            )
        }

    def calculate_total_impact(self,
                             electricity_kwh: float,
                             thermal_product_kg: float,
                             mechanical_product_kg: float) -> float:
        """Calculate total FRS impact"""
        self.total_impact = (
            self.calculate_impact('electricity', electricity_kwh, 'kWh') +
            self.calculate_impact('thermal_treatment', thermal_product_kg, 'kg') +
            self.calculate_impact('mechanical_processing', mechanical_product_kg, 'kg')
        )
        return self.total_impact 