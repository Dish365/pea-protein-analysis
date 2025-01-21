from typing import Dict, List, Optional
import numpy as np
from .economic import EconomicAllocator
from .physical import PhysicalAllocator

class HybridAllocator:
    """Hybrid allocation combining economic and physical allocation methods"""
    
    def __init__(self):
        self.economic_allocator = EconomicAllocator()
        self.physical_allocator = PhysicalAllocator()
        self.weighting: Dict[str, float] = {
            'economic': 0.5,
            'physical': 0.5
        }
        
    def set_allocation_weights(self, economic_weight: float, physical_weight: float) -> None:
        """Set weights for combining economic and physical allocation
        
        Args:
            economic_weight: Weight for economic allocation (0-1)
            physical_weight: Weight for physical allocation (0-1)
        """
        if not np.isclose(economic_weight + physical_weight, 1.0):
            raise ValueError("Weights must sum to 1.0")
            
        self.weighting = {
            'economic': economic_weight,
            'physical': physical_weight
        }
        
    def configure_allocation(self, 
                           product_values: Dict[str, float],
                           mass_flows: Dict[str, float]) -> None:
        """Configure both allocation methods
        
        Args:
            product_values: Economic values for products ($/kg)
            mass_flows: Mass flows for products (kg)
        """
        self.economic_allocator.set_product_values(product_values)
        self.physical_allocator.set_mass_flows(mass_flows)
        
    def allocate_impact(self, total_impact: float) -> Dict[str, float]:
        """Allocate impact using weighted combination of methods
        
        Args:
            total_impact: Total environmental impact to be allocated
            
        Returns:
            Dictionary mapping products to their allocated impact
        """
        economic_allocation = self.economic_allocator.allocate_impact(total_impact)
        physical_allocation = self.physical_allocator.allocate_impact(total_impact)
        
        # Combine allocations using weights
        hybrid_allocation = {}
        for product in economic_allocation:
            hybrid_allocation[product] = (
                economic_allocation[product] * self.weighting['economic'] +
                physical_allocation[product] * self.weighting['physical']
            )
            
        return hybrid_allocation 