from typing import Dict, List


def calculate_equipment_costs(equipment_list: List[Dict[str, float]]) -> float:
    """
    Calculate the total equipment costs based on the provided equipment list.
    Uses the six-tenths rule for cost scaling with capacity.
    Based on paper Section 3.2.1

    Args:
        equipment_list: List of dictionaries containing equipment details
            Each dictionary should have:
            - name: Equipment name
            - base_cost: Base cost at reference capacity
            - efficiency_factor: Equipment efficiency factor
            - maintenance_cost: Annual maintenance cost
            - energy_consumption: Energy consumption rate
            - processing_capacity: Processing capacity
            - reference_capacity: Reference capacity for base cost (if not provided, assumes current capacity is reference)

    Returns:
        float: Total equipment costs

    Raises:
        ValueError: If equipment list is empty or missing required fields
    """
    if not equipment_list:
        raise ValueError("Equipment list cannot be empty")

    total = 0.0
    SCALE_EXPONENT = 0.6  # Six-tenths rule exponent

    for eq in equipment_list:
        # Validate required fields
        required_fields = ["base_cost", "efficiency_factor", "installation_complexity", "processing_capacity"]
        if not all(field in eq for field in required_fields):
            raise ValueError(f"Equipment must contain all required fields: {required_fields}")

        # Apply six-tenths rule for capacity scaling
        reference_capacity = eq.get('reference_capacity', eq['processing_capacity'])
        if reference_capacity <= 0:
            raise ValueError(f"Reference capacity must be positive for equipment: {eq.get('name', 'unknown')}")
        
        capacity_ratio = eq['processing_capacity'] / reference_capacity
        if capacity_ratio <= 0:
            raise ValueError(f"Invalid capacity ratio for equipment: {eq.get('name', 'unknown')}")
        
        # Calculate scaled cost using six-tenths rule
        scaled_cost = eq['base_cost'] * (capacity_ratio ** SCALE_EXPONENT)
        
        # Apply efficiency and complexity factors
        adjusted_cost = scaled_cost * eq['efficiency_factor'] * eq['installation_complexity']
        total += adjusted_cost

    return total
