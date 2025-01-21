from typing import Dict, List, Optional
import numpy as np

class GWPCalculator:
    """Global Warming Potential Calculator for dry fractionation process"""
    
    # GWP factors in kg CO2 eq per unit
    GWP_FACTORS = {
        'electricity': 0.5, # kg CO2 eq per kWh
        'water': 0.001, # kg CO2 eq per kg water
        'transport': 0.1, # kg CO2 eq per ton-km
    }

    def __init__(self):
        self.total_gwp = 0.0
        self.process_contributions: Dict[str, float] = {}

    def calculate_electricity_impact(self, kwh_consumed: float) -> float:
        """Calculate GWP from electricity consumption"""
        impact = kwh_consumed * self.GWP_FACTORS['electricity']
        self.process_contributions['electricity'] = impact
        return impact

    def calculate_water_impact(self, water_consumed_kg: float) -> float:
        """Calculate GWP from water consumption"""
        impact = water_consumed_kg * self.GWP_FACTORS['water']
        self.process_contributions['water'] = impact
        return impact

    def calculate_transport_impact(self, ton_km: float) -> float:
        """Calculate GWP from transportation"""
        impact = ton_km * self.GWP_FACTORS['transport']
        self.process_contributions['transport'] = impact
        return impact

    def calculate_total_impact(self, 
                             electricity_kwh: float,
                             water_kg: float,
                             transport_ton_km: float) -> float:
        """Calculate total GWP impact"""
        self.total_gwp = (
            self.calculate_electricity_impact(electricity_kwh) +
            self.calculate_water_impact(water_kg) +
            self.calculate_transport_impact(transport_ton_km)
        )
        return self.total_gwp

    def get_process_contributions(self) -> Dict[str, float]:
        """Get breakdown of GWP contributions by process"""
        return self.process_contributions 