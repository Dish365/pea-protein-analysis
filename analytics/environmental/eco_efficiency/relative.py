from typing import Dict, List, Optional
import numpy as np

class RelativeEfficiencyCalculator:
    """Calculate relative eco-efficiency metrics"""
    
    def __init__(self):
        self.efficiency_metrics: Dict[str, float] = {}
        
    def calculate_environmental_efficiency(self,
                                        economic_value: float,
                                        environmental_impact: Dict[str, float]) -> Dict[str, float]:
        """Calculate environmental efficiency metrics
        
        Args:
            economic_value: Economic value generated ($)
            environmental_impact: Environmental impacts by category
        """
        efficiency = {}
        for category, impact in environmental_impact.items():
            if impact > 0:
                efficiency[category] = economic_value / impact
            else:
                efficiency[category] = float('inf')
                
        self.efficiency_metrics.update(efficiency)
        return efficiency
        
    def calculate_resource_efficiency(self,
                                    product_output: float,
                                    resource_input: Dict[str, float]) -> Dict[str, float]:
        """Calculate resource efficiency metrics
        
        Args:
            product_output: Total product output (kg)
            resource_input: Resource inputs by type (kg or kWh)
        """
        efficiency = {}
        for resource, input_amount in resource_input.items():
            if input_amount > 0:
                efficiency[f"{resource}_efficiency"] = product_output / input_amount
            else:
                efficiency[f"{resource}_efficiency"] = float('inf')
                
        self.efficiency_metrics.update(efficiency)
        return efficiency
        
    def calculate_quality_efficiency(self,
                                   quality_score: float,
                                   production_cost: float) -> float:
        """Calculate quality-cost efficiency
        
        Args:
            quality_score: Product quality score (0-1)
            production_cost: Production cost per unit
        """
        if production_cost > 0:
            efficiency = quality_score / production_cost
        else:
            efficiency = float('inf')
            
        self.efficiency_metrics['quality_cost_efficiency'] = efficiency
        return efficiency
        
    def get_efficiency_metrics(self) -> Dict[str, float]:
        """Get all efficiency metrics"""
        return self.efficiency_metrics 