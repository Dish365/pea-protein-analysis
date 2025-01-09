# ...existing code...

def calculate_installation_costs(equipment_costs, installation_factor=0.2, indirect_costs_factor=0.15):
    """
    Calculate installation costs based on equipment costs, installation factor, and indirect costs factor.
    """
    direct_costs = equipment_costs * (1 + installation_factor)
    indirect_costs = direct_costs * indirect_costs_factor
    total_installation_costs = direct_costs + indirect_costs
    return total_installation_costs

# ...existing code...
