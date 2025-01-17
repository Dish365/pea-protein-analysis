from typing import Dict, List, Optional, Any
import ctypes
from pathlib import Path
import httpx
import asyncio

from analytics.environmental.services.impact_calculator import ImpactCalculator
from analytics.environmental.services.efficiency_calculator import EfficiencyCalculator
from analytics.environmental.services.allocation_engine import AllocationEngine

class EnvironmentalIntegrator:
    """Integrates environmental analysis components with FastAPI and Rust"""
    
    def __init__(self):
        # Initialize service components
        self.impact_calculator = ImpactCalculator()
        self.efficiency_calculator = EfficiencyCalculator()
        self.allocation_engine = AllocationEngine()
        
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = "http://localhost:8000/environmental"
        
        # Load Rust library
        lib_path = (
            Path(__file__).parent.parent.parent.parent
            / "backend/rust_modules/target/release/libmatrix_ops.so"
        )
        self.lib = ctypes.CDLL(str(lib_path))
        self._configure_rust_functions()

    def _configure_rust_functions(self) -> None:
        """Configure Rust function signatures"""
        self.lib.matrix_multiply.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
        ]
        self.lib.matrix_multiply.restype = None

    async def analyze_environmental_impacts(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate complete environmental impact analysis"""
        try:
            # Calculate impacts using Rust-accelerated calculations
            impact_results = await self.calculate_impacts(process_data)
            
            # Perform impact allocation
            allocation_results = await self.allocate_impacts(
                impacts=impact_results['impacts'],
                product_values=process_data.get('product_values', {}),
                mass_flows=process_data.get('mass_flows', {}),
                method=process_data.get('allocation_method', 'hybrid')
            )
            
            # Calculate eco-efficiency metrics
            efficiency_results = await self.calculate_efficiency(
                economic_data=process_data.get('economic_data', {}),
                quality_data=process_data.get('quality_data', {}),
                environmental_impacts=impact_results['impacts'],
                resource_inputs=process_data.get('resource_inputs', {})
            )
            
            return {
                'impact_assessment': impact_results,
                'allocation_results': allocation_results,
                'eco_efficiency': efficiency_results
            }
            
        except Exception as e:
            raise RuntimeError(f"Environmental analysis failed: {str(e)}")

    async def calculate_impacts(self, process_data: Dict[str, float]) -> Dict[str, Any]:
        """Calculate environmental impacts using Rust for matrix operations"""
        try:
            # Prepare impact matrices using Rust
            impact_factors = self._prepare_impact_factors(process_data)
            coefficient_matrix = self._prepare_coefficient_matrix()
            
            # Calculate impacts using Rust matrix multiplication
            impact_results = self._matrix_multiply(coefficient_matrix, impact_factors)
            
            impacts = {
                'gwp': impact_results[0][0],
                'hct': impact_results[1][0],
                'frs': impact_results[2][0]
            }
            
            # Get process contributions from impact calculator
            process_contributions = self.impact_calculator.get_process_contributions()
            
            return {
                'impacts': impacts,
                'process_contributions': process_contributions
            }
            
        except Exception as e:
            raise RuntimeError(f"Impact calculation failed: {str(e)}")

    async def allocate_impacts(self,
                             impacts: Dict[str, float],
                             product_values: Dict[str, float],
                             mass_flows: Dict[str, float],
                             method: str = 'hybrid',
                             hybrid_weights: Optional[Dict[str, float]] = None) -> Dict[str, Dict[str, float]]:
        """Allocate environmental impacts using FastAPI endpoint"""
        try:
            # Configure allocation engine
            self.allocation_engine.configure_allocation(
                product_values=product_values,
                mass_flows=mass_flows,
                hybrid_weights=hybrid_weights
            )
            
            # Perform allocation using FastAPI endpoint
            response = await self.client.post(
                f"{self.api_base_url}/allocation/calculate",
                json={
                    'impacts': impacts,
                    'product_values': product_values,
                    'mass_flows': mass_flows,
                    'method': method,
                    'hybrid_weights': hybrid_weights
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Allocation API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"Impact allocation failed: {str(e)}")

    async def calculate_efficiency(self,
                                 economic_data: Dict[str, float],
                                 quality_data: Dict[str, float],
                                 environmental_impacts: Dict[str, float],
                                 resource_inputs: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Calculate eco-efficiency metrics using FastAPI endpoint"""
        try:
            # Calculate efficiency metrics using FastAPI endpoint
            response = await self.client.post(
                f"{self.api_base_url}/efficiency/calculate",
                json={
                    'economic_data': economic_data,
                    'quality_data': quality_data,
                    'environmental_impacts': environmental_impacts,
                    'resource_inputs': resource_inputs
                }
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Efficiency API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise RuntimeError(f"Efficiency calculation failed: {str(e)}")

    def _prepare_impact_factors(self, process_data: Dict[str, float]) -> List[List[float]]:
        """Prepare impact factor matrix from process data"""
        return [
            [process_data.get('electricity_kwh', 0)],
            [process_data.get('water_kg', 0)],
            [process_data.get('transport_ton_km', 0)]
        ]

    def _prepare_coefficient_matrix(self) -> List[List[float]]:
        """Prepare environmental impact coefficient matrix"""
        return [
            [0.5, 0.001, 0.1],      # GWP factors
            [2.3e-8, 1.5e-9, 5.0e-9], # HCT factors
            [0.2, 0.0, 0.05]        # FRS factors
        ]

    def _matrix_multiply(self, a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
        """Multiply matrices using Rust"""
        m, n = len(a), len(a[0])
        p = len(b[0])
        
        a_arr = self._prepare_matrix(a, m, n)
        b_arr = self._prepare_matrix(b, n, p)
        result_arr = (ctypes.c_double * (m * p))()
        
        self.lib.matrix_multiply(a_arr, b_arr, result_arr, m, n, p)
        
        return [[result_arr[i * p + j] for j in range(p)] for i in range(m)]

    def _prepare_matrix(self, data: List[List[float]], m: int, n: int) -> ctypes.Array:
        """Convert Python matrix to C array"""
        flat_data = [item for sublist in data for item in sublist]
        return (ctypes.c_double * (m * n))(*flat_data)

