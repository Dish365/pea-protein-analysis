from typing import Dict, List

def calculate_equipment_costs(equipment_list: List[Dict[str, float]]) -> float:
    """
    Calculate the total equipment costs based on the provided equipment list.
    Based on paper Section 3.2.1
    
    Args:
        equipment_list: List of dictionaries containing equipment details
            Each dictionary should have:
            - name: Equipment name
            - cost: Base cost
            - efficiency: Equipment efficiency factor
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
        
    total_cost = 0.0
    
    for equipment in equipment_list:
        # Validate required fields
        required_fields = ['cost', 'efficiency']
        if not all(field in equipment for field in required_fields):
            raise ValueError(f"Equipment must contain all required fields: {required_fields}")
            
        # Calculate adjusted cost based on efficiency
        equipment_cost = equipment['cost']
        efficiency_factor = equipment['efficiency']
        
        # Adjust cost based on efficiency (higher efficiency = higher cost)
        adjusted_cost = equipment_cost * (1 + (efficiency_factor - 0.8) / 0.2)
        total_cost += adjusted_cost
        
    return total_cost

