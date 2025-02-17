from typing import Dict, Any, Optional
from datetime import datetime
import logging

from analytics.economic.profitability_analyzer import ProfitabilityAnalysis, ProjectParameters
from analytics.economic.services.cost_tracking import CostTracker
from backend.fastapi_app.models.economic_analysis import (
    ComprehensiveAnalysisInput, SensitivityAnalysisInput, CapexInput, OpexInput
)
from ..capex_endpoints import calculate_capex
from ..opex_endpoints import calculate_opex

logger = logging.getLogger(__name__)

class ProfitabilityService:
    def __init__(self):
        self._analyzer = ProfitabilityAnalysis()
        self._cost_tracker = CostTracker()

    def _create_project_parameters(self, input_data: ComprehensiveAnalysisInput) -> ProjectParameters:
        """Create project parameters from input data"""
        return ProjectParameters(
            discount_rate=input_data.economic_factors.discount_rate,
            project_duration=input_data.economic_factors.project_duration,
            production_volume=input_data.economic_factors.production_volume,
            uncertainty=input_data.uncertainty,
            monte_carlo_iterations=input_data.monte_carlo_iterations
        )

    async def analyze_comprehensive(
        self, 
        input_data: ComprehensiveAnalysisInput
    ) -> Dict[str, Any]:
        """Perform comprehensive profitability analysis"""
        try:
            # Calculate CAPEX
            capex_input = CapexInput(
                equipment_list=input_data.equipment_list,
                economic_factors=input_data.economic_factors,
                process_type=input_data.process_type
            )
            capex_result = await calculate_capex(capex_input)
            
            # Calculate OPEX using CAPEX results
            opex_input = OpexInput(
                utilities=input_data.utilities,
                raw_materials=input_data.raw_materials,
                labor_config=input_data.labor_config,
                equipment_costs=capex_result["capex_summary"]["equipment_costs"],
                economic_factors=input_data.economic_factors,
                process_type=input_data.process_type
            )
            opex_result = await calculate_opex(opex_input)

            # Set up project parameters
            parameters = self._create_project_parameters(input_data)
            
            # Prepare CAPEX data with total_investment
            capex_data = capex_result["capex_summary"]
            capex_data["total_investment"] = (
                capex_data["total_capex"] +  # Base CAPEX
                capex_data.get("working_capital", 0.0) +  # Working capital if present
                capex_data.get("contingency", 0.0)  # Contingency if present
            )
            
            # Prepare OPEX data with total_annual_cost
            opex_data = opex_result["opex_summary"]
            opex_data["total_annual_cost"] = opex_data["total_opex"]  # Map total_opex to total_annual_cost
            
            # Configure analyzer with calculated data
            logger.debug(f"Setting project data with CAPEX: {capex_data}")
            logger.debug(f"Setting project data with OPEX: {opex_data}")
            logger.debug(f"Setting project data with revenue: {input_data.revenue_data}")
            logger.debug(f"Setting project data with parameters: {parameters}")
            
            self._analyzer.set_project_data(
                capex=capex_data,
                opex=opex_data,
                revenue=input_data.revenue_data,
                parameters=parameters
            )
            
            # Calculate profitability metrics
            metrics = self._analyzer.calculate_profitability_metrics(
                use_rust=input_data.monte_carlo_iterations > 0
            )
            
            logger.debug(f"Raw profitability metrics: {metrics}")
            
            # Extract actual metric values
            profitability_metrics = {}
            
            # NPV calculation
            if "metrics" in metrics and "monte_carlo" in metrics["metrics"]:
                # Extract NPV from Monte Carlo results (mean value)
                profitability_metrics["npv"] = {
                    "value": float(metrics["metrics"]["monte_carlo"]["results"]["mean"]),
                    "unit": "USD"
                }
            elif isinstance(metrics.get("npv"), dict):
                profitability_metrics["npv"] = metrics["npv"]
            else:
                profitability_metrics["npv"] = {
                    "value": float(metrics.get("npv", 0.0)),
                    "unit": "USD"
                }
            
            # ROI calculation
            if "metrics" in metrics and "roi" in metrics["metrics"]:
                # Extract ROI from Rust results (using annualized ROI)
                profitability_metrics["roi"] = {
                    "value": float(metrics["metrics"]["roi"]["annualized_roi"]),
                    "unit": "ratio"
                }
            elif isinstance(metrics.get("roi"), dict):
                profitability_metrics["roi"] = metrics["roi"]
            else:
                profitability_metrics["roi"] = {
                    "value": float(metrics.get("roi", 0.0)),
                    "unit": "ratio"
                }
            
            # Payback calculation
            if isinstance(metrics.get("payback"), dict):
                profitability_metrics["payback"] = metrics["payback"]
            else:
                # Calculate payback period from cash flows
                total_investment = abs(metrics["cash_flows"][0])
                annual_flows = metrics["cash_flows"][1:]
                cumulative_flows = 0
                payback_years = 0
                
                for i, flow in enumerate(annual_flows):
                    cumulative_flows += flow
                    if cumulative_flows >= total_investment:
                        payback_years = i + 1 + (total_investment - (cumulative_flows - flow)) / flow
                        break
                
                profitability_metrics["payback"] = {
                    "value": float(payback_years),
                    "unit": "years"
                }
            
            logger.debug(f"Processed profitability metrics: {profitability_metrics}")
            
            # Calculate cash flows
            cash_flows = self._analyzer._calculate_cash_flows()
            logger.debug(f"Generated cash flows: {cash_flows}")
            
            # Perform Monte Carlo analysis if requested
            monte_carlo_results = None
            if input_data.monte_carlo_iterations > 0:
                monte_carlo_results = {
                    'iterations': input_data.monte_carlo_iterations,
                    'uncertainty': input_data.uncertainty,
                    'results': metrics.get('metrics', {}).get('monte_carlo', {}).get('results', {})
                }
            
            return {
                "investment_analysis": capex_data,
                "operational_costs": opex_data,
                "profitability_metrics": profitability_metrics,
                "breakdowns": {
                    "equipment": capex_result["equipment_breakdown"],
                    "utilities": opex_result.get("utility_costs", {}),
                    "raw_materials": opex_result.get("raw_material_costs", {}),
                    "labor": opex_result.get("labor_costs", {}),
                    "indirect_factors": capex_result.get("indirect_factors", {}).get("factors", [])
                },
                "process_type": input_data.process_type,
                "analysis_parameters": {
                    "monte_carlo_iterations": input_data.monte_carlo_iterations,
                    "uncertainty": input_data.uncertainty,
                    "project_duration": input_data.economic_factors.project_duration,
                    "discount_rate": input_data.economic_factors.discount_rate,
                    "production_volume": input_data.economic_factors.production_volume
                },
                "cash_flows": cash_flows,
                "monte_carlo_analysis": monte_carlo_results
            }

        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            raise

    async def analyze_sensitivity(self, input_data: SensitivityAnalysisInput) -> Dict[str, Any]:
        """Perform sensitivity analysis on economic metrics"""
        sensitivity_results = self._analyzer.perform_sensitivity_analysis(
            variables=input_data.variables,
            ranges=input_data.ranges,
            steps=input_data.steps
        )
        return {
            "sensitivity_analysis": sensitivity_results,
            "base_case": {
                "cash_flows": input_data.base_cash_flows,
                "variables": input_data.variables,
                "ranges": input_data.ranges
            }
        } 