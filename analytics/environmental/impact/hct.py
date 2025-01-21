from typing import Dict, List, Optional
import numpy as np

class HCTCalculator:
    """Human Carcinogenic Toxicity Calculator for dry fractionation process"""
    
    # HCT factors in CTUh (Comparative Toxic Units for humans) per unit
    HCT_FACTORS = {
        'electricity': 2.3e-8,  # CTUh per kWh
        'water_treatment': 1.5e-9,  # CTUh per kg water treated
        'waste': 5.0e-9,  # CTUh per kg waste
    }

    def __init__(self):
        self.total_hct = 0.0
        self.process_contributions: Dict[str, float] = {}

    def calculate_electricity_toxicity(self, kwh_consumed: float) -> float:
        """Calculate HCT from electricity consumption"""
        impact = kwh_consumed * self.HCT_FACTORS['electricity']
        self.process_contributions['electricity'] = impact
        return impact

    def calculate_water_treatment_toxicity(self, water_treated_kg: float) -> float:
        """Calculate HCT from water treatment"""
        impact = water_treated_kg * self.HCT_FACTORS['water_treatment']
        self.process_contributions['water_treatment'] = impact
        return impact

    def calculate_waste_toxicity(self, waste_kg: float) -> float:
        """Calculate HCT from waste generation"""
        impact = waste_kg * self.HCT_FACTORS['waste']
        self.process_contributions['waste'] = impact
        return impact

    def calculate_total_toxicity(self,
                               electricity_kwh: float,
                               water_treated_kg: float,
                               waste_kg: float) -> float:
        """Calculate total HCT impact"""
        self.total_hct = (
            self.calculate_electricity_toxicity(electricity_kwh) +
            self.calculate_water_treatment_toxicity(water_treated_kg) +
            self.calculate_waste_toxicity(waste_kg)
        )
        return self.total_hct

    def get_process_contributions(self) -> Dict[str, float]:
        """Get breakdown of HCT contributions by process"""
        return self.process_contributions 