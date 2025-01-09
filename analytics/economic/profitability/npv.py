def calculate_npv(cash_flows, discount_rate):
    npv = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows))
    return npv
