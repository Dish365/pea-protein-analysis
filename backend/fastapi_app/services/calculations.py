from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

class ProcessCalculations:
    """
    Core calculation services for process analysis.
    
    Calculation Categories:
    ---------------------
    1. Mass Balance:
       - Component balances
       - Overall mass balance
       - Yield calculations
    
    2. Energy Balance:
       - Heat transfer
       - Power consumption
       - Energy efficiency
    
    3. Performance Metrics:
       - Process efficiency
       - Quality indicators
       - Cost analysis
    """
    
    def calculate_mass_balance(
        self,
        input_streams: Dict[str, float],
        output_streams: Dict[str, float],
        compositions: Dict[str, Dict[str, float]]
    ) -> Dict[str, float]:
        """
        Calculate mass balance for process streams.
        
        Mass Balance Equations:
        --------------------
        1. Overall Balance:
           Σ(inputs) = Σ(outputs)
        
        2. Component Balance:
           Σ(xᵢ,in * ṁin) = Σ(xᵢ,out * ṁout)
        """
        results = {
            'total_input': sum(input_streams.values()),
            'total_output': sum(output_streams.values()),
            'components': {}
        }
        
        # Calculate component balances
        for component in compositions['input'].keys():
            input_mass = sum(
                flow * compositions['input'].get(component, 0) / 100
                for flow in input_streams.values()
            )
            output_mass = sum(
                flow * compositions['output'].get(component, 0) / 100
                for flow in output_streams.values()
            )
            
            results['components'][component] = {
                'input': input_mass,
                'output': output_mass,
                'recovery': (output_mass / input_mass * 100) if input_mass > 0 else 0
            }
            
        return results
    
    def calculate_energy_balance(
        self,
        process_type: str,
        operating_params: Dict[str, float],
        material_props: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate energy balance for different process types.
        
        Energy Balance:
        -------------
        Q = m * cp * ΔT + ΔH
        where:
        - Q = Total energy
        - m = Mass flow
        - cp = Specific heat
        - ΔT = Temperature change
        - ΔH = Phase change energy
        """
        results = {}
        
        if process_type == 'rf':
            # RF heating calculations
            power = operating_params['power']
            time = operating_params['treatment_time']
            dielectric_factor = material_props['dielectric_constant']
            
            energy_input = power * time * 60  # Convert time to seconds
            effective_power = power * dielectric_factor
            
            results.update({
                'energy_input': energy_input,
                'effective_power': effective_power,
                'energy_efficiency': effective_power / power * 100
            })
            
        elif process_type == 'ir':
            # IR heating calculations
            power_density = operating_params['power_density']
            area = material_props.get('surface_area', 1.0)
            time = operating_params['treatment_time']
            
            energy_input = power_density * area * time * 60
            heat_absorbed = energy_input * material_props.get('absorptivity', 0.9)
            
            results.update({
                'energy_input': energy_input,
                'heat_absorbed': heat_absorbed,
                'energy_efficiency': heat_absorbed / energy_input * 100
            })
            
        return results
    
    def calculate_performance_metrics(
        self,
        process_data: Dict,
        target_values: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate process performance metrics.
        
        Performance Indicators:
        --------------------
        1. Process Efficiency = Actual/Target
        2. Quality Score = Σ(wᵢ * qᵢ)
        3. Cost Effectiveness = Value/Cost
        """
        metrics = {}
        
        # Calculate process efficiency
        for param, target in target_values.items():
            if param in process_data:
                actual = process_data[param]
                efficiency = (actual / target * 100) if target > 0 else 0
                metrics[f'{param}_efficiency'] = efficiency
        
        # Calculate overall performance score
        if metrics:
            metrics['overall_performance'] = np.mean(list(metrics.values()))
        
        return metrics
