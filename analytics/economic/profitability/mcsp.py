def calculate_mcsp(cash_flows, discount_rate, iterations=1000):
    import random
    npvs = []
    for _ in range(iterations):
        sampled_cash_flows = [cf * random.uniform(0.9, 1.1) for cf in cash_flows]
        npv = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(sampled_cash_flows))
        npvs.append(npv)
    return sum(npvs) / len(npvs)
