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

            # Configure allocation functions
            self.lib.calculate_allocation.argtypes = [
                ctypes.POINTER(ctypes.c_double),  # impacts
                ctypes.POINTER(ctypes.c_double),  # values
                ctypes.c_size_t,                  # len
                ctypes.POINTER(ctypes.c_double),  # allocation_factors
            ]
            self.lib.calculate_allocation.restype = ctypes.c_bool

            self.lib.calculate_hybrid_allocation.argtypes = [
                ctypes.POINTER(ctypes.c_double),  # mass_factors
                ctypes.POINTER(ctypes.c_double),  # economic_factors
                ctypes.c_size_t,                  # len
                ctypes.c_double,                  # weight
                ctypes.POINTER(ctypes.c_double),  # results
            ]
            self.lib.calculate_hybrid_allocation.restype = ctypes.c_bool

            # Configure eco-efficiency functions
            self.lib.calculate_efficiency.argtypes = [
                ctypes.c_double,  # economic_value
                ctypes.c_double,  # environmental_impact
            ]
            self.lib.calculate_efficiency.restype = ctypes.c_double

            self.lib.calculate_eco_efficiency_matrix.argtypes = [
                ctypes.POINTER(ctypes.c_double),  # economic_values
                ctypes.POINTER(ctypes.c_double),  # environmental_impacts
                ctypes.c_size_t,                  # len
                ctypes.POINTER(ctypes.c_double),  # results
            ]
            self.lib.calculate_eco_efficiency_matrix.restype = ctypes.c_bool
            
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

    def calculate_allocation_factors(
        self,
        impacts: List[float],
        values: List[float]
    ) -> Dict[str, List[float]]:
        """
        Calculate allocation factors and allocated impacts using Rust implementation
        
        Args:
            impacts: List of environmental impacts
            values: List of economic/physical values for allocation
            
        Returns:
            Dictionary containing allocation factors and allocated impacts
        """
        try:
            if len(impacts) != len(values):
                raise ValueError("Impacts and values lists must have the same length")

            # Convert lists to C arrays
            impacts_array = (ctypes.c_double * len(impacts))(*impacts)
            values_array = (ctypes.c_double * len(values))(*values)
            results_array = (ctypes.c_double * len(impacts))()

            # Call Rust function
            success = self.lib.calculate_allocation(
                impacts_array,
                values_array,
                len(impacts),
                results_array
            )

            if not success:
                raise RuntimeError("Allocation calculation failed in Rust")

            return {
                "allocation_factors": [results_array[i] / impacts[i] if impacts[i] != 0 else 0 
                                     for i in range(len(impacts))],
                "allocated_impacts": [results_array[i] for i in range(len(impacts))]
            }

        except Exception as e:
            logger.error(f"Error in allocation calculation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Allocation calculation failed: {str(e)}")

    def calculate_hybrid_allocation_factors(
        self,
        mass_factors: List[float],
        economic_factors: List[float],
        weight: float
    ) -> List[float]:
        """
        Calculate hybrid allocation factors using Rust implementation
        
        Args:
            mass_factors: List of physical allocation factors
            economic_factors: List of economic allocation factors
            weight: Weight for physical allocation (1-weight for economic)
            
        Returns:
            List of hybrid allocation factors
        """
        try:
            if len(mass_factors) != len(economic_factors):
                raise ValueError("Mass and economic factors must have the same length")

            # Convert lists to C arrays
            mass_array = (ctypes.c_double * len(mass_factors))(*mass_factors)
            economic_array = (ctypes.c_double * len(economic_factors))(*economic_factors)
            results_array = (ctypes.c_double * len(mass_factors))()

            # Call Rust function
            success = self.lib.calculate_hybrid_allocation(
                mass_array,
                economic_array,
                len(mass_factors),
                weight,
                results_array
            )

            if not success:
                raise RuntimeError("Hybrid allocation calculation failed in Rust")

            return [results_array[i] for i in range(len(mass_factors))]

        except Exception as e:
            logger.error(f"Error in hybrid allocation calculation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Hybrid allocation calculation failed: {str(e)}")

    def calculate_eco_efficiency_matrix(
        self,
        economic_values: List[float],
        environmental_impacts: List[float]
    ) -> List[float]:
        """
        Calculate eco-efficiency matrix using Rust implementation
        
        Args:
            economic_values: List of economic values (NPV, profit, etc.)
            environmental_impacts: List of environmental impacts (GWP, HCT, etc.)
            
        Returns:
            List of eco-efficiency values
        """
        try:
            # Convert lists to C arrays
            values_array = (ctypes.c_double * len(economic_values))(*economic_values)
            impacts_array = (ctypes.c_double * len(environmental_impacts))(*environmental_impacts)
            results_array = (ctypes.c_double * len(economic_values))()

            # Call Rust function
            success = self.lib.calculate_eco_efficiency_matrix(
                values_array,
                impacts_array,
                len(economic_values),
                results_array
            )

            if not success:
                raise RuntimeError("Eco-efficiency matrix calculation failed in Rust")

            return [results_array[i] for i in range(len(economic_values))]

        except Exception as e:
            logger.error(f"Error in eco-efficiency matrix calculation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Eco-efficiency matrix calculation failed: {str(e)}")

    def calculate_efficiency(
        self,
        economic_value: float,
        environmental_impact: float
    ) -> float:
        """
        Calculate single eco-efficiency value using Rust implementation
        
        Args:
            economic_value: Economic value (e.g., NPV)
            environmental_impact: Environmental impact value
            
        Returns:
            Eco-efficiency value
        """
        try:
            result = self.lib.calculate_efficiency(
                ctypes.c_double(economic_value),
                ctypes.c_double(environmental_impact)
            )
            
            return float(result)

        except Exception as e:
            logger.error(f"Error in eco-efficiency calculation: {str(e)}", exc_info=True)
            raise RuntimeError(f"Eco-efficiency calculation failed: {str(e)}") 