from typing import Dict, List, Optional, Literal
from ..allocation.economic import EconomicAllocator
from ..allocation.physical import PhysicalAllocator
from ..allocation.hybrid import HybridAllocator

class AllocationEngine:
    """Service for managing environmental impact allocation"""
    
    def __init__(self):
        self.economic_allocator = EconomicAllocator()
        self.physical_allocator = PhysicalAllocator()
        self.hybrid_allocator = HybridAllocator()
        
    def configure_allocation(self,
                           product_values: Dict[str, float],
                           mass_flows: Dict[str, float],
                           hybrid_weights: Optional[Dict[str, float]] = None) -> None:
        """Configure allocation systems with process data
        
        Args:
            product_values: Economic values for products ($/kg)
            mass_flows: Mass flows for products (kg)
            hybrid_weights: Optional weights for hybrid allocation
        """
        self.economic_allocator.set_product_values(product_values)
        self.physical_allocator.set_mass_flows(mass_flows)
        
        self.hybrid_allocator.configure_allocation(product_values, mass_flows)
        if hybrid_weights:
            self.hybrid_allocator.set_allocation_weights(
                hybrid_weights['economic'],
                hybrid_weights['physical']
            )
            
    def allocate_impacts(self,
                        impacts: Dict[str, float],
                        method: Literal['economic', 'physical', 'hybrid'] = 'hybrid'
                        ) -> Dict[str, Dict[str, float]]:
        """Allocate multiple environmental impacts using specified method
        
        Args:
            impacts: Dictionary mapping impact categories to total values
            method: Allocation method to use
            
        Returns:
            Nested dictionary mapping impact categories to allocated impacts per product
        """
        allocator = {
            'economic': self.economic_allocator,
            'physical': self.physical_allocator,
            'hybrid': self.hybrid_allocator
        }[method]
        
        return {
            impact_category: allocator.allocate_impact(total_impact)
            for impact_category, total_impact in impacts.items()
        }
        
    def get_allocation_factors(self, 
                             method: Literal['economic', 'physical'] = 'economic'
                             ) -> Dict[str, float]:
        """Get allocation factors for specified method
        
        Args:
            method: Allocation method to get factors for
            
        Returns:
            Dictionary mapping products to their allocation factors
        """
        return {
            'economic': self.economic_allocator.get_allocation_factors(),
            'physical': self.physical_allocator.get_allocation_factors()
        }[method] 