from typing import Dict, List, Optional, Any
import ctypes
import httpx
import asyncio
from pathlib import Path

from analytics.economic.capex_analyzer import CapitalExpenditureAnalysis
from analytics.economic.opex_analyzer import OperationalExpenditureAnalysis
from analytics.economic.profitability_analyzer import ProfitabilityAnalysis

class EconomicIntegrator:
    """Integrates economic analysis components with FastAPI and Rust"""
    
    def __init__(self):
        # Initialize service components
        self.capex_analysis = CapitalExpenditureAnalysis()
        self.opex_analysis = OperationalExpenditureAnalysis()
        self.profitability_analysis = ProfitabilityAnalysis()
        
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = "http://localhost:8000/process-analysis"
        
        # Load Rust library for Monte Carlo simulations
        lib_path = (
            Path(__file__).parent.parent.parent.parent
            / "backend/rust_modules/target/release/libmonte_carlo.so"
        )
        self.lib = ctypes.CDLL(str(lib_path))
        self._configure_rust_functions()

    def _configure_rust_functions(self) -> None:
        """Configure Rust function signatures"""
        self.lib.run_monte_carlo_simulation.argtypes = [
            ctypes.POINTER(ctypes.c_double),  # base_values
            ctypes.c_size_t,  # len
            ctypes.c_size_t,  # iterations
            ctypes.c_double,  # uncertainty
            ctypes.POINTER(ctypes.c_double),  # results
        ]
        self.lib.run_monte_carlo_simulation.restype = None

    async def analyze_economics(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate complete economic analysis"""
        try:
            # Calculate CAPEX
            capex_results = await self.calculate_capex(process_data)
            
            # Calculate OPEX
            opex_results = await self.calculate_opex(process_data)
            
            # Calculate profitability metrics
            profitability_results = await self.analyze_profitability(
                capex=capex_results['total_capex'],
                opex=opex_results['total_opex'],
                process_data=process_data
            )
            
            return {
                'capex_analysis': capex_results,
                'opex_analysis': opex_results,
                'profitability_analysis': profitability_results
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
                f"{self.api_base_url}/capex/calculate",
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
                f"{self.api_base_url}/opex/calculate",
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
        """Analyze profitability metrics using FastAPI endpoint and Rust"""
        try:
            # Prepare cash flows
            cash_flows = self._prepare_cash_flows(
                capex=capex,
                opex=opex,
                revenue=process_data.get('revenue', []),
                project_duration=process_data.get('project_duration', 10)
            )
            
            # Get base profitability metrics from FastAPI
            response = await self.client.post(
                f"{self.api_base_url}/profitability",
                json={
                    'cash_flows': cash_flows,
                    'discount_rate': process_data.get('discount_rate', 0.1),
                    'initial_investment': capex,
                    'gain_from_investment': sum(cash_flows),
                    'cost_of_investment': capex + opex
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Profitability API call failed: {response.text}")
            
            base_results = response.json()
            
            # Run Monte Carlo simulation using Rust
            monte_carlo_results = await self._run_monte_carlo_simulation(
                cash_flows=cash_flows,
                iterations=process_data.get('monte_carlo_iterations', 1000),
                uncertainty=process_data.get('uncertainty', 0.1)
            )
            
            return {
                **base_results,
                'monte_carlo_analysis': monte_carlo_results
            }
            
        except Exception as e:
            raise RuntimeError(f"Profitability analysis failed: {str(e)}")

    def _prepare_cash_flows(self,
                          capex: float,
                          opex: float,
                          revenue: List[float],
                          project_duration: int) -> List[float]:
        """Prepare cash flow projections"""
        cash_flows = [-capex]  # Initial investment
        
        for year in range(project_duration):
            if year < len(revenue):
                annual_cash_flow = revenue[year] - opex
            else:
                # Project last known revenue for remaining years
                annual_cash_flow = revenue[-1] - opex if revenue else -opex
            cash_flows.append(annual_cash_flow)
            
        return cash_flows

    async def _run_monte_carlo_simulation(self,
                                        cash_flows: List[float],
                                        iterations: int = 1000,
                                        uncertainty: float = 0.1) -> Dict[str, float]:
        """Run Monte Carlo simulation using Rust"""
        # Prepare arrays for Rust
        base_values = (ctypes.c_double * len(cash_flows))(*cash_flows)
        results = (ctypes.c_double * 4)()  # [mean, std_dev, min_value, max_value]
        
        # Run simulation
        self.lib.run_monte_carlo_simulation(
            base_values,
            len(cash_flows),
            iterations,
            uncertainty,
            results
        )
        
        return {
            'mean_npv': results[0],
            'std_dev': results[1],
            'min_npv': results[2],
            'max_npv': results[3],
            'iterations': iterations,
            'uncertainty': uncertainty
        }
