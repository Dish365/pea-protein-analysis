def calculate_payback_period(initial_investment, cash_flows):
    cumulative_cash_flow = 0
    for i, cf in enumerate(cash_flows):
        cumulative_cash_flow += cf
        if cumulative_cash_flow >= initial_investment:
            return i + 1
    return None
