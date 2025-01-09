from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime

class ProcessHelpers:
    """
    Helper functions for process data analysis.
    
    Categories:
    ----------
    1. Data Validation
    2. Unit Conversions
    3. Statistical Analysis
    4. Data Formatting
    """
    
    @staticmethod
    def validate_numeric_range(
        value: float,
        min_value: float,
        max_value: float,
        param_name: str
    ) -> None:
        """Validate numeric value within range."""
        if not min_value <= value <= max_value:
            raise ValueError(
                f"{param_name} must be between {min_value} and {max_value}"
            )
    
    @staticmethod
    def convert_units(
        value: float,
        from_unit: str,
        to_unit: str
    ) -> float:
        """
        Convert between different units.
        
        Supported Conversions:
        - Temperature (C, F, K)
        - Pressure (bar, kPa, psi)
        - Power (W, kW, HP)
        """
        # Temperature conversions
        temp_conversions = {
            'C_to_K': lambda x: x + 273.15,
            'K_to_C': lambda x: x - 273.15,
            'C_to_F': lambda x: x * 9/5 + 32,
            'F_to_C': lambda x: (x - 32) * 5/9
        }
        
        # Pressure conversions
        pressure_conversions = {
            'bar_to_kPa': lambda x: x * 100,
            'kPa_to_bar': lambda x: x / 100,
            'bar_to_psi': lambda x: x * 14.5038,
            'psi_to_bar': lambda x: x / 14.5038
        }
        
        # Power conversions
        power_conversions = {
            'W_to_kW': lambda x: x / 1000,
            'kW_to_W': lambda x: x * 1000,
            'kW_to_HP': lambda x: x * 1.34102,
            'HP_to_kW': lambda x: x / 1.34102
        }
        
        conversion_key = f"{from_unit}_to_{to_unit}"
        
        conversions = {
            **temp_conversions,
            **pressure_conversions,
            **power_conversions
        }
        
        if conversion_key in conversions:
            return conversions[conversion_key](value)
        else:
            raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")
    
    @staticmethod
    def calculate_statistics(
        data: List[float],
        confidence_level: float = 0.95
    ) -> Dict[str, float]:
        """
        Calculate statistical metrics for process data.
        
        Metrics:
        - Mean
        - Standard deviation
        - Confidence intervals
        - Coefficient of variation
        """
        if not data:
            return {}
            
        data_array = np.array(data)
        n = len(data_array)
        
        mean = np.mean(data_array)
        std_dev = np.std(data_array, ddof=1)
        
        # Calculate confidence interval
        from scipy import stats
        t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
        margin_error = t_value * (std_dev / np.sqrt(n))
        
        return {
            'mean': mean,
            'std_dev': std_dev,
            'cv': (std_dev / mean * 100) if mean != 0 else float('inf'),
            'ci_lower': mean - margin_error,
            'ci_upper': mean + margin_error,
            'n': n
        }
    
    @staticmethod
    def format_process_data(
        data: Dict[str, Any],
        include_timestamps: bool = True
    ) -> Dict[str, Any]:
        """
        Format process data for analysis and reporting.
        
        Formatting Options:
        - Round numeric values
        - Add timestamps
        - Convert units
        - Format strings
        """
        formatted = {}
        
        for key, value in data.items():
            # Format numeric values
            if isinstance(value, (int, float)):
                formatted[key] = round(value, 3)
            # Format lists/arrays
            elif isinstance(value, (list, np.ndarray)):
                formatted[key] = [
                    round(x, 3) if isinstance(x, (int, float)) else x
                    for x in value
                ]
            # Format nested dictionaries
            elif isinstance(value, dict):
                formatted[key] = ProcessHelpers.format_process_data(
                    value,
                    include_timestamps=False
                )
            else:
                formatted[key] = value
        
        # Add timestamp if requested
        if include_timestamps:
            formatted['timestamp'] = datetime.now().isoformat()
        
        return formatted
