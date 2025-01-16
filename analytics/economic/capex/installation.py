from typing import Dict, List


def calculate_installation_costs(
    equipment_costs: float,
    installation_factor: float = 0.2,
    indirect_costs_factor: float = 0.15,
) -> float:
    """
    Calculate installation costs based on equipment costs and factors.
    Based on paper Section 3.2.1

    Installation costs include direct installation costs (percentage of equipment costs)
    and associated indirect costs (engineering, construction, etc.).

    Args:
        equipment_costs: Total base equipment costs
        installation_factor: Factor for direct installation costs (default: 0.2 or 20%)
        indirect_costs_factor: Factor for indirect costs related to installation (default: 0.15 or 15%)

    Returns:
        float: Total installation costs including direct and indirect components

    Raises:
        ValueError: If equipment costs are negative or factors are out of range
    """
    if equipment_costs < 0:
        raise ValueError("Equipment costs cannot be negative")

    if not 0 <= installation_factor <= 1:
        raise ValueError("Installation factor must be between 0 and 1")

    if not 0 <= indirect_costs_factor <= 1:
        raise ValueError("Indirect costs factor must be between 0 and 1")

    # Calculate direct installation costs
    direct_installation = equipment_costs * installation_factor

    # Calculate indirect costs associated with installation
    indirect_installation = direct_installation * indirect_costs_factor

    # Total installation costs
    total_installation = direct_installation + indirect_installation

    return total_installation
