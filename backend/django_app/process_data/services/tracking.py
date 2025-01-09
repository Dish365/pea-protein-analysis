from typing import Dict, List, Optional
from datetime import datetime
import numpy as np

class ProcessTracker:
    """
    Track and monitor process parameters and performance metrics.
    
    Tracking Categories:
    ------------------
    1. Mass Flow Tracking:
       - Input/output mass flows
       - Component mass balances
       - Yield tracking
    
    2. Equipment Monitoring:
       - Operating parameters
       - Performance metrics
       - Energy consumption
    
    3. Quality Metrics:
       - Protein content
       - Particle size distribution
       - Separation efficiency
    """
    
    def __init__(self):
        self.tracking_data = {
            'mass_flows': [],
            'equipment_parameters': [],
            'quality_metrics': [],
            'timestamps': []
        }
        
    def record_mass_flows(
        self,
        input_flows: Dict[str, float],
        output_flows: Dict[str, float],
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record mass flow measurements.
        
        Data Structure:
        {
            'inputs': {stream_name: flow_rate},
            'outputs': {stream_name: flow_rate},
            'timestamp': datetime
        }
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.tracking_data['mass_flows'].append({
            'inputs': input_flows.copy(),
            'outputs': output_flows.copy(),
            'timestamp': timestamp
        })
        
    def record_equipment_parameters(
        self,
        parameters: Dict[str, float],
        equipment_id: str,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record equipment operating parameters.
        
        Data Structure:
        {
            'equipment_id': str,
            'parameters': {param_name: value},
            'timestamp': datetime
        }
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.tracking_data['equipment_parameters'].append({
            'equipment_id': equipment_id,
            'parameters': parameters.copy(),
            'timestamp': timestamp
        })
        
    def record_quality_metrics(
        self,
        metrics: Dict[str, float],
        stream_id: str,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record quality metrics measurements.
        
        Data Structure:
        {
            'stream_id': str,
            'metrics': {metric_name: value},
            'timestamp': datetime
        }
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        self.tracking_data['quality_metrics'].append({
            'stream_id': stream_id,
            'metrics': metrics.copy(),
            'timestamp': timestamp
        })
        
    def analyze_trends(
        self,
        metric_type: str,
        parameter: str,
        time_window: Optional[tuple] = None
    ) -> Dict[str, float]:
        """
        Analyze trends in tracked parameters.
        
        Statistical Analysis:
        -------------------
        1. Moving Average:
           MA = Σ(xᵢ)/n for i in window
        
        2. Trend Analysis:
           slope = Σ((t - t̄)(x - x̄)) / Σ((t - t̄)²)
        
        Returns:
            Dict containing statistical metrics
        """
        if metric_type not in self.tracking_data:
            raise ValueError(f"Unknown metric type: {metric_type}")
            
        # Filter data by time window if specified
        data = self.tracking_data[metric_type]
        if time_window:
            start, end = time_window
            data = [
                d for d in data
                if start <= d['timestamp'] <= end
            ]
            
        # Extract values for the specified parameter
        values = []
        timestamps = []
        
        for entry in data:
            if metric_type == 'equipment_parameters':
                if parameter in entry['parameters']:
                    values.append(entry['parameters'][parameter])
                    timestamps.append(entry['timestamp'].timestamp())
            elif metric_type == 'quality_metrics':
                if parameter in entry['metrics']:
                    values.append(entry['metrics'][parameter])
                    timestamps.append(entry['timestamp'].timestamp())
                    
        if not values:
            return {}
            
        # Calculate statistics
        values = np.array(values)
        timestamps = np.array(timestamps)
        
        # Calculate trend (slope)
        t_mean = np.mean(timestamps)
        v_mean = np.mean(values)
        slope = np.sum((timestamps - t_mean) * (values - v_mean)) / np.sum((timestamps - t_mean)**2)
        
        return {
            'mean': float(np.mean(values)),
            'std_dev': float(np.std(values)),
            'trend': float(slope),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'range': float(np.ptp(values))
        } 