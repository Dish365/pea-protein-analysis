from typing import List, Dict


def calculate_npv(
    cash_flows: List[float], discount_rate: float, initial_investment: float = 0.0
) -> Dict[str, float]:
    """
    Calculate Net Present Value (NPV) of a series of cash flows.
    Based on paper Section 3.2.4

    NPV is calculated as the sum of discounted cash flows minus the initial investment:
    NPV = -I0 + Σ(CFt / (1 + r)^t)
    where:
    - I0 is the initial investment
    - CFt is the cash flow at time t
    - r is the discount rate

    Args:
        cash_flows: List of future cash flows
        discount_rate: Annual discount rate (as decimal)
        initial_investment: Initial investment amount (default: 0.0)

    Returns:
        Dict containing:
        - npv: Calculated NPV
        - discounted_flows: List of discounted cash flows
        - cumulative_npv: Cumulative NPV by period

    Raises:
        ValueError: If discount rate is invalid or no cash flows provided
    """
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")

    if discount_rate < -1:  # Allow negative rates but not less than -100%
        raise ValueError("Discount rate cannot be less than -100%")

    # Initialize results
    discounted_flows = []
    cumulative_npv = []
    running_npv = -initial_investment

    # Calculate discounted cash flows and NPV
    for t, cf in enumerate(cash_flows, 1):  # Start from period 1
        # Calculate discount factor
        discount_factor = 1 / (1 + discount_rate) ** t

        # Calculate discounted cash flow
        discounted_cf = cf * discount_factor
        discounted_flows.append(discounted_cf)

        # Update running NPV
        running_npv += discounted_cf
        cumulative_npv.append(running_npv)

    return {
        "npv": running_npv,
        "discounted_flows": discounted_flows,
        "cumulative_npv": cumulative_npv,
    }
