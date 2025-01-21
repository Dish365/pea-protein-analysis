from typing import Dict, List, Optional
import numpy as np

class FRSCalculator:
    """Fossil Resource Scarcity Calculator for dry fractionation process"""
    
    # FRS factors in kg oil eq per unit
    FRS_FACTORS = {
        'electricity': 0.2,  # kg oil eq per kWh
        'thermal_treatment': 0.1,  # kg oil eq per kg product
        'mechanical_processing': 0.05,  # kg oil eq per kg product
    }

    def __init__(self):
        self.total_frs = 0.0
        self.process_contributions: Dict[str, float] = {}

    def calculate_electricity_scarcity(self, kwh_consumed: float) -> float:
        """Calculate FRS from electricity consumption"""
        impact = kwh_consumed * self.FRS_FACTORS['electricity']
        self.process_contributions['electricity'] = impact
        return impact

    def calculate_thermal_treatment_scarcity(self, product_kg: float) -> float:
        """Calculate FRS from thermal treatment"""
        impact = product_kg * self.FRS_FACTORS['thermal_treatment']
        self.process_contributions['thermal_treatment'] = impact
        return impact

    def calculate_mechanical_scarcity(self, product_kg: float) -> float:
        """Calculate FRS from mechanical processing"""
        impact = product_kg * self.FRS_FACTORS['mechanical_processing']
        self.process_contributions['mechanical_processing'] = impact
        return impact

    def calculate_total_scarcity(self,
                               electricity_kwh: float,
                               thermal_product_kg: float,
                               mechanical_product_kg: float) -> float:
        """Calculate total FRS impact"""
        self.total_frs = (
            self.calculate_electricity_scarcity(electricity_kwh) +
            self.calculate_thermal_treatment_scarcity(thermal_product_kg) +
            self.calculate_mechanical_scarcity(mechanical_product_kg)
        )
        return self.total_frs

    def get_process_contributions(self) -> Dict[str, float]:
        """Get breakdown of FRS contributions by process"""
        return self.process_contributions 