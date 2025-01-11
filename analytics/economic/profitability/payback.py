from typing import List, Dict, Optional

def calculate_payback_period(
    initial_investment: float,
    cash_flows: List[float],
    discount_rate: Optional[float] = None
) -> Dict[str, float]:
    """
    Calculate payback period for an investment.
    Based on paper Section 3.2.4
    
    Calculates both simple payback period and discounted payback period if discount rate is provided.
    
    Args:
        initial_investment: Initial investment amount
        cash_flows: List of future cash flows
        discount_rate: Optional discount rate for discounted payback period
        
    Returns:
        Dict containing:
        - simple_payback: Simple payback period in years
        - discounted_payback: Discounted payback period in years (if discount_rate provided)
        - cumulative_flows: List of cumulative cash flows
        - recovered: Boolean indicating if investment is recovered
        
    Raises:
        ValueError: If inputs are invalid
    """
    if initial_investment < 0:
        raise ValueError("Initial investment cannot be negative")
        
    if not cash_flows:
        raise ValueError("Cash flows list cannot be empty")
        
    # Calculate simple payback period
    cumulative_flow = 0
    simple_payback = None
    cumulative_flows = []
    
    for i, cf in enumerate(cash_flows):
        cumulative_flow += cf
        cumulative_flows.append(cumulative_flow)
        
        if simple_payback is None and cumulative_flow >= initial_investment:
            # Interpolate for fractional years
            if i > 0:
                prev_flow = cumulative_flows[i-1]
                fraction = (initial_investment - prev_flow) / (cumulative_flow - prev_flow)
                simple_payback = i - 1 + fraction
            else:
                simple_payback = i + 1
                
    # Calculate discounted payback period if discount rate provided
    discounted_payback = None
    if discount_rate is not None:
        if discount_rate < -1:
            raise ValueError("Discount rate cannot be less than -100%")
            
        cumulative_discounted_flow = 0
        for i, cf in enumerate(cash_flows):
            discounted_cf = cf / ((1 + discount_rate) ** (i + 1))
            cumulative_discounted_flow += discounted_cf
            
            if discounted_payback is None and cumulative_discounted_flow >= initial_investment:
                # Interpolate for fractional years
                if i > 0:
                    prev_discounted_flow = sum(cf / ((1 + discount_rate) ** (t + 1)) 
                                            for t, cf in enumerate(cash_flows[:i]))
                    fraction = (initial_investment - prev_discounted_flow) / (cumulative_discounted_flow - prev_discounted_flow)
                    discounted_payback = i - 1 + fraction
                else:
                    discounted_payback = i + 1
    
    return {
        "simple_payback": simple_payback,
        "discounted_payback": discounted_payback,
        "cumulative_flows": cumulative_flows,
        "recovered": simple_payback is not None
    }
