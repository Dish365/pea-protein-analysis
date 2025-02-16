from typing import Dict, List, Any
from analytics.economic.capex.equipment_costs import calculate_equipment_costs
from analytics.economic.capex.installation import calculate_installation_costs
from analytics.economic.capex.indirect_costs import calculate_indirect_costs


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
        self, installation_factor: float,
        indirect_costs_factor: float,
        indirect_factors: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate total capital expenditure including all factors"""
        if not self.equipment_list:
            raise ValueError("Equipment list cannot be empty")
        
        # Calculate equipment costs
        equipment_costs = calculate_equipment_costs(self.equipment_list)

        # Calculate installation costs
        installation_costs = calculate_installation_costs(
            equipment_costs, installation_factor, indirect_costs_factor
        )

        # Use provided indirect factors or create default ones
        if not indirect_factors:
            base_cost = equipment_costs
            indirect_factors = [
                {
                    "name": "engineering",
                    "cost": base_cost,
                    "percentage": 0.15
                },
                {
                    "name": "contingency",
                    "cost": base_cost,
                    "percentage": 0.10
                },
                {
                    "name": "construction",
                    "cost": base_cost,
                    "percentage": 0.20
                }
            ]

        # Calculate indirect costs
        indirect_costs = calculate_indirect_costs(indirect_factors)

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
