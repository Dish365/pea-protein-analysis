from typing import Dict, Any, Union, List
import numpy as np
import math

def sanitize_float(value: Any) -> float:
    """Convert numpy floats to Python floats and handle NaN/Infinity/complex values"""
    if isinstance(value, complex):
        return abs(value)
    if isinstance(value, (np.floating, float)):
        if math.isnan(value) or math.isinf(value):
            return 0.0
        return float(value)
    return value

def sanitize_dict(d: Union[Dict, List]) -> Union[Dict, List]:
    """Recursively sanitize dictionary or list values"""
    if isinstance(d, list):
        return [sanitize_float(x) if isinstance(x, (np.floating, float)) else 
                sanitize_dict(x) if isinstance(x, (dict, list)) else x 
                for x in d]
    return {
        k: sanitize_dict(v) if isinstance(v, (dict, list)) else
           sanitize_float(v) if isinstance(v, (np.floating, float)) else v
        for k, v in d.items()
    }
