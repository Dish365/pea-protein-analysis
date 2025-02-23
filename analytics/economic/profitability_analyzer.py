from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.payback import calculate_payback_period
from analytics.economic.profitability.mcsp import calculate_mcsp
from backend.fastapi_app.process_analysis.services.rust_handler import RustHandler
import logging
import numpy as np

# Configure module logger with full package path
logger = logging.getLogger('analytics.economic.profitability_analyzer')

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

    def _calculate_effective_production(self) -> float:
        """Calculate effective production volume considering protein content and yield"""
        if not isinstance(self.revenue_data, dict):
            raise ValueError("Invalid revenue data format")

        # Get raw material data for protein content
        raw_materials = self.opex_data.get("raw_materials_breakdown", [])
        pea_flour = next((rm for rm in raw_materials if rm["name"].lower() == "pea flour"), None)
        
        if pea_flour and "protein_content" in pea_flour and "quantity" in pea_flour:
            # Calculate based on protein content and yield
            raw_protein = pea_flour["quantity"] * pea_flour["protein_content"]
            yield_efficiency = self.revenue_data.get("yield_efficiency", 0.78)  # Default 78% yield
            return raw_protein * yield_efficiency
        elif "annual_production" in self.revenue_data:
            # Fallback to specified production with yield adjustment
            yield_efficiency = self.revenue_data.get("yield_efficiency", 0.78)  # Default 78% yield
            return self.revenue_data["annual_production"] * yield_efficiency
        else:
            raise ValueError("Cannot calculate effective production: missing required data")

    def _calculate_cash_flows(self, apply_uncertainties: bool = True) -> List[float]:
        """Centralized cash flow calculation with enhanced validation"""
        self._validate_data()
        
        try:
            # Calculate initial investment (negative cash flow)
            initial_investment = -self.capex_data["total_investment"]
            
            # Calculate annual operating costs
            annual_opex = self.opex_data["total_annual_cost"]
            
            # Calculate annual revenue using effective production
            if "product_price" not in self.revenue_data:
                raise ValueError("Revenue data must contain product_price")
                
            effective_production = self._calculate_effective_production()
            base_revenue = self.revenue_data["product_price"] * effective_production
            
            if apply_uncertainties:
                # Get uncertainty values from the UncertaintyConfig model
                if hasattr(self.parameters, 'uncertainty') and self.parameters.uncertainty:
                    price_uncertainty = self.parameters.uncertainty.price
                    cost_uncertainty = self.parameters.uncertainty.cost
                    production_uncertainty = self.parameters.uncertainty.production
                else:
                    # Use default values if uncertainty config is not provided
                    price_uncertainty = 0.15  # 15% default price uncertainty
                    cost_uncertainty = 0.12  # 12% default cost uncertainty
                    production_uncertainty = 0.10  # 10% default production uncertainty

                # Apply correlated uncertainties
                price_factor = 1 + self.rng.normal(0, price_uncertainty/3)
                cost_factor = 1 + self.rng.normal(0, cost_uncertainty/3)
                production_factor = 1 + self.rng.normal(0, production_uncertainty/3)
                
                # Calculate annual cash flows with uncertainties
                annual_cash_flow = (
                    base_revenue * price_factor * production_factor -
                    annual_opex * cost_factor
                )
            else:
                # Use deterministic values for sensitivity analysis
                annual_cash_flow = base_revenue - annual_opex
            
            # Generate cash flow series
            cash_flows = [initial_investment]  # Year 0
            cash_flows.extend([annual_cash_flow] * self.parameters.project_duration)  # Years 1-N
            
            return cash_flows
            
        except Exception as e:
            logger.error(f"Error in cash flow calculation: {str(e)}")
            raise

    def calculate_profitability_metrics(
        self,
        use_rust: bool = True
    ) -> Dict[str, Any]:
        """Calculate all profitability metrics"""
        self._validate_data()
        
        try:
            # Set random seed if provided
            if self.parameters.random_seed is not None:
                self.rng = np.random.RandomState(self.parameters.random_seed)
                logger.debug(f"Set random seed to {self.parameters.random_seed}")

            # Calculate cash flows with uncertainties
            cash_flows = self._calculate_cash_flows()
            initial_investment = -cash_flows[0]  # First cash flow is negative investment

            try:
                if use_rust and self.parameters.monte_carlo_iterations > 0:
                    # Use Rust implementation for Monte Carlo
                    metrics = self._calculate_metrics_rust(
                        cash_flows=cash_flows,
                        initial_investment=initial_investment
                    )
                else:
                    # Use Python implementation
                    metrics = self._calculate_metrics_python(
                        cash_flows=cash_flows,
                        initial_investment=initial_investment
                    )
            except Exception as calc_error:
                logger.error(f"Error in metrics calculation: {str(calc_error)}")
                # Fallback to Python implementation
                metrics = self._calculate_metrics_python(
                    cash_flows=cash_flows,
                    initial_investment=initial_investment
                )

            # Ensure metrics has the correct structure
            if not isinstance(metrics, dict):
                metrics = {}
            
            # Ensure NPV exists and is properly formatted
            if 'npv' not in metrics or not isinstance(metrics['npv'], dict):
                # Calculate basic NPV if not present
                npv_result = calculate_npv(
                    cash_flows=cash_flows,
                    discount_rate=self.parameters.discount_rate,
                    initial_investment=initial_investment
                )
                metrics['npv'] = {
                    'value': float(npv_result['npv']),
                    'unit': 'USD'
                }

            # Format the final metrics structure
            formatted_metrics = {
                "npv": metrics.get('npv', {'value': 0.0, 'unit': 'USD'}),
                "roi": metrics.get('roi', {'value': 0.0, 'unit': 'ratio'}),
                "monte_carlo": metrics.get('monte_carlo', {
                    "results": {
                        "mean": metrics.get('npv', {}).get('value', 0.0),
                        "std_dev": 0.0,
                        "confidence_interval": [0.0, 0.0]
                    }
                })
            }

            return {
                "metrics": formatted_metrics,
                "cash_flows": cash_flows
            }

        except Exception as e:
            logger.error(f"Error calculating profitability metrics: {str(e)}")
            # Return minimal valid result structure
            return {
                "metrics": {
                    "npv": {'value': 0.0, 'unit': 'USD'},
                    "roi": {'value': 0.0, 'unit': 'ratio'},
                    "monte_carlo": {
                        "results": {
                            "mean": 0.0,
                            "std_dev": 0.0,
                            "confidence_interval": [0.0, 0.0]
                        }
                    }
                },
                "cash_flows": cash_flows if 'cash_flows' in locals() else [0.0]
            }

    def _calculate_metrics_rust(
        self,
        cash_flows: List[float],
        initial_investment: float
    ) -> Dict[str, Union[float, Dict]]:
        """Calculate metrics using Rust implementation"""
        try:
            logger.debug(f"Starting Monte Carlo simulation with seed {self.parameters.random_seed}")
            logger.debug(f"Cash flows: {cash_flows}")
            logger.debug(f"Parameters: {self.parameters}")
            
            # Run Monte Carlo simulation with seed
            monte_carlo_results = self.rust_handler.run_monte_carlo_simulation(
                cash_flows=cash_flows,
                discount_rate=self.parameters.discount_rate,
                initial_investment=initial_investment,
                iterations=self.parameters.monte_carlo_iterations,
                price_uncertainty=self.parameters.uncertainty.price,
                cost_uncertainty=self.parameters.uncertainty.cost,
                production_uncertainty=self.parameters.uncertainty.production,
                random_seed=self.parameters.random_seed if self.parameters.random_seed is not None else 42
            )
            logger.debug(f"Monte Carlo results: {monte_carlo_results}")

            # Calculate discounted cash flows for ROI
            discounted_flows = []
            for t, cf in enumerate(cash_flows[1:], 1):  # Start from year 1
                discounted_cf = cf / ((1 + self.parameters.discount_rate) ** t)
                discounted_flows.append(discounted_cf)
            
            # Calculate ROI using discounted values
            total_discounted_gain = sum(discounted_flows)
            roi_results = calculate_roi(
                gain_from_investment=total_discounted_gain,
                cost_of_investment=initial_investment,
                time_period=self.parameters.project_duration
            )

            # Format ROI
            formatted_roi = {
                'value': float(roi_results['roi']),
                'unit': 'ratio'
            }

            # Format NPV from Monte Carlo results
            formatted_npv = {
                'value': float(monte_carlo_results["results"]["mean"]),
                'unit': 'USD'
            }
            logger.debug(f"Formatted NPV: {formatted_npv}")

            return {
                "npv": formatted_npv,
                "roi": formatted_roi,
                "monte_carlo": monte_carlo_results
            }
        except Exception as e:
            logger.error(f"Error in Monte Carlo simulation: {str(e)}")
            # Fallback to Python implementation if Monte Carlo fails
            return self._calculate_metrics_python(cash_flows, initial_investment)

    def _calculate_metrics_python(
        self,
        cash_flows: List[float],
        initial_investment: float
    ) -> Dict[str, Union[float, Dict]]:
        """Calculate metrics using Python implementation"""
        try:
            npv_results = calculate_npv(
                cash_flows=cash_flows,
                discount_rate=self.parameters.discount_rate,
                initial_investment=initial_investment
            )

            # Ensure NPV is properly formatted
            formatted_npv = {
                'value': float(npv_results['npv']),
                'unit': 'USD'
            }

            # Calculate discounted cash flows for ROI
            discounted_flows = []
            for t, cf in enumerate(cash_flows[1:], 1):  # Start from year 1
                discounted_cf = cf / ((1 + self.parameters.discount_rate) ** t)
                discounted_flows.append(discounted_cf)

            # Calculate ROI using discounted values
            total_discounted_gain = sum(discounted_flows)
            roi_results = calculate_roi(
                gain_from_investment=total_discounted_gain,
                cost_of_investment=initial_investment,
                time_period=self.parameters.project_duration
            )

            # Format ROI using simple ROI instead of annualized
            formatted_roi = {
                'value': float(roi_results['roi']) if isinstance(roi_results, dict) else float(roi_results),
                'unit': 'ratio'
            }

            payback_results = calculate_payback_period(
                initial_investment=initial_investment,
                cash_flows=cash_flows[1:],  # Exclude initial investment
                discount_rate=self.parameters.discount_rate
            )

            return {
                "npv": formatted_npv,
                "roi": formatted_roi,
                "payback": payback_results
            }
        except Exception as e:
            logger.error(f"Error in Python metrics calculation: {str(e)}")
            # Return minimal valid result structure
            return {
                "npv": {'value': 0.0, 'unit': 'USD'},
                "roi": {'value': 0.0, 'unit': 'ratio'},
                "payback": {'value': float('inf')}
            }

    def perform_sensitivity_analysis(
        self,
        variables: List[str],
        ranges: Dict[str, tuple],
        steps: int = 10,
        fixed_cost_ratio: float = None,
        variable_cost_ratio: float = None
    ) -> Dict[str, Dict[str, List[float]]]:
        """
        Perform sensitivity analysis on specified variables using Rust implementation.
        """
        self._validate_data()
        logger.info("=== Starting Sensitivity Analysis in Profitability Analyzer ===")
        logger.info(f"Variables to analyze: {variables}")
        logger.info(f"Variable ranges: {ranges}")
        logger.info(f"Number of steps: {steps}")
        
        # Calculate deterministic cash flows for sensitivity analysis
        cash_flows = self._calculate_cash_flows(apply_uncertainties=False)
        logger.info(f"Base cash flows (first 5): {cash_flows[:5]}...")
        
        # Variable mapping to Rust implementation indices
        variable_mapping = {
            "discount_rate": 0,
            "production_volume": 1,
            "operating_costs": 2,
            "revenue": 3
        }
        logger.info(f"Variable mapping configuration: {variable_mapping}")

        logger.info(f"Cost ratios - Fixed: {fixed_cost_ratio:.4f}, Variable: {variable_cost_ratio:.4f}")
        
        results = {}
        
        for var in variables:
            logger.info(f"\n=== Processing Variable: {var} ===")
            if var not in variable_mapping:
                logger.warning(f"Skipping unsupported variable: {var}")
                continue
                
            range_min, range_max = ranges[var]
            var_index = variable_mapping[var]
            logger.info(f"Variable index: {var_index}, Range: ({range_min}, {range_max})")
            
            try:
                logger.info(f"Calling Rust sensitivity analysis for {var}")
                sensitivity_values = self.rust_handler.run_sensitivity_analysis(
                    base_values=cash_flows,
                    variable_index=var_index,
                    range_min=range_min,
                    range_max=range_max,
                    steps=steps,
                    discount_rate=self.parameters.discount_rate,
                    fixed_cost_ratio=fixed_cost_ratio,
                    variable_cost_ratio=variable_cost_ratio
                )
                logger.info(f"Received {len(sensitivity_values)} sensitivity values")
                logger.info(f"First few values: {sensitivity_values[:3]}...")
                
                # Calculate range values for x-axis
                range_values = [
                    range_min + i * (range_max - range_min) / steps
                    for i in range(steps + 1)
                ]
                
                # Calculate base value (middle point)
                base_value = range_min + (range_max - range_min) / 2
                
                # Calculate base case NPV for percent changes
                base_npv = sensitivity_values[steps//2]
                logger.info(f"Base NPV for {var}: {base_npv}")
                
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
                logger.info(f"Completed analysis for {var}")
                logger.info(f"Range values: {range_values[:3]}... to {range_values[-3:]}")
                logger.info(f"Percent changes: {results[var]['percent_change'][:3]}... to {results[var]['percent_change'][-3:]}")
            except Exception as e:
                logger.error(f"Error in sensitivity analysis for {var}: {str(e)}", exc_info=True)
                raise ValueError(f"Sensitivity analysis failed for {var}: {str(e)}")
        
        if not results:
            logger.error("No sensitivity results were generated")
            raise ValueError("No valid sensitivity analyses could be performed")
        
        logger.info("=== Sensitivity Analysis Complete ===")
        logger.info(f"Successfully analyzed variables: {list(results.keys())}")
        return results
