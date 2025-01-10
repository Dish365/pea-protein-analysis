# ...existing code...

def calculate_indirect_costs(indirect_factors):
    """
    Calculate the indirect costs based on the provided factors.
    """
    total_indirect_costs = 0
    for factor in indirect_factors:
        total_indirect_costs += factor['cost'] * factor['percentage']
    return total_indirect_costs

# ...existing code...
