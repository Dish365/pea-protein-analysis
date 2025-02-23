from typing import List, Dict, Union


def calculate_roi(
    gain_from_investment: Union[float, List[float]],
    cost_of_investment: float,
    time_period: int = 1,
) -> Dict[str, float]:
    """
    Calculate Return on Investment (ROI) metrics.
    Based on paper Section 3.2.4

    ROI = (Gain from Investment - Cost of Investment) / Cost of Investment

    Can handle both single-period and multi-period gains.
    For multi-period gains, calculates both simple and annualized ROI.

    Args:
        gain_from_investment: Single value or list of gains from investment
        cost_of_investment: Total investment cost
        time_period: Number of periods for annualization (default: 1)

    Returns:
        Dict containing:
        - roi: Simple ROI as decimal ratio (total return)
        - annualized_roi: Annualized ROI as decimal ratio (for multi-period)
        - total_gain: Total gain from investment
        - net_return: Net return (gain - cost)

    Raises:
        ValueError: If inputs are invalid
    """
    if not isinstance(cost_of_investment, (int, float)):
        raise ValueError("Cost of investment must be a number")
    
    if cost_of_investment <= 0:
        raise ValueError(f"Cost of investment must be positive, got: {cost_of_investment}")

    if isinstance(gain_from_investment, list):
        if not gain_from_investment:
            raise ValueError("Gains list cannot be empty")
        total_gain = sum(gain_from_investment)
    else:
        if not isinstance(gain_from_investment, (int, float)):
            raise ValueError("Gain must be a number or list of numbers")
        total_gain = gain_from_investment

    # Calculate net return
    net_return = total_gain - cost_of_investment

    # Calculate simple ROI as total return ratio
    simple_roi = net_return / cost_of_investment

    # Calculate annualized ROI for multi-period gains
    if time_period > 1:
        # Using geometric mean for annualization
        # Formula: (1 + total_roi)^(1/n) - 1
        annualized_roi = ((1 + simple_roi) ** (1 / time_period)) - 1
    else:
        annualized_roi = simple_roi

    return {
        "roi": simple_roi,  # Total ROI over entire period
        "annualized_roi": annualized_roi,  # Annualized ROI (geometric mean)
        "total_gain": total_gain,
        "net_return": net_return
    }
