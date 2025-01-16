from typing import Dict, List
import ctypes
from pathlib import Path

# Load Rust library
lib_path = Path(__file__).parent.parent.parent.parent / "backend/rust_modules/target/release/libmonte_carlo.so"
lib = ctypes.CDLL(str(lib_path))

class EconomicIntegrator:
    def __init__(self):
        # Configure Rust function signatures
        self.lib = lib
        self.lib.run_monte_carlo_simulation.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_double,
            ctypes.POINTER(ctypes.c_double)
        ]
        
    def run_monte_carlo_analysis(
        self,
        base_values: List[float],
        iterations: int = 1000,
        uncertainty: float = 0.1
    ) -> Dict[str, float]:
        """Run Monte Carlo simulation using Rust implementation"""
        arr = (ctypes.c_double * len(base_values))(*base_values)
        results = (ctypes.c_double * 4)()  # [mean, std_dev, min, max]
        
        self.lib.run_monte_carlo_simulation(
            arr,
            len(base_values),
            iterations,
            ctypes.c_double(uncertainty),
            results
        )
        
        return {
            "mean": results[0],
            "std_dev": results[1],
            "min_value": results[2],
            "max_value": results[3]
        }
        
    def analyze_economic_sensitivity(
        self,
        base_values: List[float],
        parameters: List[str],
        sensitivity_range: float = 0.2
    ) -> Dict[str, List[Dict[str, float]]]:
        """Perform sensitivity analysis on economic parameters"""
        results = []
        
        for i, param in enumerate(parameters):
            param_results = []
            for factor in [-sensitivity_range, 0, sensitivity_range]:
                modified_values = base_values.copy()
                modified_values[i] *= (1 + factor)
                
                mc_results = self.run_monte_carlo_analysis(modified_values)
                param_results.append({
                    "factor": factor,
                    "value": mc_results["mean"],
                    "std_dev": mc_results["std_dev"]
                })
            results.append({
                "parameter": param,
                "sensitivity": param_results
            })
            
        return {
            "sensitivity_analysis": results
        } 