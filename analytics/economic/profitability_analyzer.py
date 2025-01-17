from typing import Dict, List, Optional
from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period
from analytics.economic.profitability.mcsp import calculate_mcsp


class ProfitabilityAnalysis:
    """
    Analyzes profitability metrics for protein extraction processes.
    Based on paper Section 3.2.4
    """

    def __init__(self):
        self.capex_data = {}
        self.opex_data = {}
        self.revenue_data = {}
        self.project_parameters = {}

    def set_capex_data(self, capex_data: Dict[str, float]) -> None:
        """Set capital expenditure data"""
        self.capex_data = capex_data

    def set_opex_data(self, opex_data: Dict[str, float]) -> None:
        """Set operational expenditure data"""
        self.opex_data = opex_data

    def set_revenue_data(self, revenue_data: Dict[str, float]) -> None:
        """Set revenue projection data"""
        self.revenue_data = revenue_data

    def set_project_parameters(self, parameters: Dict[str, float]) -> None:
        """Set project parameters (discount rate, project life, etc.)"""
        self.project_parameters = parameters

    def calculate_profitability_metrics(
        self,
        target_npv: Optional[float] = None
    ) -> Dict[str, float]:
        """Calculate comprehensive profitability metrics"""
        # Calculate NPV
        npv = calculate_npv(
            self.capex_data,
            self.opex_data,
            self.revenue_data,
            self.project_parameters
        )

        # Calculate ROI
        roi = calculate_roi(
            self.capex_data,
            self.opex_data,
            self.revenue_data
        )

        # Calculate payback period
        payback = calculate_payback_period(
            self.capex_data,
            self.opex_data,
            self.revenue_data
        )

        # Calculate MCSP if target NPV provided
        mcsp = None
        if target_npv is not None:
            mcsp = calculate_mcsp(
                target_npv,
                self.capex_data,
                self.opex_data,
                self.project_parameters
            )

        metrics = {
            "npv": npv,
            "roi": roi,
            "payback_period": payback,
        }

        if mcsp is not None:
            metrics["mcsp"] = mcsp

        return metrics

    def get_sensitivity_analysis(
        self,
        variables: List[str],
        ranges: Dict[str, tuple]
    ) -> Dict[str, List[float]]:
        """Perform sensitivity analysis on specified variables"""
        # Implementation for sensitivity analysis
        pass
