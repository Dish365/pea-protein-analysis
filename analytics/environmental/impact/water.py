from typing import Dict, List, Optional
import numpy as np

class WaterConsumptionCalculator:
    """Water Consumption Calculator for dry fractionation process"""
    
    # Water consumption factors in kg water per unit
    WATER_FACTORS = {
        'tempering': 1.0,  # kg water per kg product
        'cleaning': 0.5,  # kg water per kg equipment
        'cooling': 0.3,  # kg water per kWh cooling
    }

    def __init__(self):
        self.total_water = 0.0
        self.process_contributions: Dict[str, float] = {}

    def calculate_tempering_consumption(self, product_kg: float) -> float:
        """Calculate water consumption from tempering"""
        consumption = product_kg * self.WATER_FACTORS['tempering']
        self.process_contributions['tempering'] = consumption
        return consumption

    def calculate_cleaning_consumption(self, equipment_kg: float) -> float:
        """Calculate water consumption from equipment cleaning"""
        consumption = equipment_kg * self.WATER_FACTORS['cleaning']
        self.process_contributions['cleaning'] = consumption
        return consumption

    def calculate_cooling_consumption(self, cooling_kwh: float) -> float:
        """Calculate water consumption from cooling"""
        consumption = cooling_kwh * self.WATER_FACTORS['cooling']
        self.process_contributions['cooling'] = consumption
        return consumption

    def calculate_total_consumption(self,
                                  product_kg: float,
                                  equipment_kg: float,
                                  cooling_kwh: float) -> float:
        """Calculate total water consumption"""
        self.total_water = (
            self.calculate_tempering_consumption(product_kg) +
            self.calculate_cleaning_consumption(equipment_kg) +
            self.calculate_cooling_consumption(cooling_kwh)
        )
        return self.total_water

    def get_process_contributions(self) -> Dict[str, float]:
        """Get breakdown of water consumption by process"""
        return self.process_contributions 