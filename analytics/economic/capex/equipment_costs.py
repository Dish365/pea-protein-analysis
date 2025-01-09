# ...existing code...

def calculate_equipment_costs(equipment_list):
    """
    Calculate the total equipment costs including installation and indirect costs.
    """
    total_cost = 0
    for equipment in equipment_list:
        equipment_cost = equipment['cost']
        installation_cost = equipment_cost * 0.2  # 20% installation factor
        indirect_cost = (equipment_cost + installation_cost) * 0.15  # 15% indirect costs factor
        total_cost += equipment_cost + installation_cost + indirect_cost
    return total_cost

# ...existing code...
