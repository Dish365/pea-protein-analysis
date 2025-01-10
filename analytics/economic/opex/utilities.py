# Implement utility cost calculations

def calculate_utility_costs(utilities):
    """
    Calculate utility costs based on the consumption and unit price of each utility.
    """
    total_cost = sum(utility['consumption'] * utility['unit_price'] for utility in utilities)
    return total_cost