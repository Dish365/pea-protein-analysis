from typing import Dict, List, Any, Optional
import httpx
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class EconomicIntegrator:
    """Integrates economic analysis components through FastAPI endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.base_url = base_url

    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()

    async def analyze_economics(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate complete economic analysis through FastAPI endpoints"""
        try:
            # Calculate CAPEX
            capex_results = await self.calculate_capex(process_data)
            
            # Calculate OPEX
            opex_results = await self.calculate_opex(process_data)
            
            # Calculate profitability metrics
            profitability_results = await self.analyze_profitability(
                capex=capex_results['capex_summary']['total_capex'],
                opex=opex_results['opex_summary']['total_opex'],
                process_data={
                    **process_data,
                    'equipment': {'cost': capex_results['capex_summary']['equipment_costs']},
                    'utilities_cost': opex_results['opex_summary']['utility_costs'],
                    'materials_cost': opex_results['opex_summary']['raw_material_costs'],
                    'labor_cost': opex_results['opex_summary']['labor_costs'],
                    'maintenance_cost': opex_results['opex_summary']['maintenance_costs']
                }
            )
            
            # Get comprehensive economic analysis
            economic_results = await self.get_economic_analysis({
                'capex': capex_results['capex_summary'],
                'opex': opex_results['opex_summary'],
                'production_volume': process_data.get('production_volume', 0),
                'project_duration': process_data.get('project_duration', 10),
                'discount_rate': process_data.get('discount_rate', 0.1),
                'cash_flows': profitability_results.get('cash_flows', [])
            })
            
            # Get sensitivity analysis
            sensitivity_results = await self.analyze_sensitivity(process_data)
            
            # Get cost tracking data
            cost_tracking = await self.get_cost_tracking()
            
            return {
                'capex_analysis': {
                    'summary': capex_results['capex_summary'],
                    'equipment_breakdown': capex_results['equipment_breakdown'],
                    'process_type': capex_results['process_type']
                },
                'opex_analysis': {
                    'summary': opex_results['opex_summary'],
                    'utilities_breakdown': opex_results['utilities_breakdown'],
                    'raw_materials_breakdown': opex_results['raw_materials_breakdown'],
                    'labor_breakdown': opex_results['labor_breakdown'],
                    'process_type': opex_results['process_type']
                },
                'profitability_analysis': {
                    'metrics': profitability_results['metrics'],
                    'monte_carlo': profitability_results.get('monte_carlo'),
                    'cash_flows': profitability_results['cash_flows']
                },
                'economic_analysis': {
                    'investment_analysis': economic_results['investment_analysis'],
                    'annual_costs': economic_results['annual_costs'],
                    'profitability_metrics': economic_results['profitability_metrics']
                },
                'sensitivity_analysis': sensitivity_results['sensitivity_analysis'],
                'cost_tracking': {
                    'summary': cost_tracking['cost_summary'],
                    'trends': cost_tracking['cost_trends']
                }
            }
            
        except Exception as e:
            raise RuntimeError(f"Economic analysis failed: {str(e)}")

    async def calculate_capex(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate capital expenditure using FastAPI endpoint"""
        try:
            # Extract equipment data from the correct location in process_data
            equipment_list = process_data.get('equipment', [])
            
            # Extract equipment data with proper validation
            if equipment_list and isinstance(equipment_list[0], dict):
                # Use first equipment item if available
                first_equipment = equipment_list[0]
                equipment = {
                    "name": "main_equipment",
                    "cost": first_equipment.get('cost', 50000.0),  # Use reasonable defaults
                    "efficiency": first_equipment.get('efficiency', 0.85),
                    "maintenance_cost": first_equipment.get('maintenance_cost', 5000.0),
                    "energy_consumption": first_equipment.get('energy_consumption', 100.0),
                    "processing_capacity": first_equipment.get('processing_capacity', 1000.0)
                }
            else:
                # Fallback to process_data fields with reasonable defaults
                equipment = {
                    "name": "main_equipment",
                    "cost": process_data.get('capex', {}).get('equipment_cost', 50000.0),
                    "efficiency": process_data.get('equipment_efficiency', 0.85),
                    "maintenance_cost": process_data.get('maintenance_cost', 5000.0),
                    "energy_consumption": process_data.get('electricity_consumption', 100.0),
                    "processing_capacity": process_data.get('production_volume', 1000.0)
                }
            
            # Format economic factors to match EconomicFactors model
            economic_factors = {
                "installation_factor": process_data.get('installation_factor', 0.2),
                "indirect_costs_factor": process_data.get('indirect_costs_factor', 0.15),
                "maintenance_factor": process_data.get('maintenance_factor', 0.05),
                "project_duration": process_data.get('project_duration', 10),
                "discount_rate": process_data.get('discount_rate', 0.1),
                "production_volume": process_data.get('production_volume', 1000.0)
            }
            
            # Prepare request payload
            payload = {
                'equipment_list': [equipment],
                'economic_factors': economic_factors,
                'indirect_factors': process_data.get('indirect_factors', []),
                'process_type': process_data.get('process_type', 'baseline')
            }
            
            logger.debug(f"CAPEX API payload: {json.dumps(payload)}")
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/capex/calculate",
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"CAPEX API call failed with status {response.status_code}: {response.text}")
                raise RuntimeError(f"CAPEX API call failed: {response.text}")
                
            result = response.json()
            
            factors_info = result.get('indirect_factors', {})
            logger.info(f"CAPEX calculation used {factors_info.get('source', 'unknown')} indirect factors")
            
            return result
            
        except Exception as e:
            logger.error(f"CAPEX calculation failed: {str(e)}")
            raise RuntimeError(f"CAPEX calculation failed: {str(e)}")

    async def calculate_opex(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate operational expenditure using FastAPI endpoint"""
        try:
            # Extract equipment costs from the first equipment item or capex data
            equipment_list = process_data.get('equipment', [])
            equipment_costs = (
                equipment_list[0].get('cost', 50000.0) if equipment_list 
                else process_data.get('capex', {}).get('equipment_cost', 50000.0)
            )
            
            # Format utilities
            utilities = []
            if process_data.get('electricity_consumption'):
                utilities.append({
                    'name': 'electricity',
                    'consumption': process_data['electricity_consumption'],
                    'unit_price': process_data.get('utility_cost', 1.5),
                    'unit': 'kWh'
                })
            if process_data.get('cooling_consumption'):
                utilities.append({
                    'name': 'cooling',
                    'consumption': process_data['cooling_consumption'],
                    'unit_price': process_data.get('utility_cost', 1.5),
                    'unit': 'kWh'
                })
            if process_data.get('water_consumption'):
                utilities.append({
                    'name': 'water',
                    'consumption': process_data['water_consumption'],
                    'unit_price': process_data.get('utility_cost', 1.5),
                    'unit': 'kg'
                })
            
            # Add default utility if none specified
            if not utilities:
                utilities.append({
                    'name': 'electricity',
                    'consumption': process_data.get('energy_consumption', 100.0),
                    'unit_price': process_data.get('utility_cost', 1.5),
                    'unit': 'kWh'
                })
            
            # Format raw materials - ensure at least one material is present
            raw_materials = []
            if process_data.get('input_mass'):
                raw_materials.append({
                    'name': 'feed_material',
                    'quantity': process_data['input_mass'],
                    'unit_price': process_data.get('raw_material_cost', 2.5),
                    'unit': 'kg'
                })
            else:
                # Add default material if none specified
                raw_materials.append({
                    'name': 'feed_material',
                    'quantity': 1000.0,
                    'unit_price': 2.5,
                    'unit': 'kg'
                })
            
            # Prepare request payload using the OpexInput model structure
            payload = {
                'utilities': utilities,
                'raw_materials': raw_materials,
                'labor_config': process_data.get('labor_config', {
                    'hourly_wage': 25.0,
                    'hours_per_week': 40,
                    'weeks_per_year': 52,
                    'num_workers': 1
                }),
                'equipment_costs': equipment_costs,
                'economic_factors': {
                    'installation_factor': process_data.get('installation_factor', 0.2),
                    'indirect_costs_factor': process_data.get('indirect_costs_factor', 0.15),
                    'maintenance_factor': process_data.get('maintenance_factor', 0.05),
                    'project_duration': process_data.get('project_duration', 10),
                    'discount_rate': process_data.get('discount_rate', 0.1),
                    'production_volume': process_data.get('production_volume', 1000.0)
                },
                'process_type': process_data.get('process_type', 'baseline')
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/opex/calculate",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error(f"OPEX API call failed: {error_detail}")
                raise RuntimeError(f"OPEX API call failed: {error_detail}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"OPEX calculation failed: {str(e)}")
            raise RuntimeError(f"OPEX calculation failed: {str(e)}")

    async def analyze_profitability(self,
                                  capex: float,
                                  opex: float,
                                  process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze profitability metrics using FastAPI endpoint.
        Validation is handled by the endpoint.
        """
        try:
            # Get project parameters directly from process_data
            project_duration = process_data.get('project_duration', 10)
            discount_rate = process_data.get('discount_rate', 0.1)
            production_volume = process_data.get('production_volume', 1000.0)
            
            # Calculate initial cash flow (negative CAPEX)
            initial_investment = -capex
            
            # Calculate annual cash flows (revenue - OPEX)
            annual_cash_flow = process_data.get('revenue_per_year', opex * 1.2) - opex
            
            # Generate cash flows list
            cash_flows = [initial_investment]  # First year is investment
            cash_flows.extend([annual_cash_flow] * project_duration)  # Add annual cash flows
            
            # Prepare request payload using the ProfitabilityInput model structure
            payload = {
                'capex': {
                    "total_investment": capex,
                    "equipment_cost": process_data.get('equipment', {}).get('cost', 0),
                    "installation_cost": capex * process_data.get('installation_factor', 0.2),
                    "indirect_cost": capex * process_data.get('indirect_costs_factor', 0.15)
                },
                'opex': {
                    "total_annual_cost": opex,
                    "utilities_cost": process_data.get('utilities_cost', 0),
                    "materials_cost": process_data.get('materials_cost', 0),
                    "labor_cost": process_data.get('labor_cost', 0),
                    "maintenance_cost": process_data.get('maintenance_cost', 0)
                },
                'economic_factors': {
                    "project_duration": project_duration,
                    "discount_rate": discount_rate,
                    "production_volume": production_volume,
                    "installation_factor": process_data.get('installation_factor', 0.2),
                    "indirect_costs_factor": process_data.get('indirect_costs_factor', 0.15),
                    "maintenance_factor": process_data.get('maintenance_factor', 0.05)
                },
                'process_type': process_data.get('process_type', 'baseline'),
                'cash_flows': cash_flows,
                'monte_carlo_iterations': process_data.get('monte_carlo_iterations', 1000),
                'uncertainty': process_data.get('uncertainty', 0.1)
            }
            
            logger.debug(f"Sending profitability analysis request with payload: {json.dumps(payload)}")
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability/analyze",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error(f"Profitability API call failed: {error_detail}")
                raise RuntimeError(f"Profitability API call failed: {error_detail}")
                
            result = response.json()
            
            # Return structured response matching endpoint output
            return {
                'metrics': result['metrics'],
                'monte_carlo': result.get('monte_carlo'),
                'cash_flows': cash_flows,
                'process_type': result.get('process_type'),
                'production_volume': production_volume
            }
            
        except Exception as e:
            logger.error(f"Profitability analysis failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Profitability analysis failed: {str(e)}")

    async def analyze_sensitivity(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform sensitivity analysis using FastAPI endpoint.
        Validation is handled by the endpoint.
        """
        try:
            # Calculate cash flows if not provided
            if not process_data.get('cash_flows'):
                # Get CAPEX and OPEX data
                capex_results = await self.calculate_capex(process_data)
                opex_results = await self.calculate_opex(process_data)
                
                # Calculate initial investment (negative)
                initial_investment = -capex_results['capex_summary']['total_capex']
                
                # Calculate annual cash flow (revenue - opex)
                annual_revenue = opex_results['opex_summary']['total_opex'] * 1.2  # Assume 20% margin
                annual_cash_flow = annual_revenue - opex_results['opex_summary']['total_opex']
                
                # Generate cash flows list
                process_data['cash_flows'] = [initial_investment] + [annual_cash_flow] * process_data.get('project_duration', 10)

            # Format request payload
            payload = {
                'base_cash_flows': process_data['cash_flows'],
                'discount_rate': process_data.get('discount_rate', 0.1),
                'production_volume': process_data.get('production_volume', 1000.0),
                'sensitivity_range': process_data.get('sensitivity_range', 0.2),
                'steps': process_data.get('steps', 10)
            }

            logger.debug(f"Sending sensitivity analysis request with payload: {json.dumps(payload)}")
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability/sensitivity",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error(f"Sensitivity analysis API call failed: {error_detail}")
                raise RuntimeError(f"Sensitivity analysis API call failed: {error_detail}")
            
            result = response.json()
            
            # Return structured response matching endpoint output
            return {
                'sensitivity_analysis': result['sensitivity_analysis'],
                'variables_analyzed': [
                    'discount_rate',
                    'production_volume'
                ]
            }
            
        except Exception as e:
            logger.error(f"Sensitivity analysis failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Sensitivity analysis failed: {str(e)}")

    async def get_cost_tracking(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get cost tracking data using FastAPI endpoint.
        Validation is handled by the endpoint.
        """
        try:
            # Format request parameters
            params = {}
            if start_date:
                params['start_date'] = start_date.isoformat()
            if end_date:
                params['end_date'] = end_date.isoformat()
            
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
            
            # Return structured response matching endpoint output
            return {
                'cost_summary': result['summary'],
                'cost_trends': result['trends'],
                'time_range': {
                    'start_date': start_date.isoformat() if start_date else None,
                    'end_date': end_date.isoformat() if end_date else None
                }
            }
            
        except Exception as e:
            logger.error(f"Cost tracking retrieval failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Cost tracking retrieval failed: {str(e)}")

    async def get_economic_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive economic analysis using FastAPI endpoint.
        Validation is handled by the endpoint.
        """
        try:
            # Format request payload to match ComprehensiveAnalysisInput model
            payload = {
                'capex': {
                    'equipment_cost': analysis_data['capex'].get('equipment_costs', 0),
                    'installation_cost': analysis_data['capex'].get('installation_costs', 0),
                    'indirect_cost': analysis_data['capex'].get('indirect_costs', 0),
                    'total_investment': analysis_data['capex'].get('total_investment', 
                                      analysis_data['capex'].get('total_capex', 0))
                },
                'opex': {
                    'total_annual_cost': analysis_data['opex'].get('total_opex', 0),
                    'utilities_cost': analysis_data['opex'].get('utilities_cost', 0),
                    'materials_cost': analysis_data['opex'].get('materials_cost', 0),
                    'labor_cost': analysis_data['opex'].get('labor_cost', 0),
                    'maintenance_cost': analysis_data['opex'].get('maintenance_cost', 0)
                },
                'production_volume': analysis_data.get('production_volume', 0),
                'project_duration': analysis_data.get('project_duration', 10),
                'discount_rate': analysis_data.get('discount_rate', 0.1),
                'cash_flows': analysis_data.get('cash_flows', [])
            }
            
            logger.debug(f"Sending comprehensive analysis request with payload: {json.dumps(payload)}")
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('detail', str(response.text))
                logger.error(f"Economic analysis API call failed: {error_detail}")
                raise RuntimeError(f"Economic analysis API call failed: {error_detail}")
            
            result = response.json()
            
            # Return structured response matching endpoint output
            return {
                'investment_analysis': result['investment_analysis'],
                'annual_costs': result['annual_costs'],
                'profitability_metrics': result['profitability_metrics']
            }
            
        except Exception as e:
            logger.error(f"Economic analysis failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Economic analysis failed: {str(e)}")
