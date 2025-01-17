from typing import Dict, List
from analytics.economic.opex.raw_materials import calculate_raw_material_costs
from analytics.economic.opex.utilities import calculate_utility_costs
from analytics.economic.opex.labor import calculate_labor_costs
from analytics.economic.opex.maintenance import calculate_maintenance_costs


class OperationalExpenditureAnalysis:
    """
    Analyzes operational expenditure for protein extraction processes.
    Based on paper Section 3.2.2
    """

    def __init__(self):
        self.raw_materials = []
        self.utilities = []
        self.labor_data = {}
        self.maintenance_factors = {}

    def add_raw_material(self, material: Dict[str, float]) -> None:
        """Add raw material to the analysis"""
        self.raw_materials.append(material)

    def add_utility(self, utility: Dict[str, float]) -> None:
        """Add utility consumption data"""
        self.utilities.append(utility)

    def set_labor_data(self, labor_data: Dict[str, float]) -> None:
        """Set labor cost data"""
        self.labor_data = labor_data

    def set_maintenance_factors(self, factors: Dict[str, float]) -> None:
        """Set maintenance cost factors"""
        self.maintenance_factors = factors

    def calculate_total_opex(self) -> Dict[str, float]:
        """Calculate total operational expenditure including all components"""
        # Calculate raw material costs
        raw_material_costs = calculate_raw_material_costs(self.raw_materials)

        # Calculate utility costs
        utility_costs = calculate_utility_costs(self.utilities)

        # Calculate labor costs
        labor_costs = calculate_labor_costs(self.labor_data)

        # Calculate maintenance costs
        maintenance_costs = calculate_maintenance_costs(self.maintenance_factors)

        # Calculate total OPEX
        total_opex = (
            raw_material_costs +
            utility_costs +
            labor_costs +
            maintenance_costs
        )

        return {
            "raw_material_costs": raw_material_costs,
            "utility_costs": utility_costs,
            "labor_costs": labor_costs,
            "maintenance_costs": maintenance_costs,
            "total_opex": total_opex,
        }

    def get_raw_materials_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of raw material costs"""
        return self.raw_materials

    def get_utilities_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of utility costs"""
        return self.utilities
