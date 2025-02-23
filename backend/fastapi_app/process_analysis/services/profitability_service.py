from typing import Dict, Any, Optional
from datetime import datetime
import logging

from analytics.economic.profitability_analyzer import ProfitabilityAnalysis, ProjectParameters
from analytics.economic.services.cost_tracking import CostTracker
from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis
from backend.fastapi_app.models.economic_analysis import (
    ComprehensiveAnalysisInput, SensitivityAnalysisInput
)



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
            production_volume=input_data.revenue_data.annual_production,
            uncertainty=input_data.uncertainty,
            monte_carlo_iterations=input_data.monte_carlo_iterations,
            random_seed=input_data.random_seed
        )

    async def analyze_comprehensive(
        self, 
        input_data: ComprehensiveAnalysisInput
    ) -> Dict[str, Any]:
        """Perform comprehensive profitability analysis"""
        try:
            # Calculate CAPEX using analyzer directly
            capex_analyzer = CapitalExpenditureAnalysis()
            
            # Add equipment
            for equipment in input_data.equipment_list:
                capex_analyzer.add_equipment(equipment.model_dump())
            
            # Calculate total equipment cost for default indirect factors if needed
            total_equipment_cost = sum(
                equip.base_cost * (equip.processing_capacity / 1000)
                for equip in input_data.equipment_list
            )
            
            # Add indirect factors
            if input_data.indirect_factors:
                # Use provided indirect factors
                for factor in input_data.indirect_factors:
                    capex_analyzer.add_indirect_factor(factor.model_dump())
                logger.debug(f"Added {len(input_data.indirect_factors)} indirect factors from input")
            else:
                # Use default indirect factors
                default_factors = [
                    {
                        "name": "engineering",
                        "cost": total_equipment_cost,
                        "percentage": 0.15
                    },
                    {
                        "name": "contingency",
                        "cost": total_equipment_cost,
                        "percentage": 0.10
                    },
                    {
                        "name": "construction",
                        "cost": total_equipment_cost,
                        "percentage": 0.20
                    }
                ]
                for factor in default_factors:
                    capex_analyzer.add_indirect_factor(factor)
                logger.debug("Added default indirect factors")
            
            # Calculate CAPEX
            capex_result = capex_analyzer.calculate_total_capex(
                installation_factor=input_data.economic_factors.installation_factor,
                indirect_costs_factor=input_data.economic_factors.indirect_costs_factor
            )
            logger.debug("CAPEX calculation completed")
            
            # Configure analyzer with calculated data
            opex_analyzer = OperationalExpenditureAnalysis()
            
            # Set production volume first
            production_volume = input_data.revenue_data.annual_production
            opex_analyzer.set_production_volume(production_volume)
            
            # Add utilities
            for utility in input_data.utilities:
                opex_analyzer.add_utility(utility.model_dump())
            
            # Add raw materials
            for material in input_data.raw_materials:
                opex_analyzer.add_raw_material(material.model_dump())
            
            # Set labor data
            opex_analyzer.set_labor_data(input_data.labor_config.model_dump())
            
            # Set maintenance factors
            opex_analyzer.set_maintenance_factors({
                "equipment_cost": capex_result["equipment_costs"],
                "maintenance_factor": input_data.economic_factors.maintenance_factor
            })
            
            opex_result = opex_analyzer.calculate_total_opex()
            logger.debug("OPEX calculation completed")

            # Set up project parameters
            parameters = self._create_project_parameters(input_data)
            
            # Calculate working capital based on OPEX
            working_capital = opex_result["total_opex"] * 0.0833  # 1 month
            
            # Calculate contingency on direct costs only
            direct_costs = capex_result["equipment_costs"] + capex_result["installation_costs"]
            contingency = direct_costs * 0.10
            
            # Calculate total investment
            total_investment = (
                capex_result["total_capex"] +  # Base CAPEX (direct + indirect)
                working_capital + 
                contingency  # 10% of direct costs
            )

            # Update CAPEX data with calculated contingency
            capex_data = {
                "total_capex": capex_result["total_capex"],
                "equipment_costs": capex_result["equipment_costs"],
                "installation_costs": capex_result["installation_costs"],
                "indirect_costs": capex_result["indirect_costs"],
                "working_capital": working_capital,
                "contingency": contingency,
                "total_investment": total_investment
            }

            # Prepare OPEX data
            opex_data = {
                "total_opex": opex_result["total_opex"],
                "total_annual_cost": opex_result["total_opex"],  # Required by profitability analyzer
                "raw_material_costs": opex_result["cost_breakdown"]["raw_materials"],
                "utility_costs": opex_result["cost_breakdown"]["utilities"],
                "labor_costs": opex_result["cost_breakdown"]["labor"],
                "maintenance_costs": opex_result["cost_breakdown"]["maintenance"]
            }
            
            # Configure analyzer with calculated data
            self._analyzer.set_project_data(
                capex=capex_data,
                opex=opex_data,
                revenue=input_data.revenue_data.model_dump(),
                parameters=parameters
            )
            
            # Calculate profitability metrics
            profitability_results = self._analyzer.calculate_profitability_metrics(
                use_rust=parameters.monte_carlo_iterations > 0
            )
            
            # Ensure all required metrics are properly formatted
            metrics = profitability_results["metrics"]
            
            # Format NPV
            if "monte_carlo" in metrics and "results" in metrics["monte_carlo"]:
                metrics["npv"] = {
                    "value": float(metrics["monte_carlo"]["results"]["mean"]),
                    "unit": "USD"
                }
            
            # Format ROI
            if "roi" not in metrics:
                metrics["roi"] = {"value": 0.0, "unit": "ratio"}
            
            # Calculate and format payback period
            cash_flows = profitability_results.get("cash_flows", [])
            payback_value = self.calculate_payback_period(cash_flows)
            metrics["payback"] = {"value": payback_value}
            
            # Calculate annual revenue
            revenue_data = input_data.revenue_data.model_dump()
            product_price = float(revenue_data["product_price"])
            annual_production = float(revenue_data["annual_production"])
            yield_efficiency = float(revenue_data.get("yield_efficiency"))
            
            annual_revenue = product_price * annual_production * yield_efficiency
            logger.debug(f"Calculated annual revenue: {annual_revenue} from price={product_price}, production={annual_production}, yield={yield_efficiency}")
            
            # Calculate total annual costs
            total_annual_costs = opex_data["total_annual_cost"]
            logger.debug(f"Total annual costs: {total_annual_costs}")
            
            # Calculate operating income
            operating_income = annual_revenue - total_annual_costs
            logger.debug(f"Operating income: {operating_income}")
            
            # Calculate margins
            variable_costs = opex_data["raw_material_costs"] + opex_data["utility_costs"]
            gross_margin = (annual_revenue - variable_costs) / annual_revenue if annual_revenue > 0 else 0.0
            operating_margin = operating_income / annual_revenue if annual_revenue > 0 else 0.0
            logger.debug(f"Margins calculated - gross: {gross_margin}, operating: {operating_margin}")
            
            # Update metrics with calculated values
            metrics["margins"] = {
                "gross_margin": {"value": gross_margin, "unit": "ratio"},
                "operating_margin": {"value": operating_margin, "unit": "ratio"}
            }
            
            # Update annual metrics
            fixed_costs = opex_data["labor_costs"] + opex_data["maintenance_costs"]
            metrics["annual_metrics"] = {
                "revenue": annual_revenue,
                "operating_costs": opex_data["total_annual_cost"],
                "fixed_costs": fixed_costs,
                "total_costs": total_annual_costs,
                "effective_production": annual_production * yield_efficiency
            }
            logger.debug(f"Annual metrics updated: {metrics['annual_metrics']}")
            
            # Calculate break-even point
            if variable_costs > 0 and annual_production > 0:
                variable_cost_per_unit = variable_costs / annual_production
                contribution_margin = product_price - variable_cost_per_unit
                if contribution_margin > 0:
                    break_even_units = fixed_costs / contribution_margin
                    break_even_revenue = break_even_units * product_price
                else:
                    break_even_units = float('inf')
                    break_even_revenue = float('inf')
            else:
                break_even_units = float('inf')
                break_even_revenue = float('inf')
                variable_cost_per_unit = 0.0
            
            metrics["break_even"] = {
                "units": break_even_units,
                "revenue": break_even_revenue,
                "unit_price": product_price,
                "variable_cost_per_unit": variable_cost_per_unit
            }
            logger.debug(f"Break-even metrics calculated: {metrics['break_even']}")
            
            # Format investment efficiency
            if "investment_efficiency" not in metrics:
                metrics["investment_efficiency"] = {
                    "capex_per_unit": capex_data["total_capex"] / annual_production,
                    "revenue_to_investment_ratio": product_price * annual_production / capex_data["total_investment"],
                    "opex_to_capex_ratio": opex_data["total_opex"] / capex_data["total_capex"]
                }
            
            # Format cost structure
            fixed_costs = opex_data["labor_costs"] + opex_data["maintenance_costs"]
            variable_costs = opex_data["raw_material_costs"] + opex_data["utility_costs"]
            total_costs = fixed_costs + variable_costs
            
            metrics["cost_structure"] = {
                "fixed_costs": {
                    "value": fixed_costs,
                    "percentage": (fixed_costs / total_costs * 100) if total_costs > 0 else 0.0,
                    "breakdown": {
                        "labor": opex_data["labor_costs"],
                        "maintenance": opex_data["maintenance_costs"]
                    }
                },
                "variable_costs": {
                    "value": variable_costs,
                    "percentage": (variable_costs / total_costs * 100) if total_costs > 0 else 0.0,
                    "breakdown": {
                        "raw_materials": opex_data["raw_material_costs"],
                        "utilities": opex_data["utility_costs"]
                    }
                }
            }
            
            # Calculate cash flows for Monte Carlo
            initial_investment = -capex_data["total_investment"]
            annual_cash_flow = annual_revenue - total_annual_costs
            cash_flows = [initial_investment] + [annual_cash_flow] * input_data.economic_factors.project_duration
            
            # Set up project parameters for Monte Carlo
            parameters = ProjectParameters(
                discount_rate=input_data.economic_factors.discount_rate,
                project_duration=input_data.economic_factors.project_duration,
                production_volume=annual_production,
                monte_carlo_iterations=input_data.monte_carlo_iterations or 1000,
                uncertainty=input_data.uncertainty,
                random_seed=input_data.random_seed
            )
            
            # Configure analyzer with calculated data
            self._analyzer.set_project_data(
                capex=capex_data,
                opex=opex_data,
                revenue=revenue_data,
                parameters=parameters
            )
            
            # Calculate profitability metrics with Monte Carlo
            profitability_results = self._analyzer.calculate_profitability_metrics(
                use_rust=True
            )
            
            # Update metrics with Monte Carlo results
            if "monte_carlo" in profitability_results["metrics"]:
                mc_results = profitability_results["metrics"]["monte_carlo"]["results"]
                metrics["npv"] = {
                    "value": float(mc_results["mean"]),
                    "unit": "USD"
                }
                metrics["monte_carlo"] = {
                    "results": {
                        "mean": float(mc_results["mean"]),
                        "std_dev": float(mc_results["std_dev"]),
                        "confidence_interval": mc_results["confidence_interval"]
                    }
                }
            
            # Return the results in the expected format
            return {
                "profitability_metrics": metrics,
                "cash_flows": cash_flows,
                "business_insights": {
                    "profitability_indicators": metrics.get("margins", {}),
                    "break_even_analysis": metrics.get("break_even", {}),
                    "cost_efficiency": metrics.get("investment_efficiency", {}),
                    "risk_metrics": {
                        "payback_period": metrics.get("payback", {}).get("value", 0.0),
                        "mcsp_confidence": metrics.get("mcsp", {}).get("confidence_interval", {"lower": 0.0, "upper": 0.0}),
                        "npv_risk": metrics.get("monte_carlo", {}).get("results", {}).get("std_dev")
                    }
                },
                "financial_model": {
                    "total_capex": capex_data["total_capex"],
                    "working_capital": working_capital,
                    "annual_revenue": annual_revenue,
                    "annual_operating_costs": opex_data["total_annual_cost"],
                    "total_annual_costs": total_annual_costs,
                    "annual_net_cash_flows": cash_flows[1:]
                }
            }

        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {str(e)}")
            raise

    async def analyze_sensitivity(self, input_data: SensitivityAnalysisInput) -> Dict[str, Any]:
        """Perform sensitivity analysis on economic metrics"""
        try:
            # Get cost ratios from the input
            fixed_cost_ratio = input_data.fixed_cost_ratio
            variable_cost_ratio = input_data.variable_cost_ratio
            
            sensitivity_results = self._analyzer.perform_sensitivity_analysis(
                variables=input_data.variables,
                ranges=input_data.ranges,
                steps=input_data.steps,
                fixed_cost_ratio=fixed_cost_ratio,
                variable_cost_ratio=variable_cost_ratio
            )
            
            return {
                "sensitivity_analysis": sensitivity_results,
                "base_case": {
                    "cash_flows": input_data.base_cash_flows,
                    "variables": input_data.variables,
                    "ranges": input_data.ranges,
                    "cost_structure": {
                        "fixed_cost_ratio": fixed_cost_ratio,
                        "variable_cost_ratio": variable_cost_ratio
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error in sensitivity analysis: {str(e)}")
            raise

    async def get_latest_analysis(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest analysis results for a process"""
        try:
            # Get all cost entries for this process from the cost tracker
            process_entries = [
                entry for entry in self._cost_tracker.cost_history
                if entry.get("process_id") == process_id
            ]
            
            if not process_entries:
                return None
                
            # Sort by timestamp and get the latest entry
            latest_entry = sorted(
                process_entries,
                key=lambda x: datetime.fromisoformat(x["timestamp"]),
                reverse=True
            )[0]
            
            return latest_entry
            
        except Exception as e:
            logger.error(f"Error getting latest analysis for process {process_id}: {str(e)}")
            raise 

    def calculate_payback_period(self, cash_flows):
        """Calculate discounted payback period with enhanced validation"""
        if not cash_flows or len(cash_flows) < 2:
            return 0.0
        
        # Use total investment as initial outflow
        initial_investment = self._analyzer.capex_data["total_investment"]
        cumulative = 0.0
        discount_rate = self._analyzer.parameters.discount_rate if self._analyzer.parameters else 0.1

        for year, cash in enumerate(cash_flows[1:], start=1):
            # Discount the cash flow
            discounted_cash = cash / ((1 + discount_rate) ** year)
            cumulative += discounted_cash
            
            if cumulative >= initial_investment:
                # Calculate exact payback point within the year
                remaining = initial_investment - (cumulative - discounted_cash)
                fractional_year = remaining / discounted_cash
                return year - 1 + fractional_year
        
        return float('inf')  # Never recovers investment

    def _calculate_metrics_rust(self, cash_flows, initial_investment):
        metrics = {}  # Initialize metrics dictionary
        
        monte_carlo_results = self.rust_handler.run_monte_carlo_simulation(
            cash_flows=cash_flows,
            discount_rate=self.parameters.discount_rate,
            initial_investment=initial_investment,
            iterations=self.parameters.monte_carlo_iterations,
            price_uncertainty=self.parameters.uncertainty.price,
            cost_uncertainty=self.parameters.uncertainty.cost,
            production_uncertainty=self.parameters.uncertainty.production
        )
        
        # Now you can safely add to it
        metrics["monte_carlo"] = {
            "mean": monte_carlo_results["results"]["mean"],
            "std_dev": monte_carlo_results["results"]["std_dev"],
            "confidence_interval": monte_carlo_results["results"]["confidence_interval"]
        }
        
        return metrics 