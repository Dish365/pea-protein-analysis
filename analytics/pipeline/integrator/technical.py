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
    calculate_protein_recovery: Any  # Protein recovery calculation
    analyze_particle_distribution: Any  # Particle distribution analysis
    calculate_separation_efficiency: Any  # Separation efficiency calculation

class TechnicalIntegrator:
    """
    Integrates technical analysis components with FastAPI and Rust.
    
    This class coordinates between:
    1. FastAPI endpoints for protein analysis
    2. Rust modules for optimized calculations
    3. Python-based analysis components
    
    The integrator ensures no duplication of logic while maintaining 
    high performance through Rust for computationally intensive operations.
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8001/process/technical"):
        """
        Initialize the technical integrator with API and Rust components.
        
        Args:
            api_base_url: Base URL for FastAPI endpoints
        """
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = api_base_url
        
        # Initialize Rust library
        self.lib = self._load_rust_library()
        self.rust_config = self._configure_rust_functions()
        
        logger.info("TechnicalIntegrator initialized successfully")

    def _load_rust_library(self) -> Any:
        """Load the Rust library based on platform"""
        try:
            # Get the path to the Rust library
            lib_path = Path(__file__).parent.parent.parent.parent / "backend" / "rust_modules" / "target" / "release"
            
            # Use correct extension based on platform
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

            lib = ctypes.CDLL(str(lib_path))
            
            # Verify required functions exist
            required_functions = [
                'calculate_protein_recovery',
                'analyze_particle_distribution',
                'calculate_separation_efficiency'
            ]
            
            for func_name in required_functions:
                if not hasattr(lib, func_name):
                    raise AttributeError(
                        f"Required function '{func_name}' not found in Rust library. "
                        f"Please ensure the library is properly compiled with all required functions."
                    )

            return lib

        except Exception as e:
            logger.error(f"Failed to load Rust library: {str(e)}")
            raise RuntimeError(f"Failed to load Rust library: {str(e)}")

    def _configure_rust_functions(self) -> RustLibConfig:
        """Configure Rust function signatures and return types"""
        # Protein recovery calculation
        self.lib.calculate_protein_recovery.argtypes = [
            ctypes.c_double,  # protein_yield
            ctypes.c_double,  # protein_content
            ctypes.c_double,  # separation_efficiency
        ]
        self.lib.calculate_protein_recovery.restype = ctypes.c_double

        # Particle distribution analysis
        self.lib.analyze_particle_distribution.argtypes = [
            ctypes.POINTER(ctypes.c_double),  # particles
            ctypes.c_size_t,  # len
            ctypes.POINTER(ctypes.c_double),  # d10
            ctypes.POINTER(ctypes.c_double),  # d50
            ctypes.POINTER(ctypes.c_double),  # d90
        ]
        self.lib.analyze_particle_distribution.restype = None

        # Separation efficiency calculation
        self.lib.calculate_separation_efficiency.argtypes = [
            ctypes.c_double,  # input_mass
            ctypes.c_double,  # output_mass
            ctypes.c_double,  # input_concentration 
            ctypes.c_double   # output_concentration
        ]
        self.lib.calculate_separation_efficiency.restype = ctypes.c_double
        
        return RustLibConfig(
            calculate_protein_recovery=self.lib.calculate_protein_recovery,
            analyze_particle_distribution=self.lib.analyze_particle_distribution,
            calculate_separation_efficiency=self.lib.calculate_separation_efficiency
        )

    async def analyze_technical(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate complete technical analysis using FastAPI endpoints and Rust calculations.
        
        Args:
            process_data: Dictionary containing process parameters and measurements
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        try:
            logger.debug(f"Starting technical analysis with data: {process_data}")
            
            # Extract process parameters
            params = self._extract_process_parameters(process_data)
            
            # Parallel execution of analysis tasks
            recovery_task = self.analyze_protein_recovery(params['recovery_params'])
            separation_task = self.analyze_separation_efficiency(params['separation_params'])
            particle_task = self.analyze_particle_size(params['particle_params']) if params['particle_params'] else None
            
            # Gather results
            results = await asyncio.gather(recovery_task, separation_task)
            recovery_results, separation_results = results
            
            # Add particle analysis if available
            particle_results = await particle_task if particle_task else {}
            
            return self._compile_analysis_results(
                recovery_results, 
                separation_results, 
                particle_results,
                params['process_params']
            )
            
        except Exception as e:
            logger.error(f"Technical analysis failed: {str(e)}")
            raise RuntimeError(f"Technical analysis failed: {str(e)}")

    def _extract_process_parameters(self, process_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Extract and organize process parameters for analysis"""
        process_params = process_data.get("process_parameters", {})
        material_props = process_data.get("material_properties", {})
        operating_conds = process_data.get("operating_conditions", {})
        
        recovery_params = {
            "input_mass": process_params.get("feed_rate", 0) * operating_conds.get("processing_time", 0),
            "output_mass": process_params.get("output_mass", 0),
            "initial_protein_content": material_props.get("initial_protein_content", 0),
            "output_protein_content": material_props.get("final_protein_content", 0)
        }
        
        separation_params = {
            "feed_composition": {
                "protein": material_props.get("initial_protein_content", 0),
                "moisture": material_props.get("initial_moisture", 0)
            },
            "product_composition": {
                "protein": material_props.get("final_protein_content", 0),
                "moisture": material_props.get("final_moisture", 0)
            },
            "mass_flow": {
                "input": process_params.get("feed_rate", 0),
                "output": process_params.get("output_rate", 0)
            }
        }
        
        particle_params = None
        if "particle_size" in material_props:
            particle_data = material_props["particle_size"]
            particle_params = {
                "particle_sizes": [
                    particle_data.get("d10", 0),
                    particle_data.get("d50", 0),
                    particle_data.get("d90", 0)
                ]
            }
        
        return {
            "recovery_params": recovery_params,
            "separation_params": separation_params,
            "particle_params": particle_params,
            "process_params": process_params
        }

    async def analyze_protein_recovery(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate protein recovery using FastAPI endpoint and Rust"""
        try:
            # Call FastAPI endpoint
            response = await self.client.post(
                f"{self.api_base_url}/protein-recovery/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Protein recovery API call failed: {response.text}")
                
            # Enhance results with Rust calculation
            api_results = response.json()
            rust_recovery = self.rust_config.calculate_protein_recovery(
                ctypes.c_double(api_results.get('protein_yield', 0.0)),
                ctypes.c_double(process_data.get('initial_protein_content', 0.0)),
                ctypes.c_double(api_results.get('separation_efficiency', 0.0))
            )
            
            api_results['rust_calculated_recovery'] = rust_recovery
            return api_results
            
        except Exception as e:
            logger.error(f"Protein recovery analysis failed: {str(e)}")
            raise RuntimeError(f"Protein recovery analysis failed: {str(e)}")

    async def analyze_separation_efficiency(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate separation efficiency using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/separation-efficiency/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Separation efficiency API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Separation efficiency analysis failed: {str(e)}")
            raise RuntimeError(f"Separation efficiency analysis failed: {str(e)}")

    async def analyze_particle_size(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze particle size distribution using FastAPI endpoint and Rust"""
        try:
            # Call FastAPI endpoint
            response = await self.client.post(
                f"{self.api_base_url}/particle-size/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Particle size API call failed: {response.text}")
                
            # Enhance with Rust calculation
            api_results = response.json()
            rust_results = self._calculate_particle_distribution(process_data['particle_sizes'])
            api_results.update(rust_results)
            
            return api_results
            
        except Exception as e:
            logger.error(f"Particle size analysis failed: {str(e)}")
            raise RuntimeError(f"Particle size analysis failed: {str(e)}")

    def _calculate_particle_distribution(self, particles: List[float]) -> Dict[str, float]:
        """Calculate particle distribution using Rust"""
        arr = (ctypes.c_double * len(particles))(*particles)
        d10 = ctypes.c_double()
        d50 = ctypes.c_double()
        d90 = ctypes.c_double()

        self.rust_config.analyze_particle_distribution(
            arr, 
            len(particles),
            ctypes.byref(d10),
            ctypes.byref(d50),
            ctypes.byref(d90)
        )

        return {
            "rust_d10": d10.value,
            "rust_d50": d50.value,
            "rust_d90": d90.value,
            "rust_distribution_width": (d90.value - d10.value) / d50.value
        }

    def _compile_analysis_results(
        self,
        recovery_results: Dict[str, float],
        separation_results: Dict[str, float],
        particle_results: Dict[str, float],
        process_params: Dict[str, float]
    ) -> Dict[str, Any]:
        """Compile all analysis results into a single response"""
        return {
            "protein_recovery": recovery_results,
            "separation_efficiency": separation_results,
            "particle_analysis": particle_results,
            "process_parameters": {
                "feed_rate_actual": process_params.get("feed_rate", 0),
                "air_flow_actual": process_params.get("air_flow_rate", 0),
                "classifier_efficiency": process_params.get("classifier_speed", 0)
            }
        }
