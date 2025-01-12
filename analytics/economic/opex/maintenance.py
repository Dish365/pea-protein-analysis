from typing import Dict, List, Optional

def calculate_maintenance_costs(
    equipment_costs: float,
    maintenance_factor: float = 0.05,
    additional_maintenance: Optional[Dict[str, float]] = None
) -> float:
    """
    Calculate maintenance costs based on equipment costs and maintenance factor.
    Based on paper Section 3.2.2
    
    Args:
        equipment_costs: Total equipment costs
        maintenance_factor: Annual maintenance cost as fraction of equipment costs (default: 0.05 or 5%)
        additional_maintenance: Dictionary of additional maintenance costs by category (optional)
        
    Returns:
        float: Total annual maintenance costs
        
    Raises:
        ValueError: If equipment costs are negative or maintenance factor is invalid
    """
    if equipment_costs < 0:
        raise ValueError("Equipment costs cannot be negative")
        
    if not 0 <= maintenance_factor <= 1:
        raise ValueError("Maintenance factor must be between 0 and 1")
        
    # Calculate base maintenance costs
    base_maintenance = equipment_costs * maintenance_factor
    
    # Add any additional maintenance costs
    additional_costs = 0.0
    if additional_maintenance:
        additional_costs = sum(additional_maintenance.values())
        
        # Validate additional costs
        if additional_costs < 0:
            raise ValueError("Additional maintenance costs cannot be negative")
            
    # Total maintenance costs
    total_maintenance = base_maintenance + additional_costs
    
    return total_maintenance
