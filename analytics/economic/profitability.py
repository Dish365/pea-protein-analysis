from typing import Dict, List, Optional
from .profitability.npv import calculate_npv
from .profitability.roi import calculate_roi
from .profitability.payback import calculate_payback_period
from .profitability.mcsp import calculate_mcsp, perform_sensitivity_analysis


class ProfitabilityAnalysis:
    """
    Analyzes profitability metrics for protein extraction processes.
    Based on paper Section 3.2.4 and 3.2.6
    """

    def __init__(self):
        self.cash_flows = []
        self.discount_rate = 0.0
        self.initial_investment = 0.0
        self.production_volume = 0.0

    def set_cash_flows(self, cash_flows: List[float]) -> None:
        """Set projected cash flows"""
        self.cash_flows = cash_flows

    def set_discount_rate(self, rate: float) -> None:
        """Set discount rate for NPV calculation"""
        self.discount_rate = rate

    def set_initial_investment(self, investment: float) -> None:
        """Set initial investment amount"""
        self.initial_investment = investment

    def set_production_volume(self, volume: float) -> None:
        """Set annual production volume"""
        self.production_volume = volume

    def calculate_profitability_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive profitability metrics"""
        if not self.cash_flows or self.discount_rate == 0:
            raise ValueError(
                "Cash flows and discount rate must be set before calculation"
            )

        # Calculate NPV
        npv = calculate_npv(self.cash_flows, self.discount_rate)

        # Calculate ROI
        total_cash_flow = sum(self.cash_flows)
        roi = calculate_roi(total_cash_flow, self.initial_investment)

        # Calculate payback period
        payback = calculate_payback_period(self.initial_investment, self.cash_flows)

        # Calculate MCSP
        mcsp_result = calculate_mcsp(
            self.cash_flows, self.discount_rate, self.production_volume
        )

        return {"npv": npv, "roi": roi, "payback_period": payback, "mcsp": mcsp_result}

    def perform_sensitivity_analysis(
        self, sensitivity_range: float = 0.2, steps: int = 10
    ) -> Dict[str, List[tuple]]:
        """Perform sensitivity analysis on profitability metrics"""
        if not all([self.cash_flows, self.discount_rate, self.production_volume]):
            raise ValueError("All parameters must be set before sensitivity analysis")

        return perform_sensitivity_analysis(
            self.cash_flows,
            self.discount_rate,
            self.production_volume,
            sensitivity_range,
            steps,
        )

    def get_cash_flow_summary(self) -> Dict[str, float]:
        """Get summary of cash flow analysis"""
        if not self.cash_flows:
            return {}

        return {
            "total_cash_flow": sum(self.cash_flows),
            "average_annual_cash_flow": sum(self.cash_flows) / len(self.cash_flows),
            "min_cash_flow": min(self.cash_flows),
            "max_cash_flow": max(self.cash_flows),
            "num_periods": len(self.cash_flows),
        }
