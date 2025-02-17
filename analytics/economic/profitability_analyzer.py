from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period
from analytics.economic.profitability.mcsp import calculate_mcsp
from backend.fastapi_app.process_analysis.services.rust_handler import RustHandler
import logging
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class ProjectParameters:
    """Project financial parameters"""
    discount_rate: float
    project_duration: int
    production_volume: float
    uncertainty: float = 0.1
    monte_carlo_iterations: int = 1000
    random_seed: Optional[int] = None  # Add seed control

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
        self.rng = np.random.RandomState()  # Initialize RNG

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
        
        # Set random seed if provided
        if parameters.random_seed is not None:
            self.rng = np.random.RandomState(parameters.random_seed)

    def _validate_data(self) -> None:
        """Validate that all required data is present"""
        if not all([self.capex_data, self.opex_data, self.revenue_data, self.parameters]):
            raise ValueError("All project data must be set before analysis")

    def _calculate_cash_flows(self) -> List[float]:
        """Centralized cash flow calculation with enhanced validation"""
        self._validate_data()
        
        try:
            # Calculate initial investment (negative cash flow)
            initial_investment = -self.capex_data["total_investment"]
            
            # Calculate annual operating costs
            annual_opex = self.opex_data["total_annual_cost"]
            
            # Calculate annual revenue from price and production
            if isinstance(self.revenue_data, dict):
                if "product_price" in self.revenue_data and "annual_production" in self.revenue_data:
                    base_revenue = self.revenue_data["product_price"] * self.revenue_data["annual_production"]
                elif "annual" in self.revenue_data:
                    base_revenue = self.revenue_data["annual"]
                else:
                    raise ValueError("Revenue data must contain either 'product_price' and 'annual_production' or 'annual'")
            else:
                raise ValueError("Invalid revenue data format")
            
            # Apply Monte Carlo simulation for uncertainty using seeded RNG
            annual_flows = []
            for year in range(self.parameters.project_duration):
                # Revenue uncertainty
                revenue_uncertainty = self.parameters.uncertainty * self.rng.uniform(-1, 1)
                annual_revenue = base_revenue * (1 + revenue_uncertainty)
                
                # Cost uncertainty
                cost_uncertainty = self.parameters.uncertainty * self.rng.uniform(-1, 1)
                year_opex = annual_opex * (1 + cost_uncertainty)
                
                # Net cash flow for the year
                net_cash_flow = annual_revenue - year_opex
                annual_flows.append(net_cash_flow)
            
            # Return complete cash flow series
            cash_flows = [initial_investment] + annual_flows
            logger.debug(f"Generated cash flows: {cash_flows}")
            
            return cash_flows
            
        except KeyError as e:
            logger.error(f"Missing required financial data: {str(e)}")
            raise ValueError(f"Incomplete financial data: {str(e)} required")
        except Exception as e:
            logger.error(f"Error calculating cash flows: {str(e)}")
            raise ValueError(f"Cash flow calculation failed: {str(e)}")

    def calculate_profitability_metrics(
        self,
        use_rust: bool = True,
        target_npv: Optional[float] = None
    ) -> Dict[str, Any]:
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

            return {
                "metrics": metrics,
                "cash_flows": cash_flows,
                "initial_investment": initial_investment
            }

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
        steps: int = 10
    ) -> Dict[str, Dict[str, List[float]]]:
        """
        Perform sensitivity analysis on specified variables using Rust implementation.
        
        Args:
            variables: List of variables to analyze (discount_rate, production_volume, operating_costs, revenue)
            ranges: Dictionary of (min, max) tuples for each variable
            steps: Number of steps in sensitivity analysis
            
        Returns:
            Dictionary of sensitivity results for each variable
        """
        self._validate_data()
        cash_flows = self._calculate_cash_flows()
        
        # Variable mapping to Rust implementation indices
        variable_mapping = {
            "discount_rate": 0,
            "production_volume": 1,
            "operating_costs": 2,
            "revenue": 3
        }
        
        results = {}
        
        for var in variables:
            if var not in variable_mapping:
                logger.warning(f"Unsupported sensitivity variable: {var}")
                continue
                
            range_min, range_max = ranges[var]
            var_index = variable_mapping[var]
            
            try:
                # Run Rust sensitivity analysis
                sensitivity_values = self.rust_handler.run_sensitivity_analysis(
                    base_values=cash_flows,
                    variable_index=var_index,
                    range_min=range_min,
                    range_max=range_max,
                    steps=steps
                )
                
                # Calculate range values for x-axis
                range_values = [
                    range_min + i * (range_max - range_min) / steps
                    for i in range(steps + 1)
                ]
                
                # Calculate base value (middle point)
                base_value = range_min + (range_max - range_min) / 2
                
                # Calculate base case NPV for percent changes
                base_npv = sensitivity_values[steps//2]
                
                results[var] = {
                    "values": sensitivity_values,
                    "range": range_values,
                    "base_value": base_value,
                    "base_npv": base_npv,
                    "percent_change": [
                        ((val - base_npv) / abs(base_npv)) * 100 if base_npv != 0 else 0.0
                        for val in sensitivity_values
                    ]
                }
            except Exception as e:
                logger.error(f"Error in Rust sensitivity analysis for {var}: {str(e)}")
                raise ValueError(f"Sensitivity analysis failed for {var}: {str(e)}")
        
        if not results:
            raise ValueError("No valid sensitivity analyses could be performed")
        
        return results
