from typing import Dict, Any, List
import numpy as np
from dataclasses import dataclass

@dataclass
class ValidationRules:
    """Data validation rules for process parameters"""
    min_value: float
    max_value: float
    required: bool = True

class DataValidator:
    """Validates process analysis input data"""
    
    def __init__(self):
        self.rules = {
            'input_mass': ValidationRules(min_value=0.0, max_value=1000.0),
            'output_mass': ValidationRules(min_value=0.0, max_value=1000.0),
            'protein_content': ValidationRules(min_value=0.0, max_value=100.0),
            'moisture_content': ValidationRules(min_value=0.0, max_value=100.0),
            'temperature': ValidationRules(min_value=20.0, max_value=200.0),
            'processing_time': ValidationRules(min_value=0.0, max_value=360.0),
            'particle_size_d10': ValidationRules(min_value=0.0, max_value=1000.0),
            'particle_size_d50': ValidationRules(min_value=0.0, max_value=1000.0),
            'particle_size_d90': ValidationRules(min_value=0.0, max_value=1000.0)
        }
    
    def validate_process_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate process data against defined rules"""
        errors = []
        
        # Check required fields
        for field, rules in self.rules.items():
            if rules.required and field not in data:
                errors.append(f"Missing required field: {field}")
                continue
                
            if field in data:
                value = data[field]
                try:
                    value = float(value)
                    if value < rules.min_value or value > rules.max_value:
                        errors.append(
                            f"{field} must be between {rules.min_value} and {rules.max_value}"
                        )
                except (TypeError, ValueError):
                    errors.append(f"Invalid value for {field}")
        
        return errors
    
    def validate_particle_distribution(
        self,
        d10: float,
        d50: float,
        d90: float
    ) -> List[str]:
        """Validate particle size distribution parameters"""
        errors = []
        
        # Check basic range
        for size, label in [(d10, 'D10'), (d50, 'D50'), (d90, 'D90')]:
            if size < 0:
                errors.append(f"{label} cannot be negative")
        
        # Check distribution logic
        if d10 > d50:
            errors.append("D10 cannot be greater than D50")
        if d50 > d90:
            errors.append("D50 cannot be greater than D90")
        
        return errors
    
    def validate_economic_data(
        self,
        data: Dict[str, float]
    ) -> List[str]:
        """Validate economic analysis input data"""
        errors = []
        
        required_fields = [
            'equipment_cost',
            'installation_factor',
            'maintenance_cost',
            'labor_cost',
            'utility_cost'
        ]
        
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required economic field: {field}")
                continue
            
            value = data[field]
            if not isinstance(value, (int, float)) or value < 0:
                errors.append(f"Invalid value for {field}")
        
        return errors 