from typing import Dict, Any, List, Union
import numpy as np
from scipy import stats

class DataNormalizer:
    """Handles data normalization and standardization"""
    
    def normalize_process_parameters(
        self, 
        data: Dict[str, float],
        method: str = 'minmax'
    ) -> Dict[str, float]:
        """Normalize process parameters using specified method"""
        normalized_data = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if method == 'minmax':
                    # Min-max normalization to [0,1] range
                    min_val = self._get_parameter_min(key)
                    max_val = self._get_parameter_max(key)
                    normalized_data[key] = (value - min_val) / (max_val - min_val)
                elif method == 'zscore':
                    # Z-score normalization
                    mean_val = self._get_parameter_mean(key)
                    std_val = self._get_parameter_std(key)
                    normalized_data[key] = (value - mean_val) / std_val
                else:
                    raise ValueError(f"Unsupported normalization method: {method}")
            else:
                normalized_data[key] = value
                
        return normalized_data
    
    def normalize_particle_distribution(
        self,
        particle_sizes: np.ndarray
    ) -> np.ndarray:
        """Normalize particle size distribution"""
        if len(particle_sizes) == 0:
            raise ValueError("Empty particle size array")
            
        # Log-transform particle sizes (common in particle analysis)
        log_sizes = np.log(particle_sizes)
        
        # Z-score normalization
        normalized_sizes = stats.zscore(log_sizes)
        
        return normalized_sizes
    
    def _get_parameter_min(self, parameter: str) -> float:
        """Get minimum value for parameter based on historical data/domain knowledge"""
        parameter_ranges = {
            'input_mass': 0.0,
            'output_mass': 0.0,
            'protein_content': 0.0,
            'moisture_content': 0.0,
            'temperature': 20.0,  # Minimum processing temperature
            'processing_time': 0.0
        }
        return parameter_ranges.get(parameter, 0.0)
    
    def _get_parameter_max(self, parameter: str) -> float:
        """Get maximum value for parameter based on historical data/domain knowledge"""
        parameter_ranges = {
            'input_mass': 1000.0,  # kg
            'output_mass': 1000.0,  # kg
            'protein_content': 100.0,  # percentage
            'moisture_content': 100.0,  # percentage
            'temperature': 200.0,  # Maximum processing temperature
            'processing_time': 360.0  # minutes
        }
        return parameter_ranges.get(parameter, 1.0)
    
    def _get_parameter_mean(self, parameter: str) -> float:
        """Get mean value for parameter based on historical data"""
        parameter_means = {
            'input_mass': 500.0,
            'output_mass': 450.0,
            'protein_content': 50.0,
            'moisture_content': 12.0,
            'temperature': 80.0,
            'processing_time': 120.0
        }
        return parameter_means.get(parameter, 0.0)
    
    def _get_parameter_std(self, parameter: str) -> float:
        """Get standard deviation for parameter based on historical data"""
        parameter_stds = {
            'input_mass': 100.0,
            'output_mass': 90.0,
            'protein_content': 10.0,
            'moisture_content': 2.0,
            'temperature': 15.0,
            'processing_time': 30.0
        }
        return parameter_stds.get(parameter, 1.0) 