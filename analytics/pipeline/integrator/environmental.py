from typing import Dict, List, Optional, Any
import ctypes
import httpx
import asyncio
from pathlib import Path
import os
import sys
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RustLibConfig:
    """Configuration for Rust library functions"""
    matrix_multiply: Any  # Matrix multiplication for impact calculations
    calculate_allocation: Any  # Impact allocation calculations
    calculate_efficiency: Any  # Efficiency metric calculations
    calculate_eco_efficiency_matrix: Any  # Matrix of eco-efficiency indicators

class EnvironmentalIntegrator:
    """
    Integrates environmental analysis components with FastAPI and Rust.
    
    This class coordinates between:
    1. FastAPI endpoints for environmental analysis
    2. Rust modules for optimized matrix calculations
    3. Python-based environmental analysis components
    
    The integrator ensures no duplication of logic while maintaining 
    high performance through Rust for computationally intensive operations.
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8001/environmental"):
        """
        Initialize the environmental integrator with API and Rust components.
        
        Args:
            api_base_url: Base URL for FastAPI endpoints
        """
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = api_base_url
        
        # Initialize Rust library
        self.lib = self._load_rust_library()
        self.rust_config = self._configure_rust_functions()
        
        logger.info("EnvironmentalIntegrator initialized successfully")

    def _load_rust_library(self) -> Any:
        """Load the Rust library based on platform"""
        lib_path = Path(__file__).parent.parent.parent.parent / "backend" / "rust_modules" / "target" / "release"
        
        if sys.platform == "win32":
            lib_path = lib_path / "protein_analysis.dll"
        elif sys.platform == "darwin":
            lib_path = lib_path / "libprotein_analysis.dylib"
        else:
            lib_path = lib_path / "libprotein_analysis.so"

        if not lib_path.exists():
            raise FileNotFoundError(
                f"Rust library not found at {lib_path}. "
                "Please ensure the library has been built with 'cargo build --release'"
            )

        return ctypes.CDLL(str(lib_path))

    def _configure_rust_functions(self) -> RustLibConfig:
        """Configure Rust function signatures and return types"""
        # Matrix multiplication for impact calculations
        self.lib.matrix_multiply.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t,
        ]
        self.lib.matrix_multiply.restype = None

        # Impact allocation calculation
        self.lib.calculate_allocation.argtypes = [
            ctypes.POINTER(ctypes.c_double),  # impacts
            ctypes.POINTER(ctypes.c_double),  # values
            ctypes.c_size_t,                  # len
            ctypes.POINTER(ctypes.c_double),  # allocation_factors
        ]
        self.lib.calculate_allocation.restype = ctypes.c_bool

        # Efficiency calculation
        self.lib.calculate_efficiency.argtypes = [
            ctypes.c_double,  # economic_value
            ctypes.c_double,  # environmental_impact
        ]
        self.lib.calculate_efficiency.restype = ctypes.c_double

        # Add eco-efficiency matrix calculation
        self.lib.calculate_eco_efficiency_matrix.argtypes = [
            ctypes.POINTER(ctypes.c_double),  # economic_values
            ctypes.POINTER(ctypes.c_double),  # environmental_impacts
            ctypes.c_size_t,                  # len
            ctypes.POINTER(ctypes.c_double),  # results
        ]
        self.lib.calculate_eco_efficiency_matrix.restype = ctypes.c_bool
        
        return RustLibConfig(
            matrix_multiply=self.lib.matrix_multiply,
            calculate_allocation=self.lib.calculate_allocation,
            calculate_efficiency=self.lib.calculate_efficiency,
            calculate_eco_efficiency_matrix=self.lib.calculate_eco_efficiency_matrix
        )

    async def analyze_environmental_impacts(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate complete environmental impact analysis using FastAPI endpoints and Rust calculations.
        
        Args:
            process_data: Dictionary containing process parameters and measurements
            
        Returns:
            Dictionary containing comprehensive environmental analysis results
        """
        try:
            logger.debug(f"Starting environmental analysis with data: {process_data}")
            
            # Extract process parameters
            params = self._extract_process_parameters(process_data)
            
            # Parallel execution of analysis tasks
            impact_task = self.calculate_impacts(params['impact_params'])
            allocation_task = self.allocate_impacts(params['allocation_params'])
            efficiency_task = self.calculate_efficiency(params['efficiency_params'])
            
            # Gather results
            results = await asyncio.gather(impact_task, allocation_task, efficiency_task)
            impact_results, allocation_results, efficiency_results = results
            
            return self._compile_analysis_results(
                impact_results,
                allocation_results,
                efficiency_results
            )
            
        except Exception as e:
            logger.error(f"Environmental analysis failed: {str(e)}")
            raise RuntimeError(f"Environmental analysis failed: {str(e)}")

    def _extract_process_parameters(self, process_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Extract and organize process parameters for analysis"""
        impact_params = {
            'electricity_kwh': process_data.get('electricity_kwh', 0),
            'water_kg': process_data.get('water_kg', 0),
            'transport_ton_km': process_data.get('transport_ton_km', 0),
            'product_kg': process_data.get('product_kg', 0),
            'equipment_kg': process_data.get('equipment_kg', 0),
            'cooling_kwh': process_data.get('cooling_kwh', 0),
            'waste_kg': process_data.get('waste_kg', 0)
        }
        
        allocation_params = {
            'impacts': process_data.get('impacts', {}),
            'product_values': process_data.get('product_values', {}),
            'mass_flows': process_data.get('mass_flows', {}),
            'method': process_data.get('allocation_method', 'hybrid'),
            'hybrid_weights': process_data.get('hybrid_weights')
        }
        
        efficiency_params = {
            'economic_data': process_data.get('economic_data', {}),
            'quality_data': process_data.get('quality_data', {}),
            'environmental_impacts': process_data.get('environmental_impacts', {}),
            'resource_inputs': process_data.get('resource_inputs', {})
        }
        
        return {
            'impact_params': impact_params,
            'allocation_params': allocation_params,
            'efficiency_params': efficiency_params
        }

    async def calculate_impacts(self, process_data: Dict[str, float]) -> Dict[str, Any]:
        """Calculate environmental impacts using FastAPI endpoint and Rust"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/calculate-impacts",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Impact calculation API call failed: {response.text}")
            
            # Enhance results with Rust matrix calculations
            api_results = response.json()
            impact_matrix = self._prepare_impact_matrix(process_data)
            coefficient_matrix = self._prepare_coefficient_matrix()
            
            rust_results = self._matrix_multiply(coefficient_matrix, impact_matrix)
            api_results['impacts'].update({
                'rust_calculated_impacts': rust_results
            })
            
            return api_results
            
        except Exception as e:
            logger.error(f"Impact calculation failed: {str(e)}")
            raise RuntimeError(f"Impact calculation failed: {str(e)}")

    async def allocate_impacts(self, allocation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate environmental impacts using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/allocate-impacts",
                json=allocation_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Impact allocation API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Impact allocation failed: {str(e)}")
            raise RuntimeError(f"Impact allocation failed: {str(e)}")

    async def calculate_efficiency(self, efficiency_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate eco-efficiency metrics using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/calculate-efficiency",
                json=efficiency_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Efficiency calculation API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Efficiency calculation failed: {str(e)}")
            raise RuntimeError(f"Efficiency calculation failed: {str(e)}")

    def _prepare_impact_matrix(self, process_data: Dict[str, float]) -> List[List[float]]:
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
        
        self.rust_config.matrix_multiply(a_arr, b_arr, result_arr, m, n, p)
        
        return [[result_arr[i * p + j] for j in range(p)] for i in range(m)]

    def _prepare_matrix(self, data: List[List[float]], m: int, n: int) -> ctypes.Array:
        """Convert Python matrix to C array"""
        flat_data = [item for sublist in data for item in sublist]
        return (ctypes.c_double * (m * n))(*flat_data)

    def _compile_analysis_results(
        self,
        impact_results: Dict[str, Any],
        allocation_results: Dict[str, Any],
        efficiency_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile all analysis results into a single response"""
        return {
            'impact_assessment': impact_results,
            'allocation_results': allocation_results,
            'eco_efficiency': efficiency_results
        }

