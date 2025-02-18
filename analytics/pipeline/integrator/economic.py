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
            
            # Format equipment data with proper validation
            if equipment_list and isinstance(equipment_list[0], dict):
                formatted_equipment = []
                for equip in equipment_list:
                    formatted_equipment.append({
                        "name": str(equip.get('name', 'equipment')),
                        "cost": float(equip.get('cost', process_data.get('equipment_cost', 50000.0))),
                        "efficiency": float(equip.get('efficiency', 0.85)),
                        "maintenance_cost": float(equip.get('maintenance_cost', process_data.get('maintenance_cost', 5000.0))),
                        "energy_consumption": float(equip.get('energy_consumption', process_data.get('electricity_consumption', 100.0))),
                        "processing_capacity": float(equip.get('processing_capacity', process_data.get('production_volume', 1000.0)))
                    })
            else:
                # Fallback to process_data fields with reasonable defaults
                formatted_equipment = [{
                    "name": "main_equipment",
                    "cost": float(process_data.get('equipment_cost', 50000.0)),
                    "efficiency": float(process_data.get('equipment_efficiency', 0.85)),
                    "maintenance_cost": float(process_data.get('maintenance_cost', 5000.0)),
                    "energy_consumption": float(process_data.get('electricity_consumption', 100.0)),
                    "processing_capacity": float(process_data.get('production_volume', 1000.0))
                }]
            
            # Format economic factors to match EconomicFactors model
            economic_factors = {
                "installation_factor": float(process_data.get('installation_factor', 0.2)),
                "indirect_costs_factor": float(process_data.get('indirect_costs_factor', 0.15)),
                "maintenance_factor": float(process_data.get('maintenance_factor', 0.05)),
                "project_duration": int(process_data.get('project_duration', 10)),
                "discount_rate": float(process_data.get('discount_rate', 0.1)),
                "production_volume": float(process_data.get('production_volume', 1000.0))
            }
            
            # Format indirect factors
            base_cost = sum(equip["cost"] for equip in formatted_equipment)
            indirect_factors = process_data.get('indirect_factors', [
                {
                    "name": "engineering",
                    "cost": base_cost,
                    "percentage": 0.15
                },
                {
                    "name": "contingency",
                    "cost": base_cost,
                    "percentage": 0.10
                },
                {
                    "name": "construction",
                    "cost": base_cost,
                    "percentage": 0.20
                }
            ])
            
            # Prepare payload for CAPEX endpoint
            payload = {
                "equipment_list": formatted_equipment,
                "economic_factors": economic_factors,
                "indirect_factors": indirect_factors,
                "process_type": process_data.get('process_type', 'baseline')
            }
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/capex/calculate",
                json=payload
            )
            
            if response.status_code != 200:
                error_detail = response.json().get("detail", response.text)
                raise RuntimeError(f"CAPEX calculation failed: {error_detail}")
                
            result = response.json()
            
            # Extract and validate the capex_summary
            capex_summary = result.get('capex_summary')
            if not capex_summary or not isinstance(capex_summary, dict):
                raise RuntimeError("Invalid CAPEX response: missing or invalid capex_summary")
            
            # Ensure all required fields are present and are numeric
            required_fields = ['total_capex', 'equipment_costs', 'installation_costs', 'indirect_costs']
            for field in required_fields:
                if field not in capex_summary or not isinstance(capex_summary[field], (int, float)):
                    raise RuntimeError(f"Invalid CAPEX response: missing or invalid {field}")
            
            logger.info(f"CAPEX calculation successful: {capex_summary}")
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

    async def analyze_profitability(self, capex: float, opex: float, process_data: Dict):
        """Analyze profitability using the profitability endpoint"""
        payload = {
            "capex": {
                "total_capex": capex,
                "equipment_costs": process_data.get('equipment', {}).get('cost', 0),
                "installation_costs": process_data.get('installation_costs', capex * 0.2),
                "indirect_costs": process_data.get('indirect_costs', capex * 0.1)
            },
            "opex": {
                "total_opex": opex,
                "utility_costs": process_data.get('utilities_cost', opex * 0.3),
                "raw_material_costs": process_data.get('materials_cost', opex * 0.4),
                "labor_costs": process_data.get('labor_cost', opex * 0.2),
                "maintenance_costs": process_data.get('maintenance_cost', opex * 0.1)
            },
            "revenue_data": process_data.get('revenue', {
                "annual_revenue": opex * 1.2  # Default 20% margin if not provided
            }),
            "economic_factors": {
                "discount_rate": process_data.get('discount_rate', 0.1),
                "project_duration": process_data.get('project_duration', 10),
                "production_volume": process_data.get('production_volume', 1000.0),
                "installation_factor": process_data.get('installation_factor', 0.2),
                "indirect_costs_factor": process_data.get('indirect_costs_factor', 0.15),
                "maintenance_factor": process_data.get('maintenance_factor', 0.05)
            },
            "process_type": process_data.get('process_type', 'baseline'),
            "monte_carlo_iterations": process_data.get('monte_carlo_iterations', 1000),
            "uncertainty": process_data.get('uncertainty', 0.1)
        }
        
        response = await self.client.post(
            f"{self.base_url}/api/v1/economic/profitability/analyze",
            json=payload
        )
        
        result = response.json()
        
        # Extract cash flows from response
        cash_flows = result.get('cash_flows', {})
        
        # Extract metrics from response
        metrics = result.get('metrics', {})
        
        # Extract key financial indicators
        financial_indicators = {
            'npv': metrics.get('npv', 0.0),
            'roi': metrics.get('roi', 0.0),
            'payback_period': metrics.get('payback', 0.0),
            'mcsp': metrics.get('mcsp', {}).get('value', 0.0) if metrics.get('mcsp') else 0.0
        }
        
        # Log the financial indicators for debugging
        logger.debug(f"Financial indicators calculated: {financial_indicators}")
        
        return {
            'metrics': metrics,
            'process_type': result['process_type'],
            'monte_carlo': metrics.get('monte_carlo'),
            'production_volume': process_data.get('production_volume', 1000.0),
            'cash_flows': {
                'initial_investment': cash_flows.get('initial_investment', -capex),
                'annual_flows': cash_flows.get('annual_flows', []),
                'total_flows': cash_flows.get('total_flows', 0.0),
                'discounted_flows': cash_flows.get('discounted_flows', [])
            },
            'financial_indicators': financial_indicators
        }

    async def analyze_sensitivity(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform sensitivity analysis using FastAPI endpoint.
        Validation is handled by the endpoint.
        """
        try:
            # Calculate cash flows if not provided
            if not process_data.get('cash_flows'):
                # Get profitability analysis first to get cash flows
                capex_results = await self.calculate_capex(process_data)
                opex_results = await self.calculate_opex(process_data)
                
                profitability_results = await self.analyze_profitability(
                    capex=capex_results['capex_summary']['total_capex'],
                    opex=opex_results['opex_summary']['total_opex'],
                    process_data=process_data
                )
                
                # Use calculated cash flows
                cash_flows = profitability_results['cash_flows']
                process_data['cash_flows'] = [
                    cash_flows['initial_investment'],
                    *cash_flows['annual_flows']
                ]

            # Format request payload to match SensitivityAnalysisInput model
            payload = {
                'base_cash_flows': process_data['cash_flows'],
                'variables': process_data.get('variables', [
                    "discount_rate",
                    "production_volume",
                    "operating_costs",
                    "revenue"
                ]),
                'ranges': process_data.get('ranges', {
                    "discount_rate": (0.05, 0.15),
                    "production_volume": (500.0, 1500.0),
                    "operating_costs": (0.8, 1.2),
                    "revenue": (0.8, 1.2)
                }),
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
                'base_case': result['base_case'],
                'variables_analyzed': result['variables_analyzed'],
                'steps': result['steps'],
                'implementation': result['implementation']
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
                'equipment_list': analysis_data.get('equipment_list', []),
                'utilities': analysis_data.get('utilities', []),
                'raw_materials': analysis_data.get('raw_materials', []),
                'labor_config': analysis_data.get('labor_config', {}),
                'revenue_data': analysis_data.get('revenue_data', {}),
                'economic_factors': {
                    'installation_factor': analysis_data.get('installation_factor', 0.3),
                    'indirect_costs_factor': analysis_data.get('indirect_costs_factor', 0.45),
                    'maintenance_factor': analysis_data.get('maintenance_factor', 0.02),
                    'project_duration': analysis_data.get('project_duration', 10),
                    'discount_rate': analysis_data.get('discount_rate', 0.1),
                    'production_volume': analysis_data.get('production_volume', 1000.0)
                },
                'process_type': analysis_data.get('process_type', 'baseline'),
                'monte_carlo_iterations': analysis_data.get('monte_carlo_iterations', 1000),
                'uncertainty': analysis_data.get('uncertainty', 0.1)
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
                'investment_analysis': result.get('investment_analysis', {}),
                'operational_costs': result.get('operational_costs', {}),
                'profitability_metrics': result.get('profitability_metrics', {}),
                'breakdowns': {
                    'equipment': result.get('breakdowns', {}).get('equipment', []),
                    'utilities': result.get('breakdowns', {}).get('utilities', []),
                    'raw_materials': result.get('breakdowns', {}).get('raw_materials', []),
                    'labor': result.get('breakdowns', {}).get('labor', {}),
                    'indirect_factors': result.get('breakdowns', {}).get('indirect_factors', [])
                },
                'process_type': result.get('process_type'),
                'analysis_parameters': {
                    'monte_carlo_iterations': result.get('analysis_parameters', {}).get('monte_carlo_iterations'),
                    'uncertainty': result.get('analysis_parameters', {}).get('uncertainty'),
                    'project_duration': result.get('analysis_parameters', {}).get('project_duration'),
                    'discount_rate': result.get('analysis_parameters', {}).get('discount_rate'),
                    'production_volume': result.get('analysis_parameters', {}).get('production_volume')
                },
                'cash_flows': result.get('cash_flows', {
                    'initial_investment': 0.0,
                    'annual_flows': [],
                    'total_flows': 0.0,
                    'discounted_flows': []
                })
            }
            
        except Exception as e:
            logger.error(f"Economic analysis failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Economic analysis failed: {str(e)}")
