from typing import Dict
from .base import BaseEnvironmentalCalculator, ImpactFactor, ValidationConfig

class GWPCalculator(BaseEnvironmentalCalculator):
    """Global Warming Potential Calculator for dry fractionation process"""
    
    @property
    def IMPACT_FACTORS(self) -> Dict[str, ImpactFactor]:
        return {
            'electricity': {
                'value': 0.5,
                'unit': 'kg_CO2_eq/kWh',
                'description': 'CO2 equivalent emissions from electricity consumption'
            },
            'water': {
                'value': 0.001,
                'unit': 'kg_CO2_eq/kg',
                'description': 'CO2 equivalent emissions from water usage'
            },
            'transport': {
                'value': 0.1,
                'unit': 'kg_CO2_eq/ton_km',
                'description': 'CO2 equivalent emissions from transportation'
            }
        }

    @property
    def VALIDATION_CONFIG(self) -> Dict[str, ValidationConfig]:
        return {
            'electricity': ValidationConfig(
                min_value=0.0,
                max_value=1e6,  # 1 million kWh as reasonable upper limit
                allow_zero=True,
                required_unit='kWh'
            ),
            'water': ValidationConfig(
                min_value=0.0,
                max_value=1e6,  # 1 million kg as reasonable upper limit
                allow_zero=True,
                required_unit='kg'
            ),
            'transport': ValidationConfig(
                min_value=0.0,
                max_value=1e6,  # 1 million ton-km as reasonable upper limit
                allow_zero=True,
                required_unit='ton_km'
            )
        }

    def calculate_total_impact(self,
                             electricity_kwh: float,
                             water_kg: float,
                             transport_ton_km: float) -> float:
        """Calculate total GWP impact"""
        self.total_impact = (
            self.calculate_impact('electricity', electricity_kwh, 'kWh') +
            self.calculate_impact('water', water_kg, 'kg') +
            self.calculate_impact('transport', transport_ton_km, 'ton_km')
        )
        return self.total_impact 