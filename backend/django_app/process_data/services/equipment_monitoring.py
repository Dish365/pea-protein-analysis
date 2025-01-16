from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass

@dataclass
class OperatingRange:
    """Define normal operating ranges for equipment parameters."""
    min_value: float
    max_value: float
    warning_threshold: float  # Percentage of range for warning
    units: str

class EquipmentMonitor:
    """
    Monitor and analyze equipment performance and operating conditions.
    
    Monitoring Categories:
    --------------------
    1. Operating Parameters:
       - Real-time parameter tracking
       - Range validation
       - Deviation detection
    
    2. Performance Metrics:
       - Energy efficiency
       - Throughput
       - Utilization rate
    
    3. Maintenance Indicators:
       - Parameter drift analysis
       - Anomaly detection
       - Preventive maintenance scheduling
    
    Mathematical Background:
    ----------------------
    1. Deviation Score:
       DS = |x - μ|/σ
       where:
       - x = Current value
       - μ = Mean value
       - σ = Standard deviation
    
    2. Energy Efficiency:
       EE = Output/Energy_Input
    
    3. Equipment Reliability:
       R(t) = e^(-λt)
       where:
       - λ = Failure rate
       - t = Operating time
    """
    
    def __init__(self):
        # Define operating ranges for different equipment types
        self.operating_ranges = {
            'classifier': {
                'speed': OperatingRange(1000, 5000, 0.1, 'rpm'),
                'air_flow': OperatingRange(10, 50, 0.15, 'm³/h'),
                'power': OperatingRange(0.5, 5, 0.2, 'kW')
            },
            'rf_generator': {
                'power': OperatingRange(0.5, 5, 0.1, 'kW'),
                'frequency': OperatingRange(27.12, 27.12, 0.01, 'MHz'),
                'temperature': OperatingRange(20, 80, 0.15, '°C')
            },
            'ir_heater': {
                'power_density': OperatingRange(2, 10, 0.1, 'kW/m²'),
                'surface_temp': OperatingRange(30, 150, 0.15, '°C'),
                'wavelength': OperatingRange(3, 15, 0.2, 'μm')
            }
        }
        
        self.monitoring_data = {
            'parameters': [],
            'performance': [],
            'maintenance': []
        }
        
    def monitor_parameters(
        self,
        equipment_type: str,
        parameters: Dict[str, float],
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Monitor equipment operating parameters and detect deviations.
        
        Algorithm:
        1. Validate parameters against operating ranges
        2. Calculate deviation scores
        3. Generate warnings for out-of-range values
        4. Track parameter trends
        
        Returns:
            Dict containing status and warnings for each parameter
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        if equipment_type not in self.operating_ranges:
            raise ValueError(f"Unknown equipment type: {equipment_type}")
            
        results = {}
        ranges = self.operating_ranges[equipment_type]
        
        for param, value in parameters.items():
            if param in ranges:
                range_obj = ranges[param]
                
                # Calculate percentage within range
                total_range = range_obj.max_value - range_obj.min_value
                position = (value - range_obj.min_value) / total_range
                
                # Calculate deviation from center
                center = (range_obj.max_value + range_obj.min_value) / 2
                deviation = abs(value - center) / (total_range / 2)
                
                # Determine status
                status = 'normal'
                if value < range_obj.min_value or value > range_obj.max_value:
                    status = 'critical'
                elif deviation > (1 - range_obj.warning_threshold):
                    status = 'warning'
                
                results[param] = {
                    'value': value,
                    'status': status,
                    'deviation': deviation,
                    'units': range_obj.units
                }
                
        # Record monitoring data
        self.monitoring_data['parameters'].append({
            'equipment_type': equipment_type,
            'parameters': parameters.copy(),
            'results': results.copy(),
            'timestamp': timestamp
        })
        
        return results
    
    def calculate_performance_metrics(
        self,
        equipment_type: str,
        throughput: float,
        energy_consumption: float,
        operating_time: float
    ) -> Dict[str, float]:
        """
        Calculate equipment performance metrics.
        
        Metrics:
        1. Energy Efficiency = Throughput/Energy
        2. Utilization Rate = Operating Time/Total Time
        3. Specific Energy Consumption = Energy/Throughput
        
        Args:
            throughput: Material processed (kg/h)
            energy_consumption: Energy used (kWh)
            operating_time: Hours of operation
        """
        total_time = 24.0  # Hours per day
        
        metrics = {
            'energy_efficiency': throughput / energy_consumption if energy_consumption > 0 else 0,
            'utilization_rate': (operating_time / total_time) * 100,
            'specific_energy': energy_consumption / throughput if throughput > 0 else float('inf')
        }
        
        self.monitoring_data['performance'].append({
            'equipment_type': equipment_type,
            'metrics': metrics.copy(),
            'timestamp': datetime.now()
        })
        
        return metrics
    
    def analyze_maintenance_indicators(
        self,
        equipment_type: str,
        operating_hours: float,
        parameter_history: List[Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Analyze maintenance indicators and predict maintenance needs.
        
        Indicators:
        1. Parameter Drift = Δx/Δt
        2. Reliability = e^(-λt)
        3. Maintenance Priority Score
        
        Returns:
            Dict containing maintenance indicators and recommendations
        """
        # Define failure rates for different equipment types
        failure_rates = {
            'classifier': 0.0001,
            'rf_generator': 0.0002,
            'ir_heater': 0.00015
        }
        
        # Calculate reliability
        λ = failure_rates.get(equipment_type, 0.0001)
        reliability = np.exp(-λ * operating_hours)
        
        # Calculate parameter drift
        if len(parameter_history) >= 2:
            drifts = {}
            for param in parameter_history[0].keys():
                values = [record[param] for record in parameter_history]
                drift = (values[-1] - values[0]) / len(values)
                drifts[param] = drift
        else:
            drifts = {'insufficient_data': 0.0}
        
        # Calculate maintenance priority score
        priority_score = (1 - reliability) * max(abs(d) for d in drifts.values())
        
        results = {
            'reliability': reliability,
            'parameter_drifts': drifts,
            'priority_score': priority_score,
            'maintenance_recommended': priority_score > 0.7
        }
        
        self.monitoring_data['maintenance'].append({
            'equipment_type': equipment_type,
            'indicators': results.copy(),
            'timestamp': datetime.now()
        })
        
        return results 