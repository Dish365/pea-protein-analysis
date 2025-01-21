from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period
from analytics.economic.profitability.mcsp import calculate_mcsp
from backend.fastapi_app.process_analysis.services.rust_handler import RustHandler
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProjectParameters:
    """Project financial parameters"""
    discount_rate: float
    project_duration: int
    production_volume: float
    uncertainty: float = 0.1
    monte_carlo_iterations: int = 1000

class ProfitabilityAnalysis:
    """
    Analyzes profitability metrics for protein extraction processes.
    Integrates Python implementations with optimized Rust calculations.
    """

    def __init__(self):
        self.capex_data: Dict[str, float] = {}
        self.opex_data: Dict[str, float] = {}
        self.revenue_data: Dict[str, float] = {}
        self.parameters: Optional[ProjectParameters] = None
        self.rust_handler = RustHandler()

    def set_project_data(
        self,
        capex: Dict[str, float],
        opex: Dict[str, float],
        revenue: Dict[str, float],
        parameters: ProjectParameters
    ) -> None:
        """Set all project data at once"""
        self.capex_data = capex
        self.opex_data = opex
        self.revenue_data = revenue
        self.parameters = parameters

    def _validate_data(self) -> None:
        """Validate that all required data is present"""
        if not all([self.capex_data, self.opex_data, self.revenue_data, self.parameters]):
            raise ValueError("All project data must be set before analysis")

    def _calculate_cash_flows(self) -> List[float]:
        """Calculate annual cash flows from revenue and costs"""
        self._validate_data()
        
        initial_investment = -self.capex_data["total_investment"]
        annual_flows = []
        
        for year in range(self.parameters.project_duration):
            revenue = self.revenue_data.get(f"year_{year}", 0)
            opex = self.opex_data.get("total_annual_cost", 0)
            annual_flows.append(revenue - opex)
            
        return [initial_investment] + annual_flows

    def calculate_profitability_metrics(
        self,
        use_rust: bool = True,
        target_npv: Optional[float] = None
    ) -> Dict[str, Union[float, Dict]]:
        """
        Calculate comprehensive profitability metrics using either Rust or Python
        implementations based on the use_rust flag.
        """
        try:
            self._validate_data()
            cash_flows = self._calculate_cash_flows()
            initial_investment = self.capex_data["total_investment"]

            if use_rust:
                # Use Rust implementation for core calculations
                metrics = self._calculate_metrics_rust(cash_flows, initial_investment)
            else:
                # Use Python implementation
                metrics = self._calculate_metrics_python(cash_flows, initial_investment)

            # Calculate MCSP if target NPV provided
            if target_npv is not None:
                mcsp = calculate_mcsp(
                    cash_flows=cash_flows,
                    discount_rate=self.parameters.discount_rate,
                    production_volume=self.parameters.production_volume,
                    target_npv=target_npv,
                    iterations=self.parameters.monte_carlo_iterations,
                    confidence_interval=0.95
                )
                metrics["mcsp"] = mcsp

            return metrics

        except Exception as e:
            logger.error(f"Error in profitability analysis: {str(e)}", exc_info=True)
            raise

    def _calculate_metrics_rust(
        self,
        cash_flows: List[float],
        initial_investment: float
    ) -> Dict[str, Union[float, Dict]]:
        """Calculate metrics using Rust implementation"""
        # Run Monte Carlo simulation
        monte_carlo_results = self.rust_handler.run_monte_carlo_simulation(
            cash_flows=cash_flows,
            discount_rate=self.parameters.discount_rate,
            initial_investment=initial_investment,
            iterations=self.parameters.monte_carlo_iterations,
            uncertainty=self.parameters.uncertainty
        )

        # Calculate ROI using Rust
        total_gain = sum(cash_flows[1:])  # Exclude initial investment
        roi_results = calculate_roi(
            gain_from_investment=total_gain,
            cost_of_investment=initial_investment,
            time_period=self.parameters.project_duration
        )

        return {
            "monte_carlo": monte_carlo_results,
            "roi": roi_results,
            "initial_investment": initial_investment,
            "total_gain": total_gain
        }

    def _calculate_metrics_python(
        self,
        cash_flows: List[float],
        initial_investment: float
    ) -> Dict[str, Union[float, Dict]]:
        """Calculate metrics using Python implementation"""
        npv_results = calculate_npv(
            cash_flows=cash_flows,
            discount_rate=self.parameters.discount_rate,
            initial_investment=initial_investment
        )

        roi_results = calculate_roi(
            gain_from_investment=sum(cash_flows[1:]),
            cost_of_investment=initial_investment,
            time_period=self.parameters.project_duration
        )

        payback_results = calculate_payback_period(
            initial_investment=initial_investment,
            cash_flows=cash_flows[1:],  # Exclude initial investment
            discount_rate=self.parameters.discount_rate
        )

        return {
            "npv": npv_results,
            "roi": roi_results,
            "payback": payback_results
        }

    def perform_sensitivity_analysis(
        self,
        variables: List[str],
        ranges: Dict[str, tuple],
        use_rust: bool = True
    ) -> Dict[str, List[float]]:
        """
        Perform sensitivity analysis on specified variables using either
        Rust or Python implementation.
        """
        self._validate_data()
        cash_flows = self._calculate_cash_flows()

        if use_rust:
            results = {}
            for var in variables:
                range_min, range_max = ranges[var]
                sensitivity_results = self.rust_handler.run_sensitivity_analysis(
                    base_values=cash_flows,
                    variable_index=variables.index(var),
                    range_min=range_min,
                    range_max=range_max,
                    steps=10
                )
                results[var] = sensitivity_results
            return results
        else:
            # Use existing Python implementation
            from analytics.economic.profitability.mcsp import perform_sensitivity_analysis
            return perform_sensitivity_analysis(
                base_cash_flows=cash_flows,
                discount_rate=self.parameters.discount_rate,
                production_volume=self.parameters.production_volume,
                sensitivity_range=0.2,
                steps=10
            )
