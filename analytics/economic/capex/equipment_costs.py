from typing import Dict, List


def calculate_equipment_costs(equipment_list: List[Dict[str, float]]) -> float:
    """
    Calculate the total equipment costs based on the provided equipment list.
    Based on paper Section 3.2.1

    Args:
        equipment_list: List of dictionaries containing equipment details
            Each dictionary should have:
            - name: Equipment name
            - base_cost: Base cost
            - efficiency_factor: Equipment efficiency factor
            - maintenance_cost: Annual maintenance cost
            - energy_consumption: Energy consumption rate
            - processing_capacity: Processing capacity

    Returns:
        float: Total equipment costs

    Raises:
        ValueError: If equipment list is empty or missing required fields
    """
    if not equipment_list:
        raise ValueError("Equipment list cannot be empty")

    total = 0

    for eq in equipment_list:
        # Validate required fields
        required_fields = ["base_cost", "efficiency_factor", "installation_complexity"]
        if not all(field in eq for field in required_fields):
            raise ValueError(
                f"Equipment must contain all required fields: {required_fields}"
            )

        # Calculate adjusted cost based on efficiency and installation complexity
        adjusted_cost = eq['base_cost'] * (1 + eq['efficiency_factor']) * eq['installation_complexity']
        total += adjusted_cost

    return total
