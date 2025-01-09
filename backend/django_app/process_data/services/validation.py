from typing import Dict, List, Optional
from ..models.baseline import BaselineProcess
from ..models.rf_treatment import RFTreatmentProcess
from ..models.ir_treatment import IRTreatmentProcess

class ProcessDataValidator:
    """
    Validate process data for different treatment types.
    
    Validation Rules:
    ----------------
    1. Mass Balance:
       Σ(inputs) = Σ(outputs) ± tolerance
    
    2. Component Balance:
       For each component i:
       Σ(xᵢ,in * ṁin) = Σ(xᵢ,out * ṁout) ± tolerance
       where:
       - xᵢ = Mass fraction of component i
       - ṁ = Mass flow rate
    
    3. Protein Content:
       0 < protein% ≤ 100 for all streams
    
    4. Equipment Parameters:
       Each parameter must be within specified ranges
    """
    
    def __init__(self, tolerance: float = 0.02):
        """Initialize validator with mass balance tolerance."""
        self.tolerance = tolerance
        
    def validate_mass_balance(
        self,
        input_streams: Dict[str, float],
        output_streams: Dict[str, float]
    ) -> bool:
        """
        Validate overall mass balance.
        
        Mass Balance Equation:
        |Σ(inputs) - Σ(outputs)| ≤ tolerance * Σ(inputs)
        """
        total_input = sum(input_streams.values())
        total_output = sum(output_streams.values())
        
        return abs(total_input - total_output) <= self.tolerance * total_input
    
    def validate_component_balance(
        self,
        input_compositions: Dict[str, Dict[str, float]],
        output_compositions: Dict[str, Dict[str, float]],
        input_flows: Dict[str, float],
        output_flows: Dict[str, float]
    ) -> Dict[str, bool]:
        """
        Validate component-wise mass balances.
        
        Component Balance:
        For each component i:
        |Σ(xᵢ,in * ṁin) - Σ(xᵢ,out * ṁout)| ≤ tolerance * Σ(xᵢ,in * ṁin)
        """
        results = {}
        components = set()
        
        # Collect all unique components
        for comp in input_compositions.values():
            components.update(comp.keys())
            
        # Check balance for each component
        for component in components:
            input_mass = sum(
                flows * comps.get(component, 0) / 100
                for flows, comps in zip(input_flows.values(), input_compositions.values())
            )
            output_mass = sum(
                flows * comps.get(component, 0) / 100
                for flows, comps in zip(output_flows.values(), output_compositions.values())
            )
            
            results[component] = (
                abs(input_mass - output_mass) <= self.tolerance * input_mass
                if input_mass > 0 else output_mass == 0
            )
            
        return results
    
    def validate_equipment_parameters(
        self,
        process_type: str,
        parameters: Dict[str, float]
    ) -> Dict[str, bool]:
        """
        Validate equipment-specific parameters.
        
        Parameter Ranges:
        ---------------
        Baseline:
        - Air flow: 10-50 m³/h
        - Classifier speed: 1000-5000 rpm
        
        RF Treatment:
        - Power: 0.5-5 kW
        - Frequency: 27.12 MHz
        - Treatment time: 1-10 min
        
        IR Treatment:
        - Power density: 2-10 kW/m²
        - Wavelength: 3-15 μm
        - Treatment time: 1-15 min
        """
        validation_rules = {
            'baseline': {
                'air_flow': (10, 50),
                'classifier_speed': (1000, 5000)
            },
            'rf': {
                'power': (0.5, 5),
                'frequency': (27.12, 27.12),
                'treatment_time': (1, 10)
            },
            'ir': {
                'power_density': (2, 10),
                'wavelength': (3, 15),
                'treatment_time': (1, 15)
            }
        }
        
        if process_type not in validation_rules:
            raise ValueError(f"Unknown process type: {process_type}")
            
        results = {}
        rules = validation_rules[process_type]
        
        for param, value in parameters.items():
            if param in rules:
                min_val, max_val = rules[param]
                results[param] = min_val <= value <= max_val
                
        return results
    
    def validate_process_data(
        self,
        process_type: str,
        data: Dict
    ) -> Dict[str, bool]:
        """
        Perform comprehensive validation of process data.
        
        Validation Steps:
        1. Check mass balance
        2. Validate component balances
        3. Verify equipment parameters
        4. Check protein content ranges
        5. Validate process-specific constraints
        """
        results = {
            'mass_balance': False,
            'component_balance': {},
            'equipment_parameters': {},
            'protein_content': True,
            'process_constraints': True
        }
        
        # Validate mass balance
        results['mass_balance'] = self.validate_mass_balance(
            data['input_streams'],
            data['output_streams']
        )
        
        # Validate component balances
        results['component_balance'] = self.validate_component_balance(
            data['input_compositions'],
            data['output_compositions'],
            data['input_streams'],
            data['output_streams']
        )
        
        # Validate equipment parameters
        results['equipment_parameters'] = self.validate_equipment_parameters(
            process_type,
            data['equipment_parameters']
        )
        
        # Check protein content
        for comps in data['input_compositions'].values():
            if not 0 < comps.get('protein', 0) <= 100:
                results['protein_content'] = False
                break
                
        for comps in data['output_compositions'].values():
            if not 0 < comps.get('protein', 0) <= 100:
                results['protein_content'] = False
                break
        
        return results 