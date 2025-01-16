from typing import Dict, List
from .opex.utilities import calculate_utility_costs
from .opex.raw_materials import calculate_raw_material_costs
from .opex.maintenance import calculate_maintenance_costs
from .opex.labor import calculate_labor_costs


class OperationalExpenditureAnalysis:
    """
    Analyzes operational expenditure for protein extraction processes.
    Based on paper Section 3.2.2
    """

    def __init__(self):
        self.utilities = []
        self.raw_materials = []
        self.equipment_costs = 0.0
        self.labor_config = {
            "hourly_wage": 0.0,
            "hours_per_week": 0,
            "weeks_per_year": 0,
            "num_workers": 0,
        }

    def add_utility(self, utility: Dict[str, float]) -> None:
        """Add utility consumption and cost data"""
        self.utilities.append(utility)

    def add_raw_material(self, material: Dict[str, float]) -> None:
        """Add raw material quantity and cost data"""
        self.raw_materials.append(material)

    def set_equipment_costs(self, costs: float) -> None:
        """Set equipment costs for maintenance calculation"""
        self.equipment_costs = costs

    def set_labor_config(self, config: Dict[str, float]) -> None:
        """Set labor configuration"""
        self.labor_config.update(config)

    def calculate_total_opex(
        self, maintenance_factor: float = 0.05
    ) -> Dict[str, float]:
        """Calculate total operational expenditure including all components"""
        # Calculate utility costs
        utility_costs = calculate_utility_costs(self.utilities)

        # Calculate raw material costs
        material_costs = calculate_raw_material_costs(self.raw_materials)

        # Calculate maintenance costs
        maintenance_costs = calculate_maintenance_costs(
            self.equipment_costs, maintenance_factor
        )

        # Calculate labor costs
        labor_costs = calculate_labor_costs(
            self.labor_config["hourly_wage"],
            self.labor_config["hours_per_week"],
            self.labor_config["weeks_per_year"],
            self.labor_config["num_workers"],
        )

        # Calculate total OPEX
        total_opex = utility_costs + material_costs + maintenance_costs + labor_costs

        return {
            "utility_costs": utility_costs,
            "raw_material_costs": material_costs,
            "maintenance_costs": maintenance_costs,
            "labor_costs": labor_costs,
            "total_opex": total_opex,
        }

    def get_utilities_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of utility costs"""
        return self.utilities

    def get_materials_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of raw material costs"""
        return self.raw_materials

    def get_labor_breakdown(self) -> Dict[str, float]:
        """Get detailed breakdown of labor configuration"""
        return self.labor_config.copy()
