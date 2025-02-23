from typing import Dict, List, Optional


def calculate_utility_costs(
    utilities: List[Dict[str, float]],
    production_volume: float,
    reference_volume: Optional[float] = None
) -> Dict[str, float]:
    """
    Calculate utility costs with proper scaling based on production volume.
    Uses a 0.8 power rule for utility consumption scaling, which is typical for process industries.
    
    Args:
        utilities: List of utility configurations
            Each utility must have:
            - name: Utility name
            - consumption: Base consumption rate
            - unit_price: Cost per unit
            - operating_hours: Annual operating hours
            - unit: Unit of measurement
        production_volume: Current production volume
        reference_volume: Reference production volume for base consumption rates
            
    Returns:
        Dictionary containing:
        - total_cost: Total annual utility costs
        - costs_by_utility: Breakdown of costs by utility
        - consumption_rates: Scaled consumption rates
        
    Raises:
        ValueError: If utilities list is empty or contains invalid data
    """
    if not utilities:
        raise ValueError("Utilities list cannot be empty")
        
    if production_volume <= 0:
        raise ValueError("Production volume must be positive")
        
    # Use current volume as reference if not provided
    reference_volume = reference_volume or production_volume
    if reference_volume <= 0:
        raise ValueError("Reference volume must be positive")
        
    UTILITY_SCALE_EXPONENT = 0.8  # Typical scaling exponent for utility consumption
    
    total_cost = 0.0
    costs_by_utility = {}
    consumption_rates = {}
    
    for utility in utilities:
        # Validate required fields
        required_fields = ["name", "consumption", "unit_price", "operating_hours", "unit"]
        if not all(field in utility for field in required_fields):
            raise ValueError(f"Utility must contain all required fields: {required_fields}")
            
        # Calculate volume ratio for scaling
        volume_ratio = production_volume / reference_volume
        
        # Scale consumption using 0.8 power rule
        base_consumption = utility["consumption"]
        scaled_consumption = base_consumption * (volume_ratio ** UTILITY_SCALE_EXPONENT)
        
        # Calculate annual cost
        annual_cost = (
            scaled_consumption * 
            utility["unit_price"] * 
            utility["operating_hours"]
        )
        
        # Store results
        utility_name = utility["name"]
        costs_by_utility[utility_name] = annual_cost
        consumption_rates[utility_name] = {
            "base_rate": base_consumption,
            "scaled_rate": scaled_consumption,
            "unit": utility["unit"]
        }
        total_cost += annual_cost
    
    return {
        "total_cost": total_cost,
        "costs_by_utility": costs_by_utility,
        "consumption_rates": consumption_rates
    }
