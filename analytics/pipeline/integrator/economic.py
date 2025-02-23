from typing import Dict, List, Any, Optional
import httpx
from datetime import datetime
import logging
import json
from dataclasses import dataclass

from analytics.economic.profitability.npv import calculate_npv
from analytics.economic.profitability.roi import calculate_roi
from analytics.economic.profitability.mcsp import calculate_mcsp
from analytics.economic.services.metrics import get_economic_metrics
from backend.django_app.process_data.services.fastapi_service import FastAPIService

logger = logging.getLogger(__name__)

@dataclass
class EconomicMetrics:
    """Container for economic metrics with enhanced business insights"""
    npv: float
    roi: float
    mcsp: float
    payback_period: float
    gross_margin: float
    operating_margin: float
    break_even_units: float
    break_even_revenue: float
    cost_structure: Dict[str, Any]
    investment_efficiency: Dict[str, Any]

class EconomicIntegrator:
    """Integrates economic analysis components through FastAPI endpoints"""
    
    def __init__(self):
        self.fastapi_service = FastAPIService()
        self.metrics_history = []
        self.logger = logging.getLogger(__name__)

    async def analyze_economics(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze economics by utilizing the FastAPI service
        """
        try:
            # Call FastAPI service for comprehensive analysis
            analysis_result = await self.fastapi_service.analyze_process(process_data)
            
            # Store metrics history for trend analysis
            if analysis_result.get("profitability_metrics"):
                self.metrics_history.append({
                    "timestamp": datetime.now(),
                    "metrics": analysis_result["profitability_metrics"]
                })
            
            return analysis_result
        except Exception as e:
            self.logger.error(f"Error in economic analysis: {str(e)}")
            raise

    async def get_business_metrics(self, process_id: int, metrics_filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get filtered business metrics from FastAPI service
        """
        try:
            return await self.fastapi_service.get_business_metrics(process_id, metrics_filter)
        except Exception as e:
            self.logger.error(f"Error fetching business metrics: {str(e)}")
            raise

    async def get_performance_indicators(self, process_id: int, time_range: str = "1M") -> Dict[str, Any]:
        """
        Get performance indicators from FastAPI service
        """
        try:
            return await self.fastapi_service.get_performance_indicators(process_id, time_range)
        except Exception as e:
            self.logger.error(f"Error fetching performance indicators: {str(e)}")
            raise

    async def get_cost_summary(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get cost summary with business metrics trends from FastAPI service
        """
        try:
            return await self.fastapi_service.get_cost_summary(start_date, end_date)
        except Exception as e:
            self.logger.error(f"Error fetching cost summary: {str(e)}")
            raise

    async def calculate_capex(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate capital expenditure using FastAPI endpoint.
        
        Args:
            process_data: Dictionary containing:
                - equipment: List of equipment data matching Equipment model
                - economic_factors: Dictionary matching EconomicFactors model
                - indirect_factors: Optional list matching IndirectFactor model
                - process_type: ProcessType enum value
            
        Returns:
            Dictionary containing:
                - capex_summary: Dict with total_capex, equipment_costs, installation_costs, indirect_costs
                - equipment_breakdown: List of equipment details
                - process_type: ProcessType value
                - indirect_factors: Dict with source and factors list
                
        Raises:
            RuntimeError: If required data is missing or API call fails
        """
        try:
            logger.debug("Starting CAPEX calculation")
            # Validate required fields
            if 'equipment' not in process_data:
                logger.error("Missing required field: equipment")
                raise RuntimeError("Missing required field: equipment")
            if 'economic_factors' not in process_data:
                logger.error("Missing required field: economic_factors")
                raise RuntimeError("Missing required field: economic_factors")
            if 'process_type' not in process_data:
                logger.error("Missing required field: process_type")
                raise RuntimeError("Missing required field: process_type")

            # Validate equipment processing capacity
            for eq in process_data['equipment']:
                if eq.get('processing_capacity', 0) <= 0:
                    raise ValueError(f"Invalid processing capacity for {eq.get('name')}")

            # Format equipment list according to Equipment model
            logger.debug("Formatting equipment list")
            equipment_list = []
            for equip in process_data['equipment']:
                # Validate required equipment fields
                required_fields = ['name', 'base_cost', 'efficiency_factor', 'installation_complexity',
                                 'maintenance_cost', 'energy_consumption', 'processing_capacity']
                missing_fields = [field for field in required_fields if field not in equip]
                if missing_fields:
                    logger.error("Missing required equipment fields: %s", missing_fields)
                    raise RuntimeError(f"Missing required equipment fields: {missing_fields}")

                equipment_list.append({
                    "name": str(equip['name']),
                    "base_cost": float(equip['base_cost']),
                    "efficiency_factor": float(equip['efficiency_factor']),
                    "installation_complexity": float(equip['installation_complexity']),
                    "maintenance_cost": float(equip['maintenance_cost']),
                    "energy_consumption": float(equip['energy_consumption']),
                    "processing_capacity": float(equip['processing_capacity'])
                })

            # Validate and format economic factors
            logger.debug("Formatting economic factors")
            economic_factors_data = process_data['economic_factors']
            required_econ_fields = ['installation_factor', 'indirect_costs_factor', 'maintenance_factor',
                                  'project_duration', 'discount_rate', 'production_volume']
            missing_econ_fields = [field for field in required_econ_fields if field not in economic_factors_data]
            if missing_econ_fields:
                logger.error("Missing required economic factor fields: %s", missing_econ_fields)
                raise RuntimeError(f"Missing required economic factor fields: {missing_econ_fields}")

            economic_factors = {
                "installation_factor": float(economic_factors_data['installation_factor']),
                "indirect_costs_factor": float(economic_factors_data['indirect_costs_factor']),
                "maintenance_factor": float(economic_factors_data['maintenance_factor']),
                "project_duration": int(economic_factors_data['project_duration']),
                "discount_rate": float(economic_factors_data['discount_rate']),
                "production_volume": float(economic_factors_data['production_volume'])
            }

            # Format indirect factors if provided
            logger.debug("Formatting indirect factors")
            indirect_factors = []
            if 'indirect_costs' in process_data:
                indirect_factors = [
                    {
                        'name': factor['name'],
                        'cost': float(factor['cost']),
                        'percentage': float(factor['percentage'])
                    }
                    for factor in process_data['indirect_costs']
                ]

            # Prepare CapexInput payload
            payload = {
                "equipment_list": equipment_list,
                "economic_factors": economic_factors,
                "indirect_factors": indirect_factors,
                "process_type": process_data['process_type']
            }

            # Make API call
            logger.debug("Making CAPEX API call")
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/capex/calculate",
                json=payload
            )

            if response.status_code != 200:
                error_detail = response.json().get("detail", response.text)
                logger.error("CAPEX API call failed: %s", error_detail)
                raise RuntimeError(f"CAPEX calculation failed: {error_detail}")

            result = response.json()
            logger.debug("CAPEX API call successful")

            # Validate response structure
            required_sections = ['capex_summary', 'equipment_breakdown', 'process_type', 'indirect_factors']
            missing_sections = [section for section in required_sections if section not in result]
            if missing_sections:
                logger.error("Invalid CAPEX response: missing sections: %s", missing_sections)
                raise RuntimeError(f"Invalid CAPEX response: missing sections: {missing_sections}")

            # Validate capex_summary structure
            capex_summary = result['capex_summary']
            required_fields = ['total_capex', 'equipment_costs', 'installation_costs', 'indirect_costs']
            missing_fields = [field for field in required_fields if field not in capex_summary]
            if missing_fields:
                logger.error("Invalid CAPEX response: missing fields in capex_summary: %s", missing_fields)
                raise RuntimeError(f"Invalid CAPEX response: missing fields in capex_summary: {missing_fields}")

            # Validate numeric fields
            for field in required_fields:
                if not isinstance(capex_summary[field], (int, float)):
                    logger.error("Invalid CAPEX response: %s must be numeric", field)
                    raise RuntimeError(f"Invalid CAPEX response: {field} must be numeric")

            logger.info("CAPEX calculation successful: %s", capex_summary)
            return result

        except Exception as e:
            logger.error("CAPEX calculation failed: %s", str(e), exc_info=True)
            raise RuntimeError(f"CAPEX calculation failed: {str(e)}")

    async def calculate_opex(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate operational expenditure using FastAPI endpoint.
        
        Args:
            process_data: Dictionary containing:
                - utilities: List of utility data matching Utility model
                - raw_materials: List of raw material data matching RawMaterial model
                - labor_config: Dictionary matching LaborConfig model
                - equipment_costs: Float value for equipment costs
                - economic_factors: Dictionary matching EconomicFactors model
                - process_type: ProcessType enum value
            
        Returns:
            Dictionary containing:
                - opex_summary: Dict with total_opex and cost breakdowns
                - breakdowns: Dict with detailed cost breakdowns
                - process_type: ProcessType value
                - production_volume: Float production volume
                
        Raises:
            RuntimeError: If required data is missing or API call fails
        """
        try:
            logger.debug("Starting OPEX calculation")
            # Validate required fields
            required_fields = ['utilities', 'raw_materials', 'labor_config', 
                             'equipment_costs', 'economic_factors', 'process_type']
            missing_fields = [field for field in required_fields if field not in process_data]
            if missing_fields:
                logger.error("Missing required fields: %s", missing_fields)
                raise RuntimeError(f"Missing required fields: {missing_fields}")

            # Format utilities according to Utility model
            logger.debug("Formatting utilities data")
            utilities = []
            for utility in process_data['utilities']:
                required_utility_fields = ['name', 'consumption', 'unit_price', 'unit']
                missing_fields = [field for field in required_utility_fields if field not in utility]
                if missing_fields:
                    logger.error("Missing required utility fields: %s", missing_fields)
                    raise RuntimeError(f"Missing required utility fields: {missing_fields}")

                utilities.append({
                    'name': str(utility['name']),
                    'consumption': float(utility['consumption']),
                    'unit_price': float(utility['unit_price']),
                    'unit': str(utility['unit'])
                })

            # Format raw materials according to RawMaterial model
            logger.debug("Formatting raw materials data")
            raw_materials = []
            for material in process_data['raw_materials']:
                required_material_fields = ['name', 'quantity', 'unit_price', 'unit']
                missing_fields = [field for field in required_material_fields if field not in material]
                if missing_fields:
                    logger.error("Missing required raw material fields: %s", missing_fields)
                    raise RuntimeError(f"Missing required raw material fields: {missing_fields}")

                raw_materials.append({
                    'name': str(material['name']),
                    'quantity': float(material['quantity']),
                    'unit_price': float(material['unit_price']),
                    'unit': str(material['unit'])
                })

            # Validate and format labor configuration
            logger.debug("Formatting labor configuration")
            labor_config_data = process_data['labor_config']
            required_labor_fields = ['hourly_wage', 'hours_per_week', 'weeks_per_year', 'num_workers']
            missing_fields = [field for field in required_labor_fields if field not in labor_config_data]
            if missing_fields:
                logger.error("Missing required labor configuration fields: %s", missing_fields)
                raise RuntimeError(f"Missing required labor configuration fields: {missing_fields}")

            labor_config = {
                'hourly_wage': float(labor_config_data['hourly_wage']),
                'hours_per_week': float(labor_config_data['hours_per_week']),
                'weeks_per_year': float(labor_config_data['weeks_per_year']),
                'num_workers': int(labor_config_data['num_workers'])
            }

            # Validate equipment costs
            if not isinstance(process_data['equipment_costs'], (int, float)):
                logger.error("Equipment costs must be numeric")
                raise RuntimeError("Equipment costs must be numeric")
            equipment_costs = float(process_data['equipment_costs'])

            # Validate and format economic factors
            logger.debug("Formatting economic factors")
            economic_factors_data = process_data['economic_factors']
            required_econ_fields = ['maintenance_factor', 'project_duration', 
                                  'discount_rate', 'production_volume']
            missing_fields = [field for field in required_econ_fields if field not in economic_factors_data]
            if missing_fields:
                logger.error("Missing required economic factor fields: %s", missing_fields)
                raise RuntimeError(f"Missing required economic factor fields: {missing_fields}")

            economic_factors = {
                'maintenance_factor': float(economic_factors_data['maintenance_factor']),
                'project_duration': int(economic_factors_data['project_duration']),
                'discount_rate': float(economic_factors_data['discount_rate']),
                'production_volume': float(economic_factors_data['production_volume']),
                # Include required but unused fields for model compatibility
                'installation_factor': float(economic_factors_data.get('installation_factor', 0.2)),
                'indirect_costs_factor': float(economic_factors_data.get('indirect_costs_factor', 0.15))
            }

            # Prepare OpexInput payload
            payload = {
                'utilities': utilities,
                'raw_materials': raw_materials,
                'labor_config': labor_config,
                'equipment_costs': equipment_costs,
                'economic_factors': economic_factors,
                'process_type': process_data['process_type']
            }

            # Make API call
            logger.debug("Making OPEX API call")
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/opex/calculate",
                json=payload
            )

            if response.status_code != 200:
                error_detail = response.json().get('detail', response.text)
                logger.error("OPEX API call failed: %s", error_detail)
                raise RuntimeError(f"OPEX calculation failed: {error_detail}")

            result = response.json()
            logger.debug("OPEX API call successful")

            # Validate response structure
            required_sections = ['opex_summary', 'breakdowns', 'process_type', 'production_volume']
            missing_sections = [section for section in required_sections if section not in result]
            if missing_sections:
                logger.error("Invalid OPEX response: missing sections: %s", missing_sections)
                raise RuntimeError(f"Invalid OPEX response: missing sections: {missing_sections}")

            # Validate opex_summary structure
            opex_summary = result['opex_summary']
            required_summary_fields = ['total_opex', 'raw_material_costs', 'utility_costs', 
                                     'labor_costs', 'maintenance_costs']
            missing_fields = [field for field in required_summary_fields if field not in opex_summary]
            if missing_fields:
                logger.error("Invalid OPEX response: missing fields in opex_summary: %s", missing_fields)
                raise RuntimeError(f"Invalid OPEX response: missing fields in opex_summary: {missing_fields}")

            # Validate numeric fields in summary
            for field in required_summary_fields:
                if not isinstance(opex_summary[field], (int, float)):
                    logger.error("Invalid OPEX response: %s must be numeric", field)
                    raise RuntimeError(f"Invalid OPEX response: {field} must be numeric")

            # Validate breakdowns structure
            breakdowns = result['breakdowns']
            required_breakdown_sections = ['raw_materials', 'utilities', 'labor']
            missing_sections = [section for section in required_breakdown_sections if section not in breakdowns]
            if missing_sections:
                logger.error("Invalid OPEX response: missing sections in breakdowns: %s", missing_sections)
                raise RuntimeError(f"Invalid OPEX response: missing sections in breakdowns: {missing_sections}")

            logger.info("OPEX calculation successful: %s", opex_summary)
            return result

        except Exception as e:
            logger.error("OPEX calculation failed: %s", str(e), exc_info=True)
            raise RuntimeError(f"OPEX calculation failed: {str(e)}")

    async def analyze_profitability(
        self,
        capex: float,
        opex: float,
        process_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze profitability using FastAPI endpoint.
        
        Args:
            capex: Total capital expenditure value
            opex: Total operational expenditure value
            process_data: Dictionary containing process configuration
            
        Returns:
            Dictionary containing profitability analysis results
        """
        try:
            logger.debug("Starting profitability analysis")
            logger.debug("Input parameters - CAPEX: $%.2f, OPEX: $%.2f", capex, opex)
            
            # Get calculated costs if available
            calculated_costs = process_data.get('calculated_costs', {})
            
            # Format request payload to match ComprehensiveAnalysisInput model
            logger.debug("Formatting profitability analysis payload")
            payload = {
                "equipment_list": [
                    {
                        **equipment,
                        'cost': calculated_costs.get('equipment_costs', equipment.get('base_cost', 0.0)) / len(process_data.get('equipment', []))
                    }
                    for equipment in process_data.get('equipment', [])
                ],
                "utilities": process_data.get('utilities', []),
                "raw_materials": process_data.get('raw_materials', []),
                "labor_config": process_data.get('labor_config', {}),
                "revenue_data": process_data.get('revenue_data', {}),
                "economic_factors": process_data.get('economic_factors', {}),
                "process_type": process_data.get('process_type', 'baseline'),
                "monte_carlo_iterations": process_data.get('monte_carlo_iterations', 1000),
                "uncertainty": process_data.get('uncertainty', 0.1)
            }

            # Make API call
            logger.debug("Making profitability analysis API call")
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability/analyze",
                json=payload
            )

            if response.status_code != 200:
                error_detail = response.json().get('detail', response.text)
                logger.error("Profitability analysis API call failed: %s", error_detail)
                raise RuntimeError(f"Profitability analysis failed: {error_detail}")

            result = response.json()
            logger.debug("Profitability analysis API call successful")
            
            # Extract and format metrics
            metrics = result.get('profitability_metrics', {})
            cash_flows = result.get('cash_flows', [])
            monte_carlo = result.get('monte_carlo_analysis')
            
            logger.info("Profitability analysis metrics:")
            if 'npv' in metrics:
                logger.info("- NPV: $%.2f", metrics['npv']['value'])
            if 'roi' in metrics:
                logger.info("- Annualized ROI: %.2f (%.1f%%)", metrics['roi']['value'], metrics['roi']['value'] * 100)
            if 'payback' in metrics:
                logger.info("- Payback Period: %.2f years", metrics['payback']['value'])
            
            if monte_carlo:
                logger.debug("Monte Carlo analysis completed with %d iterations", monte_carlo.get('iterations', 0))
            
            return {
                "metrics": metrics,
                "cash_flows": cash_flows,
                "monte_carlo": monte_carlo,
                "process_type": result.get('process_type')
            }

        except Exception as e:
            logger.error("Profitability analysis failed: %s", str(e), exc_info=True)
            raise RuntimeError(f"Profitability analysis failed: {str(e)}")

    async def analyze_sensitivity(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform sensitivity analysis using FastAPI endpoint.
        
        Args:
            process_data: Dictionary containing:
                - base_cash_flows: List of cash flows (required)
                - variables: Optional list of variables to analyze
                - ranges: Optional dict of variable ranges
                - steps: Optional number of steps for analysis
                
        Returns:
            Dictionary containing:
                - sensitivity_analysis: Dict with results for each variable
                - base_case: Dict with original values
                
        Raises:
            RuntimeError: If API call fails or response is invalid
        """
        try:
            logger.debug("Starting sensitivity analysis")
            
            # Validate cash flows
            if 'base_cash_flows' not in process_data:
                logger.error("base_cash_flows is required for sensitivity analysis")
                raise ValueError("base_cash_flows is required for sensitivity analysis")
            
            base_cash_flows = process_data['base_cash_flows']
            if not isinstance(base_cash_flows, list) or len(base_cash_flows) < 2:
                logger.error("Cash flows must be a list with at least initial investment and one annual flow")
                raise ValueError("Cash flows must be a list with at least initial investment and one annual flow")

            # Default variables if not provided
            variables = process_data.get('variables', [
                "discount_rate",
                "production_volume",
                "operating_costs",
                "revenue"
            ])
            logger.debug("Analyzing sensitivity for variables: %s", variables)

            # Validate variables
            allowed_vars = {"discount_rate", "production_volume", "operating_costs", "revenue"}
            invalid_vars = set(variables) - allowed_vars
            if invalid_vars:
                logger.error("Invalid variables: %s. Must be from: %s", invalid_vars, allowed_vars)
                raise ValueError(f"Invalid variables: {invalid_vars}. Must be from: {allowed_vars}")

            # Get ranges with proper validation
            logger.debug("Validating variable ranges")
            ranges = {}
            default_ranges = {
                "discount_rate": [0.05, 0.15],
                "production_volume": [500.0, 1500.0],
                "operating_costs": [0.8, 1.2],
                "revenue": [0.8, 1.2]
            }

            for var in variables:
                if var in process_data.get('ranges', {}):
                    range_values = process_data['ranges'][var]
                    if len(range_values) != 2:
                        logger.error("Range for %s must have exactly 2 values [min, max]", var)
                        raise ValueError(f"Range for {var} must have exactly 2 values [min, max]")
                    if range_values[0] >= range_values[1]:
                        logger.error("Invalid range for %s: min must be less than max", var)
                        raise ValueError(f"Invalid range for {var}: min must be less than max")
                    
                    # Specific validations for different variables
                    if var == "discount_rate":
                        if not (0 < range_values[0] < range_values[1] < 1):
                            logger.error("Discount rate must be between 0 and 1")
                            raise ValueError("Discount rate must be between 0 and 1")
                    elif var in ["operating_costs", "revenue"]:
                        if not (0 < range_values[0] < range_values[1]):
                            logger.error("%s multipliers must be positive", var)
                            raise ValueError(f"{var} multipliers must be positive")
                    elif var == "production_volume":
                        if not (0 < range_values[0] < range_values[1]):
                            logger.error("Production volume must be positive")
                            raise ValueError("Production volume must be positive")
                    
                    ranges[var] = range_values
                else:
                    ranges[var] = default_ranges[var]

            # Validate steps
            steps = process_data.get('steps', 10)
            if not isinstance(steps, int) or not (5 <= steps <= 100):
                logger.error("Steps must be an integer between 5 and 100")
                raise ValueError("Steps must be an integer between 5 and 100")

            # Format request payload to match SensitivityAnalysisInput model
            payload = {
                'base_cash_flows': base_cash_flows,
                'variables': variables,
                'ranges': ranges,
                'steps': steps
            }

            logger.debug("Making sensitivity analysis API call")
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability/sensitivity",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error("Sensitivity analysis API call failed: %s", error_detail)
                raise RuntimeError(f"Sensitivity analysis API call failed: {error_detail}")
            
            result = response.json()
            logger.debug("Sensitivity analysis API call successful")
            
            # Validate response structure
            if 'sensitivity_analysis' not in result or 'base_case' not in result:
                logger.error("Invalid response structure from sensitivity analysis endpoint")
                raise RuntimeError("Invalid response structure from sensitivity analysis endpoint")

            # Validate sensitivity results for each variable
            sensitivity_results = result['sensitivity_analysis']
            for var in variables:
                if var not in sensitivity_results:
                    logger.error("Missing sensitivity results for variable: %s", var)
                    raise RuntimeError(f"Missing sensitivity results for variable: {var}")
                var_results = sensitivity_results[var]
                required_fields = ['values', 'range', 'base_value', 'percent_change']
                missing_fields = [field for field in required_fields if field not in var_results]
                if missing_fields:
                    logger.error("Missing fields in sensitivity results for %s: %s", var, missing_fields)
                    raise RuntimeError(f"Missing fields in sensitivity results for {var}: {missing_fields}")

            logger.info("Sensitivity analysis completed for %d variables with %d steps each", len(variables), steps)
            
            # Return structured response
            return {
                'sensitivity_analysis': sensitivity_results,
                'base_case': {
                    'cash_flows': base_cash_flows,
                    'variables': variables,
                    'ranges': ranges
                },
                'analysis_parameters': {
                    'steps': steps,
                    'variables_analyzed': variables,
                    'total_scenarios': len(variables) * steps
                }
            }
            
        except Exception as e:
            logger.error("Sensitivity analysis failed: %s", str(e), exc_info=True)
            raise RuntimeError(f"Sensitivity analysis failed: {str(e)}")

    async def get_cost_tracking(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        process_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get cost tracking data using FastAPI endpoint.
        
        Args:
            start_date: Optional start date for filtering costs
            end_date: Optional end date for filtering costs
            process_type: Optional process type for filtering costs
            
        Returns:
            Dictionary containing:
                - cost_summary: Dict with cost summaries by category
                - cost_trends: Dict with cost trends over time
                - time_range: Dict with start and end dates
                - process_metrics: Dict with process-specific metrics
                
        Raises:
            RuntimeError: If API call fails or response is invalid
        """
        try:
            # Validate date ranges if provided
            if start_date and end_date and start_date > end_date:
                raise ValueError("Start date must be before end date")

            # Format request parameters
            params = {}
            if start_date:
                if not isinstance(start_date, datetime):
                    raise ValueError("start_date must be a datetime object")
                params['start_date'] = start_date.isoformat()
            
            if end_date:
                if not isinstance(end_date, datetime):
                    raise ValueError("end_date must be a datetime object")
                params['end_date'] = end_date.isoformat()
            
            if process_type:
                if process_type not in ['baseline', 'rf', 'ir']:
                    raise ValueError("process_type must be one of: baseline, rf, ir")
                params['process_type'] = process_type
            
            logger.debug(f"Sending cost tracking request with params: {params}")
            
            # Make API call
            response = await self.client.get(
                f"{self.base_url}/api/v1/economic/profitability/costs/summary",
                params=params
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error(f"Cost tracking API call failed: {error_detail}")
                raise RuntimeError(f"Cost tracking API call failed: {error_detail}")
            
            result = response.json()
            
            # Validate response structure
            if 'summary' not in result or 'trends' not in result:
                raise RuntimeError("Invalid response structure from cost tracking endpoint")

            # Validate summary structure
            summary = result['summary']
            required_summary_fields = ['total_costs', 'cost_by_category', 'cost_by_process']
            missing_fields = [field for field in required_summary_fields if field not in summary]
            if missing_fields:
                raise RuntimeError(f"Invalid cost summary: missing fields: {missing_fields}")

            # Validate trends structure
            trends = result['trends']
            required_trend_fields = ['monthly_costs', 'category_distribution', 'process_distribution']
            missing_fields = [field for field in required_trend_fields if field not in trends]
            if missing_fields:
                raise RuntimeError(f"Invalid cost trends: missing fields: {missing_fields}")

            # Format and validate numeric values in summary
            cost_summary = {
                'total_costs': float(summary['total_costs']),
                'cost_by_category': {
                    category: float(cost)
                    for category, cost in summary['cost_by_category'].items()
                },
                'cost_by_process': {
                    process: float(cost)
                    for process, cost in summary['cost_by_process'].items()
                }
            }

            # Format and validate trends data
            cost_trends = {
                'monthly_costs': [
                    {
                        'date': entry['date'],
                        'value': float(entry['value']),
                        'category': entry['category']
                    }
                    for entry in trends['monthly_costs']
                ],
                'category_distribution': {
                    category: float(percentage)
                    for category, percentage in trends['category_distribution'].items()
                },
                'process_distribution': {
                    process: float(percentage)
                    for process, percentage in trends['process_distribution'].items()
                }
            }

            # Calculate process-specific metrics
            process_metrics = {
                'cost_efficiency': summary.get('cost_efficiency', {}),
                'cost_per_unit': summary.get('cost_per_unit', {}),
                'cost_reduction': summary.get('cost_reduction', {}),
                'trend_analysis': {
                    'slope': trends.get('trend_slope', 0.0),
                    'correlation': trends.get('trend_correlation', 0.0),
                    'forecast': trends.get('trend_forecast', [])
                }
            }

            # Return comprehensive response
            return {
                'cost_summary': cost_summary,
                'cost_trends': cost_trends,
                'time_range': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None,
                    'duration_days': (end_date - start_date).days if start_date and end_date else None
                },
                'process_metrics': process_metrics,
                'metadata': {
                    'process_type': process_type,
                    'data_points': len(cost_trends['monthly_costs']),
                    'categories_tracked': list(cost_summary['cost_by_category'].keys()),
                    'processes_tracked': list(cost_summary['cost_by_process'].keys())
                }
            }
            
        except Exception as e:
            logger.error(f"Cost tracking retrieval failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Cost tracking retrieval failed: {str(e)}")

    def calculate_comprehensive_metrics(
        self,
        cash_flows: List[float],
        initial_investment: float,
        annual_revenue: float,
        annual_opex: float,
        production_volume: float,
        project_duration: int,
        discount_rate: float,
        monte_carlo_iterations: int = 1000,
        confidence_interval: float = 0.95
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive economic metrics including enhanced business insights
        """
        try:
            # Calculate base metrics
            base_metrics = get_economic_metrics(
                cash_flows=cash_flows,
                initial_investment=initial_investment,
                discount_rate=discount_rate,
                project_duration=project_duration
            )
            
            # Calculate MCSP
            mcsp_result = calculate_mcsp(
                cash_flows=cash_flows,
                discount_rate=discount_rate,
                production_volume=production_volume,
                target_npv=0.0,
                iterations=monte_carlo_iterations,
                confidence_interval=confidence_interval
            )
            
            # Calculate additional business metrics
            gross_margin = (annual_revenue - annual_opex) / annual_revenue if annual_revenue > 0 else 0.0
            operating_margin = (annual_revenue - annual_opex - initial_investment/project_duration) / annual_revenue if annual_revenue > 0 else 0.0
            
            # Break-even analysis
            fixed_costs = initial_investment / project_duration
            variable_costs_per_unit = annual_opex / production_volume if production_volume > 0 else 0.0
            unit_price = annual_revenue / production_volume if production_volume > 0 else 0.0
            break_even_units = fixed_costs / (unit_price - variable_costs_per_unit) if (unit_price - variable_costs_per_unit) > 0 else float('inf')
            break_even_revenue = break_even_units * unit_price
            
            # Cost structure analysis
            total_annual_cost = annual_opex + fixed_costs
            cost_structure = {
                "fixed_costs": {
                    "value": fixed_costs,
                    "percentage": (fixed_costs / total_annual_cost * 100) if total_annual_cost > 0 else 0.0
                },
                "variable_costs": {
                    "value": annual_opex,
                    "percentage": (annual_opex / total_annual_cost * 100) if total_annual_cost > 0 else 0.0
                }
            }
            
            # Investment efficiency metrics
            investment_efficiency = {
                "capex_per_unit": initial_investment / production_volume if production_volume > 0 else 0.0,
                "revenue_to_investment_ratio": annual_revenue / initial_investment if initial_investment > 0 else 0.0,
                "opex_to_capex_ratio": annual_opex / initial_investment if initial_investment > 0 else 0.0
            }
            
            # Combine all metrics
            comprehensive_metrics = {
                "base_metrics": base_metrics,
                "mcsp": mcsp_result,
                "business_metrics": {
                    "margins": {
                        "gross_margin": {"value": gross_margin, "unit": "ratio"},
                        "operating_margin": {"value": operating_margin, "unit": "ratio"}
                    },
                    "break_even": {
                        "units": break_even_units,
                        "revenue": break_even_revenue,
                        "unit_price": unit_price,
                        "variable_cost_per_unit": variable_costs_per_unit
                    },
                    "cost_structure": cost_structure,
                    "investment_efficiency": investment_efficiency
                }
            }
            
            # Store metrics history
            self.metrics_history.append({
                "timestamp": datetime.now().isoformat(),
                "metrics": comprehensive_metrics
            })
            
            return comprehensive_metrics
            
        except Exception as e:
            logger.error(f"Error calculating comprehensive metrics: {str(e)}")
            raise
            
    def get_metrics_trends(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get historical trends of economic metrics
        """
        filtered_history = [
            entry for entry in self.metrics_history
            if (not start_date or datetime.fromisoformat(entry["timestamp"]) >= start_date) and
               (not end_date or datetime.fromisoformat(entry["timestamp"]) <= end_date)
        ]
        
        trends = {
            "npv": [],
            "roi": [],
            "mcsp": [],
            "margins": [],
            "efficiency": []
        }
        
        for entry in filtered_history:
            metrics = entry["metrics"]
            timestamp = entry["timestamp"]
            
            # Extract and store trends
            trends["npv"].append({
                "timestamp": timestamp,
                "value": metrics["base_metrics"]["npv"]["value"]
            })
            
            trends["roi"].append({
                "timestamp": timestamp,
                "value": metrics["base_metrics"]["roi"]["value"]
            })
            
            trends["mcsp"].append({
                "timestamp": timestamp,
                "value": metrics["mcsp"]["value"]
            })
            
            trends["margins"].append({
                "timestamp": timestamp,
                "gross_margin": metrics["business_metrics"]["margins"]["gross_margin"]["value"],
                "operating_margin": metrics["business_metrics"]["margins"]["operating_margin"]["value"]
            })
            
            trends["efficiency"].append({
                "timestamp": timestamp,
                "capex_per_unit": metrics["business_metrics"]["investment_efficiency"]["capex_per_unit"],
                "opex_to_capex_ratio": metrics["business_metrics"]["investment_efficiency"]["opex_to_capex_ratio"]
            })
        
        return trends
        
    def analyze_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance indicators and provide insights
        """
        insights = {
            "profitability": {
                "status": "positive" if metrics["base_metrics"]["npv"]["value"] > 0 else "negative",
                "key_drivers": []
            },
            "efficiency": {
                "status": "high" if metrics["business_metrics"]["margins"]["operating_margin"]["value"] > 0.2 else "low",
                "improvement_areas": []
            },
            "risk": {
                "level": "low" if metrics["mcsp"]["std_dev"] < metrics["mcsp"]["value"] * 0.1 else "high",
                "factors": []
            }
        }
        
        # Analyze profitability drivers
        if metrics["business_metrics"]["margins"]["gross_margin"]["value"] > 0.3:
            insights["profitability"]["key_drivers"].append("Strong gross margins")
        if metrics["business_metrics"]["investment_efficiency"]["revenue_to_investment_ratio"] > 1.0:
            insights["profitability"]["key_drivers"].append("Efficient capital utilization")
            
        # Analyze efficiency
        if metrics["business_metrics"]["investment_efficiency"]["capex_per_unit"] > metrics["mcsp"]["value"]:
            insights["efficiency"]["improvement_areas"].append("High capital intensity per unit")
        if metrics["business_metrics"]["cost_structure"]["variable_costs"]["percentage"] > 70:
            insights["efficiency"]["improvement_areas"].append("High variable cost ratio")
            
        # Analyze risk factors
        production_volume = metrics["business_metrics"]["annual_metrics"]["production_volume"]
        if metrics["business_metrics"]["break_even"]["units"] > production_volume * 0.8:
            insights["risk"]["factors"].append("High break-even point")
        if metrics["mcsp"]["confidence_interval"]["upper"] - metrics["mcsp"]["confidence_interval"]["lower"] > metrics["mcsp"]["value"] * 0.2:
            insights["risk"]["factors"].append("High MCSP volatility")
            
        return insights

    
