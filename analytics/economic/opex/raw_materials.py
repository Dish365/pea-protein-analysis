from typing import Dict, List


def calculate_raw_material_costs(materials: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Calculate raw material costs based on quantity and unit price of each material.
    Based on paper Section 3.2.2

    Args:
        materials: List of dictionaries containing material details
            Each dictionary should have:
            - name: Material name
            - quantity: Annual consumption quantity
            - unit_price: Price per unit
            - unit: Unit of measurement

    Returns:
        Dict containing:
        - total_cost: Total cost of all materials
        - material_costs: Dictionary of costs by material name

    Raises:
        ValueError: If materials list is empty or missing required fields
    """
    if not materials:
        raise ValueError("Materials list cannot be empty")

    total_cost = 0.0
    material_costs = {}

    for material in materials:
        # Validate required fields
        required_fields = ["name", "quantity", "unit_price"]
        if not all(field in material for field in required_fields):
            raise ValueError(
                f"Material must contain all required fields: {required_fields}"
            )

        # Validate numeric values
        if material["quantity"] < 0:
            raise ValueError(
                f"Quantity cannot be negative for material: {material.get('name', 'unknown')}"
            )

        if material["unit_price"] < 0:
            raise ValueError(
                f"Unit price cannot be negative for material: {material.get('name', 'unknown')}"
            )

        # Calculate cost for this material
        material_cost = material["quantity"] * material["unit_price"]
        material_costs[material["name"]] = material_cost
        total_cost += material_cost

    return {"total_cost": total_cost, "material_costs": material_costs}
