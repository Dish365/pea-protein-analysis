from typing import Dict, Any, List
import numpy as np
import pandas as pd

class DataCleaner:
    """Handles data cleaning and validation for process analysis inputs"""
    
    def __init__(self):
        self.valid_process_types = ['baseline', 'rf_treatment', 'ir_treatment']
        
    def clean_process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate process input data"""
        cleaned_data = {}
        
        # Validate process type
        if 'process_type' not in data:
            raise ValueError("Process type is required")
        
        process_type = data['process_type'].lower()
        if process_type not in self.valid_process_types:
            raise ValueError(f"Invalid process type. Must be one of {self.valid_process_types}")
        
        cleaned_data['process_type'] = process_type
        
        # Clean numerical values
        numerical_fields = [
            'input_mass', 'output_mass', 'protein_content',
            'moisture_content', 'temperature', 'processing_time'
        ]
        
        for field in numerical_fields:
            if field in data:
                try:
                    cleaned_data[field] = float(data[field])
                    if cleaned_data[field] < 0:
                        raise ValueError(f"{field} cannot be negative")
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid value for {field}")
        
        return cleaned_data
    
    def clean_particle_data(self, particle_sizes: List[float]) -> np.ndarray:
        """Clean and validate particle size distribution data"""
        try:
            cleaned_sizes = np.array(particle_sizes, dtype=float)
            if np.any(cleaned_sizes < 0):
                raise ValueError("Particle sizes cannot be negative")
            return cleaned_sizes
        except (TypeError, ValueError):
            raise ValueError("Invalid particle size data") 