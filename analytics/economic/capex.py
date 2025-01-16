from typing import Dict, List
from .capex.equipment_costs import calculate_equipment_costs
from .capex.installation import calculate_installation_costs
from .capex.indirect_costs import calculate_indirect_costs


class CapitalExpenditureAnalysis:
    """
    Analyzes capital expenditure for protein extraction processes.
    Based on paper Section 3.2.1
    """

    def __init__(self):
        self.equipment_list = []
        self.indirect_factors = []

    def add_equipment(self, equipment: Dict[str, float]) -> None:
        """Add equipment to the analysis"""
        self.equipment_list.append(equipment)

    def add_indirect_factor(self, factor: Dict[str, float]) -> None:
        """Add indirect cost factor to the analysis"""
        self.indirect_factors.append(factor)

    def calculate_total_capex(
        self, installation_factor: float = 0.2, indirect_costs_factor: float = 0.15
    ) -> Dict[str, float]:
        """Calculate total capital expenditure including all components"""
        # Calculate equipment costs
        equipment_costs = calculate_equipment_costs(self.equipment_list)

        # Calculate installation costs
        installation_costs = calculate_installation_costs(
            equipment_costs, installation_factor, indirect_costs_factor
        )

        # Calculate indirect costs
        indirect_costs = calculate_indirect_costs(self.indirect_factors)

        # Calculate total CAPEX
        total_capex = equipment_costs + installation_costs + indirect_costs

        return {
            "equipment_costs": equipment_costs,
            "installation_costs": installation_costs,
            "indirect_costs": indirect_costs,
            "total_capex": total_capex,
        }

    def get_equipment_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of equipment costs"""
        return self.equipment_list

    def get_indirect_factors_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of indirect cost factors"""
        return self.indirect_factors
