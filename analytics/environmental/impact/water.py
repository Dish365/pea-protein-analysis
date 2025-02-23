from typing import Dict
from .base import BaseEnvironmentalCalculator, ImpactFactor, ValidationConfig

class WaterConsumptionCalculator(BaseEnvironmentalCalculator):
    """Water Consumption Calculator for dry fractionation process"""
    
    @property
    def IMPACT_FACTORS(self) -> Dict[str, ImpactFactor]:
        return {
            'tempering': {
                'value': 1.0,
                'unit': 'kg_water_per_kg',
                'description': 'Water consumption from product tempering'
            },
            'cleaning': {
                'value': 0.5,
                'unit': 'kg_water_per_kg',
                'description': 'Water consumption from equipment cleaning'
            },
            'cooling': {
                'value': 0.3,
                'unit': 'kg_water_per_kwh',
                'description': 'Water consumption from cooling operations'
            }
        }

    @property
    def VALIDATION_CONFIG(self) -> Dict[str, ValidationConfig]:
        return {
            'tempering': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            ),
            'cleaning': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kg'
            ),
            'cooling': ValidationConfig(
                min_value=0.0,
                max_value=1e6,
                allow_zero=True,
                required_unit='kWh'
            )
        }

    def calculate_total_impact(self,
                             product_kg: float,
                             equipment_kg: float,
                             cooling_kwh: float) -> float:
        """Calculate total water consumption"""
        self.total_impact = (
            self.calculate_impact('tempering', product_kg, 'kg') +
            self.calculate_impact('cleaning', equipment_kg, 'kg') +
            self.calculate_impact('cooling', cooling_kwh, 'kWh')
        )
        return self.total_impact 