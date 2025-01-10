# Implement raw material cost tracking

def calculate_raw_material_costs(materials):
    """
    Calculate raw material costs based on the quantity and unit price of each material.
    """
    total_cost = sum(material['quantity'] * material['unit_price'] for material in materials)
    return total_cost
