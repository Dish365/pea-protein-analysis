# Understanding NPV Sensitivity Analysis Relationships

## 1. Discount Rate Inverse Relationship

### Mathematical Foundation
The NPV calculation with discount rate (r) follows this formula:
\[ NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t} \]

Where:
- CF_t = Cash flow at time t
- r = Discount rate
- n = Number of periods

### Implementation in Code
```rust
fn calculate_npv_with_rate(cash_flows: &[f64], discount_rate: f64) -> f64 {
    calculate_npv(
        cash_flows.as_ptr(),
        cash_flows.len(),
        discount_rate
    )
}
```

### Impact Analysis
Base Case Example (from logs):
- Base discount rate: 10%
- Base NPV: $10,642,064.26
- Range: [5%, 15%]

Results show:
- At 5% (lower): $14,811,664.22 (+39.18%)
- At 15% (higher): $7,238,488.17 (-31.98%)

The inverse relationship occurs because:
1. Higher discount rates increase the denominator (1+r)^t
2. Each future cash flow gets divided by a larger number
3. This effect compounds over time (t increases)

## 2. Operating Costs Inverse Relationship

### Mathematical Foundation
Operating costs affect NPV through the cash flow calculation:
\[ CF_t = Revenue_t - (FixedCosts_t + VariableCosts_t \times factor) \]

### Implementation Details
```rust
fn calculate_with_opex_factor(
    cash_flows: &[f64], 
    factor: f64, 
    discount_rate: f64, 
    fixed_cost_ratio: f64, 
    variable_cost_ratio: f64
) -> f64 {
    let initial_investment = cash_flows[0];
    let modified_flows: Vec<f64> = std::iter::once(initial_investment)
        .chain(cash_flows[1..].iter().map(|&cf| {
            let variable_cost_portion = cf.abs() * variable_cost_ratio;
            let fixed_portion = cf.abs() * fixed_cost_ratio;
            let revenue_portion = cf + variable_cost_portion;
            revenue_portion - (variable_cost_portion * factor) - fixed_portion
        }))
        .collect();
    
    calculate_npv(
        modified_flows.as_ptr(),
        modified_flows.len(),
        discount_rate
    )
}
```

### Cost Structure Analysis
From project data:
```
Total Operating Costs: $4,072,926.29
- Fixed Costs (17.62%): $717,676.29
  • Labor: $580,008.00
  • Maintenance: $137,668.29
- Variable Costs (82.38%): $3,355,250.00
  • Raw Materials: $2,305,250.00
  • Utilities: $1,050,000.00
```

### Impact Analysis
Base Case:
- Base NPV: $7,548,302.74
- Operating cost factor range: [0.8, 1.2]

Results show:
- At 0.8 (20% lower): $10,195,667.72 (+35.07%)
- At 1.2 (20% higher): $4,522,742.76 (-40.08%)

The asymmetric impact (35.07% vs -40.08%) is explained by:

1. Variable Cost Dominance
   - 82.38% of costs are variable
   - Changes directly impact cash flows
   - Effect is proportional to the cost factor

2. Fixed Cost Leverage
   - 17.62% fixed costs create a baseline
   - Acts as a multiplier on variable cost changes
   - Creates non-linear response to cost changes

3. Time Value Compounding
   - Cost changes affect all future periods
   - Each period's change is discounted
   - Cumulative effect over project lifetime

## Key Differences Between the Two Inverse Relationships

1. Mechanism of Impact
   - Discount Rate: Affects the present value calculation directly
   - Operating Costs: Affects the cash flows before discounting

2. Timing of Impact
   - Discount Rate: Greater effect on distant cash flows
   - Operating Costs: Uniform effect across all periods

3. Linearity
   - Discount Rate: Non-linear relationship due to exponential function
   - Operating Costs: More linear relationship with some non-linearity from fixed costs

This explains why both variables show negative impacts on the right side of sensitivity graphs, but through fundamentally different mechanisms.
