from typing import Dict, List

def calculate_utility_costs(utilities: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate utility costs based on consumption and unit price of each utility.
    Based on paper Section 3.2.2
    
    Args:
        utilities: List of dictionaries containing utility details
            Each dictionary should have:
            - name: Utility name (e.g., electricity, water, steam)
            - consumption: Annual consumption amount
            - unit_price: Price per unit
            - unit: Unit of measurement
            
    Returns:
        Dict containing:
        - total_cost: Total cost of all utilities
        - utility_costs: Dictionary of costs by utility type
        - consumption_data: Dictionary of consumption by utility type
        
    Raises:
        ValueError: If utilities list is empty or missing required fields
    """
    if not utilities:
        raise ValueError("Utilities list cannot be empty")
        
    total_cost = 0.0
    utility_costs = {}
    consumption_data = {}
    
    for utility in utilities:
        # Validate required fields
        required_fields = ['name', 'consumption', 'unit_price']
        if not all(field in utility for field in required_fields):
            raise ValueError(f"Utility must contain all required fields: {required_fields}")
            
        # Validate numeric values
        if utility['consumption'] < 0:
            raise ValueError(f"Consumption cannot be negative for utility: {utility.get('name', 'unknown')}")
            
        if utility['unit_price'] < 0:
            raise ValueError(f"Unit price cannot be negative for utility: {utility.get('name', 'unknown')}")
            
        # Calculate cost for this utility
        utility_cost = utility['consumption'] * utility['unit_price']
        
        # Store results
        utility_name = utility['name']
        utility_costs[utility_name] = utility_cost
        consumption_data[utility_name] = {
            'consumption': utility['consumption'],
            'unit': utility.get('unit', 'unit')
        }
        total_cost += utility_cost
        
    return {
        "total_cost": total_cost,
        "utility_costs": utility_costs,
        "consumption_data": consumption_data
    }