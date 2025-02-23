import numpy as np
from typing import Dict, List, Tuple


def calculate_mcsp(
    cash_flows: List[float],
    discount_rate: float,
    production_volume: float,
    target_npv: float = 0,
    iterations: int = 1000,
    confidence_interval: float = 0.95,
    random_seed: int = None  # Add seed parameter
) -> Dict[str, float]:
    """
    Calculate Minimum Concentrate Selling Price using Monte Carlo simulation.
    Based on paper Section 3.2.6

    Args:
        cash_flows: List of projected cash flows
        discount_rate: Annual discount rate
        production_volume: Annual production volume
        target_npv: Target NPV (usually 0 for MCSP calculation)
        iterations: Number of Monte Carlo iterations
        confidence_interval: Confidence interval for results
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary containing MCSP and statistical metrics
    """
    # Set random seed if provided
    if random_seed is not None:
        rng = np.random.RandomState(random_seed)
    else:
        rng = np.random.RandomState()

    npvs = []
    mcsps = []

    # Monte Carlo simulation
    for _ in range(iterations):
        # Sample cash flows with uncertainty using numpy's RNG
        sampled_flows = [cf * (1 + rng.uniform(-0.1, 0.1)) for cf in cash_flows]

        # Calculate NPV for this iteration
        npv = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(sampled_flows))
        npvs.append(npv)

        # Calculate MCSP for this iteration
        if production_volume > 0:
            mcsp = (target_npv - npv) / (
                production_volume
                * sum(1 / (1 + discount_rate) ** i for i in range(len(cash_flows)))
            )
            mcsps.append(mcsp)

    # Calculate statistics
    mean_mcsp = np.mean(mcsps)
    std_mcsp = np.std(mcsps)

    # Calculate confidence intervals
    ci_factor = 1.96  # 95% confidence interval
    ci_lower = mean_mcsp - ci_factor * std_mcsp / np.sqrt(iterations)
    ci_upper = mean_mcsp + ci_factor * std_mcsp / np.sqrt(iterations)

    return {
        "mcsp": mean_mcsp,
        "std_dev": std_mcsp,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "iterations": iterations,
        "confidence_interval": confidence_interval,
    }


def perform_sensitivity_analysis(
    base_cash_flows: List[float],
    discount_rate: float,
    production_volume: float,
    sensitivity_range: float = 0.2,
    steps: int = 10,
) -> Dict[str, List[Tuple[float, float]]]:
    """
    Perform sensitivity analysis on MCSP calculation

    Args:
        base_cash_flows: Base case cash flows
        discount_rate: Base case discount rate
        production_volume: Base case production volume
        sensitivity_range: Range for sensitivity analysis (+/- percentage)
        steps: Number of steps in sensitivity analysis

    Returns:
        Dictionary of sensitivity analysis results for each parameter
    """
    results = {"cash_flows": [], "discount_rate": [], "production_volume": []}

    # Sensitivity to cash flows
    for factor in np.linspace(1 - sensitivity_range, 1 + sensitivity_range, steps):
        modified_flows = [cf * factor for cf in base_cash_flows]
        mcsp = calculate_mcsp(modified_flows, discount_rate, production_volume)["mcsp"]
        results["cash_flows"].append((factor - 1, mcsp))  # Store as (% change, MCSP)

    # Sensitivity to discount rate
    for factor in np.linspace(1 - sensitivity_range, 1 + sensitivity_range, steps):
        modified_rate = discount_rate * factor
        mcsp = calculate_mcsp(base_cash_flows, modified_rate, production_volume)["mcsp"]
        results["discount_rate"].append((factor - 1, mcsp))

    # Sensitivity to production volume
    for factor in np.linspace(1 - sensitivity_range, 1 + sensitivity_range, steps):
        modified_volume = production_volume * factor
        mcsp = calculate_mcsp(base_cash_flows, discount_rate, modified_volume)["mcsp"]
        results["production_volume"].append((factor - 1, mcsp))

    return results
