from typing import Dict, List, Optional
from ..impact.gwp import GWPCalculator
from ..impact.hct import HCTCalculator
from ..impact.frs import FRSCalculator
from ..impact.water import WaterConsumptionCalculator

class ImpactCalculator:
    """Environmental Impact Calculator Service"""
    
    def __init__(self):
        self.gwp_calculator = GWPCalculator()
        self.hct_calculator = HCTCalculator()
        self.frs_calculator = FRSCalculator()
        self.water_calculator = WaterConsumptionCalculator()
        self.total_impacts: Dict[str, float] = {}

    def calculate_process_impacts(self,
                                electricity_kwh: float,
                                water_kg: float,
                                transport_ton_km: float,
                                product_kg: float,
                                equipment_kg: float,
                                cooling_kwh: float,
                                waste_kg: float) -> Dict[str, float]:
        """Calculate all environmental impacts for the process"""
        
        # Calculate GWP
        gwp = self.gwp_calculator.calculate_total_impact(
            electricity_kwh=electricity_kwh,
            water_kg=water_kg,
            transport_ton_km=transport_ton_km
        )
        
        # Calculate HCT
        hct = self.hct_calculator.calculate_total_toxicity(
            electricity_kwh=electricity_kwh,
            water_treated_kg=water_kg,
            waste_kg=waste_kg
        )
        
        # Calculate FRS
        frs = self.frs_calculator.calculate_total_scarcity(
            electricity_kwh=electricity_kwh,
            thermal_product_kg=product_kg * 0.3,  # Assuming 30% thermal treatment
            mechanical_product_kg=product_kg * 0.7  # Assuming 70% mechanical
        )
        
        # Calculate Water Consumption
        water = self.water_calculator.calculate_total_consumption(
            product_kg=product_kg,
            equipment_kg=equipment_kg,
            cooling_kwh=cooling_kwh
        )
        
        self.total_impacts = {
            'gwp': gwp,
            'hct': hct,
            'frs': frs,
            'water_consumption': water
        }
        
        return self.total_impacts

    def get_process_contributions(self) -> Dict[str, Dict[str, float]]:
        """Get detailed breakdown of environmental impacts by process"""
        return {
            'gwp': self.gwp_calculator.get_process_contributions(),
            'hct': self.hct_calculator.get_process_contributions(),
            'frs': self.frs_calculator.get_process_contributions(),
            'water': self.water_calculator.get_process_contributions()
        } 