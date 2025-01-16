from typing import Dict, List, Optional
import numpy as np

class QualityIndicators:
    """Product quality indicators for eco-efficiency analysis"""
    
    def __init__(self):
        self.indicators: Dict[str, float] = {}
        
    def calculate_protein_recovery(self,
                                 recovered_protein: float,
                                 initial_protein: float) -> float:
        """Calculate protein recovery rate
        
        Args:
            recovered_protein: Amount of protein recovered (kg)
            initial_protein: Initial protein content (kg)
        """
        recovery = recovered_protein / initial_protein
        self.indicators['protein_recovery'] = recovery
        return recovery
        
    def calculate_protein_purity(self,
                               protein_content: float,
                               total_mass: float) -> float:
        """Calculate protein purity
        
        Args:
            protein_content: Protein content (kg)
            total_mass: Total product mass (kg)
        """
        purity = protein_content / total_mass
        self.indicators['protein_purity'] = purity
        return purity
        
    def calculate_functional_properties(self,
                                     properties: Dict[str, float],
                                     target_values: Dict[str, float]) -> float:
        """Calculate functional properties score
        
        Args:
            properties: Measured functional properties
            target_values: Target values for properties
        """
        # Calculate average deviation from targets
        deviations = [abs(properties[prop] - target_values[prop])/target_values[prop]
                     for prop in properties]
        quality_score = 1 - (sum(deviations) / len(deviations))
        self.indicators['functional_score'] = quality_score
        return quality_score
        
    def get_indicators(self) -> Dict[str, float]:
        """Get all quality indicators"""
        return self.indicators 