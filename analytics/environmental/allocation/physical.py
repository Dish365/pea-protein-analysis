from typing import Dict, List, Optional
import numpy as np

class PhysicalAllocator:
    """Physical allocation of environmental impacts based on mass flows"""
    
    def __init__(self):
        self.allocation_factors: Dict[str, float] = {}
        self.mass_flows: Dict[str, float] = {}
        
    def set_mass_flows(self, flows: Dict[str, float]) -> None:
        """Set mass flows for each product stream
        
        Args:
            flows: Dictionary mapping product names to their mass flow (kg)
        """
        self.mass_flows = flows
        total_mass = sum(flows.values())
        
        # Calculate allocation factors based on mass flows
        self.allocation_factors = {
            product: mass/total_mass 
            for product, mass in flows.items()
        }
        
    def allocate_impact(self, total_impact: float) -> Dict[str, float]:
        """Allocate total environmental impact based on mass flows
        
        Args:
            total_impact: Total environmental impact to be allocated
            
        Returns:
            Dictionary mapping products to their allocated impact
        """
        if not self.allocation_factors:
            raise ValueError("Mass flows must be set before allocation")
            
        return {
            product: factor * total_impact
            for product, factor in self.allocation_factors.items()
        }
        
    def get_allocation_factors(self) -> Dict[str, float]:
        """Get the physical allocation factors"""
        return self.allocation_factors 