import ctypes
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RustHandler:
    """Handles integration with Rust libraries for economic calculations"""
    
    def __init__(self):
        try:
            self.lib = self._load_rust_library()
            self._configure_functions()
            logger.info("Rust library loaded successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Rust handler: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to initialize Rust handler: {str(e)}")
        
    def _load_rust_library(self) -> ctypes.CDLL:
        """Load the Rust library based on platform"""
        try:
            lib_path = (
                Path(__file__).parent.parent.parent.parent
                / "rust_modules/target/release"
            )
            
            if sys.platform == "win32":
                lib_path = lib_path / "protein_analysis.dll"
            elif sys.platform == "darwin":
                lib_path = lib_path / "libprotein_analysis.dylib"
            else:
                lib_path = lib_path / "libprotein_analysis.so"
            
            logger.debug(f"Attempting to load Rust library from: {lib_path}")
                
            if not lib_path.exists():
                raise FileNotFoundError(
                    f"Rust library not found at {lib_path}. "
                    "Please ensure the library has been built with 'cargo build --release'"
                )
            
            lib = ctypes.CDLL(str(lib_path))
            logger.debug("Rust library loaded successfully")
            return lib
            
        except Exception as e:
            logger.error(f"Failed to load Rust library: {str(e)}", exc_info=True)
            raise
        
    def _configure_functions(self) -> None:
        """Configure Rust function signatures"""
        try:
            # Configure Monte Carlo simulation function
            self.lib.run_economic_monte_carlo.argtypes = [
                ctypes.POINTER(ctypes.c_double),  # base_values
                ctypes.c_size_t,                  # len
                ctypes.c_size_t,                  # iterations
                ctypes.c_double,                  # uncertainty
                ctypes.POINTER(ctypes.c_double),  # results
            ]
            self.lib.run_economic_monte_carlo.restype = None
            logger.debug("Rust functions configured successfully")
            
        except Exception as e:
            logger.error(f"Failed to configure Rust functions: {str(e)}", exc_info=True)
            raise
        
    def run_monte_carlo_simulation(
        self,
        cash_flows: List[float],
        discount_rate: float,
        initial_investment: float,
        iterations: int = 1000,
        uncertainty: float = 0.1
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for NPV analysis using Rust implementation
        
        Args:
            cash_flows: List of projected cash flows
            discount_rate: Annual discount rate
            initial_investment: Initial investment amount
            iterations: Number of Monte Carlo iterations
            uncertainty: Uncertainty factor for cash flow variation
            
        Returns:
            Dictionary containing Monte Carlo simulation results
        """
        try:
            # Convert cash flows to C array
            arr = (ctypes.c_double * len(cash_flows))(*cash_flows)
            results = (ctypes.c_double * 4)()  # [mean, std_dev, min_value, max_value]
            
            # Call Rust function
            self.lib.run_economic_monte_carlo(
                arr,
                len(cash_flows),
                iterations,
                uncertainty,
                results
            )
            
            # Parse results
            return {
                "iterations": iterations,
                "uncertainty": uncertainty,
                "results": {
                    "mean": results[0],
                    "std_dev": results[1],
                    "confidence_interval": [results[2], results[3]]  # min and max values
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Monte Carlo simulation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Monte Carlo simulation failed: {str(e)}")

    def analyze_particle_distribution(
        self,
        particle_sizes: List[float],
        weights: List[float]
    ) -> Dict[str, float]:
        """
        Analyze particle size distribution using Rust implementation
        
        Args:
            particle_sizes: List of particle sizes
            weights: List of weights for each size
            
        Returns:
            Dictionary containing distribution metrics
        """
        try:
            # Convert lists to C arrays
            size_array = (ctypes.c_double * len(particle_sizes))(*particle_sizes)
            weight_array = (ctypes.c_double * len(weights))(*weights)
            
            # Initialize result variables
            d10 = ctypes.c_double()
            d50 = ctypes.c_double()
            d90 = ctypes.c_double()
            mean = ctypes.c_double()
            std_dev = ctypes.c_double()
            
            # Call Rust function
            self.lib.analyze_particle_distribution(
                size_array,
                weight_array,
                len(particle_sizes),
                ctypes.byref(d10),
                ctypes.byref(d50),
                ctypes.byref(d90),
                ctypes.byref(mean),
                ctypes.byref(std_dev)
            )
            
            return {
                "D10": d10.value,
                "D50": d50.value,
                "D90": d90.value,
                "mean": mean.value,
                "std_dev": std_dev.value
            }
            
        except Exception as e:
            logger.error(f"Error in particle size analysis: {str(e)}", exc_info=True)
            raise RuntimeError(f"Particle size analysis failed: {str(e)}") 