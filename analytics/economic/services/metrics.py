from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period
from analytics.economic.profitability.mcsp import calculate_mcsp


def get_economic_metrics(
    cash_flows,
    discount_rate,
    initial_investment,
    gain_from_investment,
    cost_of_investment,
    production_volume: float = 1000.0,
    target_npv: float = 0.0,
    monte_carlo_iterations: int = 1000,
    confidence_interval: float = 0.95
):
    """Calculate comprehensive economic metrics for the investment."""
    # Calculate NPV with initial investment
    npv_result = calculate_npv(
        cash_flows=cash_flows,
        discount_rate=discount_rate,
        initial_investment=initial_investment
    )
    
    # Calculate ROI metrics (using total gain)
    roi_result = calculate_roi(
        gain_from_investment=gain_from_investment,
        cost_of_investment=cost_of_investment
    )
    
    # Calculate payback period with discount rate
    payback_result = calculate_payback_period(
        initial_investment=initial_investment,
        cash_flows=cash_flows,
        discount_rate=discount_rate
    )
    
    # Calculate MCSP with all parameters
    mcsp_result = calculate_mcsp(
        cash_flows=cash_flows,
        discount_rate=discount_rate,
        production_volume=production_volume,
        target_npv=target_npv,
        iterations=monte_carlo_iterations,
        confidence_interval=confidence_interval
    )
    
    return {
        "NPV": npv_result["npv"],
        "ROI": roi_result["roi"],
        "Payback Period": payback_result["simple_payback"],
        "Discounted Payback Period": payback_result["discounted_payback"],
        "MCSP": mcsp_result["mcsp"],
        "details": {
            "npv_analysis": npv_result,
            "roi_analysis": roi_result,
            "payback_analysis": payback_result,
            "mcsp_analysis": mcsp_result
        }
    }
