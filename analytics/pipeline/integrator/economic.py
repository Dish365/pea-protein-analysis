from typing import Dict, List, Any
import httpx

class EconomicIntegrator:
    """Integrates economic analysis components through FastAPI endpoints"""
    
    def __init__(self):
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.base_url = "http://localhost:8001"

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
                process_data=process_data
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
            
            return {
                'capex_analysis': capex_results,
                'opex_analysis': opex_results,
                'profitability_analysis': profitability_results,
                'economic_analysis': economic_results
            }
            
        except Exception as e:
            raise RuntimeError(f"Economic analysis failed: {str(e)}")

    async def calculate_capex(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate capital expenditure using FastAPI endpoint"""
        try:
            # Prepare equipment data
            equipment_list = process_data.get('equipment_list', [])
            indirect_factors = process_data.get('indirect_factors', [])
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/capex/calculate",
                json={
                    'equipment_list': equipment_list,
                    'indirect_factors': indirect_factors,
                    'installation_factor': process_data.get('installation_factor', 0.2),
                    'indirect_costs_factor': process_data.get('indirect_costs_factor', 0.15)
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"CAPEX API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"CAPEX calculation failed: {str(e)}")

    async def calculate_opex(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate operational expenditure using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/opex/calculate",
                json={
                    'utilities': process_data.get('utilities', []),
                    'raw_materials': process_data.get('raw_materials', []),
                    'equipment_costs': process_data.get('equipment_costs', 0),
                    'labor_config': process_data.get('labor_config', {}),
                    'maintenance_factor': process_data.get('maintenance_factor', 0.05)
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"OPEX API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"OPEX calculation failed: {str(e)}")

    async def analyze_profitability(self,
                                  capex: float,
                                  opex: float,
                                  process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze profitability metrics using FastAPI endpoint"""
        try:
            # Prepare cash flows
            cash_flows = self._prepare_cash_flows(
                capex=capex,
                opex=opex,
                revenue=process_data.get('revenue', []),
                project_duration=process_data.get('project_duration', 10)
            )
            
            # Get profitability metrics from FastAPI
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability/analyze",
                json={
                    'cash_flows': cash_flows,
                    'discount_rate': process_data.get('discount_rate', 0.1),
                    'initial_investment': capex,
                    'gain_from_investment': sum(cash_flows),
                    'cost_of_investment': capex + opex,
                    'production_volume': process_data.get('production_volume', 1000.0),
                    'monte_carlo_iterations': process_data.get('monte_carlo_iterations', 1000),
                    'uncertainty': process_data.get('uncertainty', 0.1)
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Profitability API call failed: {response.text}")
            
            return {
                **response.json()['metrics'],
                'cash_flows': cash_flows
            }
            
        except Exception as e:
            raise RuntimeError(f"Profitability analysis failed: {str(e)}")

    async def get_economic_analysis(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive economic analysis using FastAPI endpoint"""
        try:
            # Prepare CAPEX and OPEX data
            capex_data = {
                'equipment_cost': analysis_data['capex'].get('equipment_cost', 0),
                'installation_cost': analysis_data['capex'].get('installation_cost', 0),
                'indirect_cost': analysis_data['capex'].get('indirect_cost', 0)
            }
            
            opex_data = {
                'utilities_cost': analysis_data['opex'].get('utilities_cost', 0),
                'materials_cost': analysis_data['opex'].get('materials_cost', 0),
                'labor_cost': analysis_data['opex'].get('labor_cost', 0),
                'maintenance_cost': analysis_data['opex'].get('maintenance_cost', 0),
                'total_opex': analysis_data['opex'].get('total_opex', 0)
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/economic/profitability",
                json={
                    'capex': capex_data,
                    'opex': opex_data,
                    'production_volume': analysis_data.get('production_volume', 0),
                    'project_duration': analysis_data.get('project_duration', 10),
                    'discount_rate': analysis_data.get('discount_rate', 0.1),
                    'cash_flows': analysis_data.get('cash_flows', [])
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Economic analysis API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"Economic analysis failed: {str(e)}")

    def _prepare_cash_flows(self,
                          capex: float,
                          opex: float,
                          revenue: List[float],
                          project_duration: int) -> List[float]:
        """Prepare cash flow projections"""
        # Initial investment (negative cash flow)
        cash_flows = [-capex]
        
        # Project annual cash flows
        annual_cash_flow = revenue[0] - opex if revenue else -opex
        for year in range(project_duration):
            if year < len(revenue):
                cash_flows.append(revenue[year] - opex)
            else:
                cash_flows.append(annual_cash_flow)
                
        return cash_flows
