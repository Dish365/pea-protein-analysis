from typing import Dict, List, Optional
import numpy as np

class EconomicAllocator:
    """Economic allocation of environmental impacts based on product value"""
    
    def __init__(self):
        self.allocation_factors: Dict[str, float] = {}
        self.product_values: Dict[str, float] = {}
        
    def set_product_values(self, values: Dict[str, float]) -> None:
        """Set economic values for each product stream
        
        Args:
            values: Dictionary mapping product names to their economic value ($/kg)
        """
        self.product_values = values
        total_value = sum(values.values())
        
        # Calculate allocation factors based on economic value
        self.allocation_factors = {
            product: value/total_value 
            for product, value in values.items()
        }
        
    def allocate_impact(self, total_impact: float) -> Dict[str, float]:
        """Allocate total environmental impact based on economic value
        
        Args:
            total_impact: Total environmental impact to be allocated
            
        Returns:
            Dictionary mapping products to their allocated impact
        """
        if not self.allocation_factors:
            raise ValueError("Product values must be set before allocation")
            
        return {
            product: factor * total_impact
            for product, factor in self.allocation_factors.items()
        }
        
    def get_allocation_factors(self) -> Dict[str, float]:
        """Get the economic allocation factors"""
        return self.allocation_factors 