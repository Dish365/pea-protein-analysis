from typing import Dict, List


def calculate_indirect_costs(indirect_factors: List[Dict[str, float]]) -> float:
    """
    Calculate the indirect costs based on the provided factors.
    Based on paper Section 3.2.1

    Args:
        indirect_factors: List of dictionaries containing indirect cost factors
            Each dictionary should have:
            - name: Factor name
            - cost: Base cost to apply percentage to
            - percentage: Percentage to apply (as decimal)

    Returns:
        float: Total indirect costs

    Raises:
        ValueError: If factors list is empty or missing required fields
    """
    if not indirect_factors:
        raise ValueError("Indirect factors list cannot be empty")

    total_indirect_costs = 0.0

    for factor in indirect_factors:
        # Validate required fields
        required_fields = ["cost", "percentage"]
        if not all(field in factor for field in required_fields):
            raise ValueError(
                f"Indirect factor must contain all required fields: {required_fields}"
            )

        # Calculate indirect cost for this factor
        base_cost = factor["cost"]
        percentage = factor["percentage"]

        # Apply percentage to base cost
        factor_cost = base_cost * percentage
        total_indirect_costs += factor_cost

    return total_indirect_costs
