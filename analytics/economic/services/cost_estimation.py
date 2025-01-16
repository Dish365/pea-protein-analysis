from typing import Dict, List


def estimate_total_investment(
    equipment_costs: float, installation_costs: float, indirect_costs: float
) -> Dict[str, float]:
    """
    Estimate total investment costs including equipment, installation, and indirect costs.
    Based on paper Section 3.2.1
    """
    direct_costs = equipment_costs + installation_costs
    total_investment = direct_costs + indirect_costs

    return {
        "direct_costs": direct_costs,
        "indirect_costs": indirect_costs,
        "total_investment": total_investment,
    }


def estimate_annual_costs(
    capex: float, opex: Dict[str, float], project_years: int, interest_rate: float
) -> Dict[str, float]:
    """
    Estimate annual costs including capital charge and operational expenses.
    Based on paper Section 3.2.3
    """
    # Calculate annual capital charge using capital recovery factor
    capital_recovery_factor = (interest_rate * (1 + interest_rate) ** project_years) / (
        (1 + interest_rate) ** project_years - 1
    )
    annual_capital_charge = capex * capital_recovery_factor

    # Sum up all operational expenses
    total_opex = sum(opex.values())

    return {
        "annual_capital_charge": annual_capital_charge,
        "annual_opex": total_opex,
        "total_annual_cost": annual_capital_charge + total_opex,
    }
