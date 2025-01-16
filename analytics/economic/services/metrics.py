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
):
    metrics = {
        "NPV": calculate_npv(cash_flows, discount_rate),
        "ROI": calculate_roi(gain_from_investment, cost_of_investment),
        "Payback Period": calculate_payback_period(initial_investment, cash_flows),
        "MCSP": calculate_mcsp(cash_flows, discount_rate),
    }
    return metrics
