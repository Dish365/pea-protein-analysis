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
        self._hybrid_weights = {'economic': 0.6, 'physical': 0.4}  # Updated based on research
        self._rf_allocation_factors = {
            'economic': 0.449,  # RF Treatment economic allocation factor
            'physical': 0.219   # RF Treatment physical allocation factor
        }
        
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
        # Validate mass flows against RF research data
        total_mass = sum(mass_flows.values())
        protein_yield = mass_flows.get('protein_concentrate', 0) / total_mass if total_mass > 0 else 0
        
        # Check if protein yield is within expected range for RF treatment (21.9% ± 2%)
        if not (0.199 <= protein_yield <= 0.239):
            print(f"Warning: Protein yield {protein_yield:.3f} is outside expected range for RF treatment (0.199-0.239)")
        
        self.economic_allocator.set_product_values(product_values)
        self.physical_allocator.set_mass_flows(mass_flows)
        
        self.hybrid_allocator.configure_allocation(product_values, mass_flows)
        if hybrid_weights:
            self._hybrid_weights = hybrid_weights
            self.hybrid_allocator.set_allocation_weights(
                hybrid_weights['economic'],
                hybrid_weights['physical']
            )
            
    def allocate_impacts(self,
                        impacts: Dict[str, float],
                        method: Literal['economic', 'physical', 'hybrid'] = 'economic'  # Default to economic as per research
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
        
        allocated_impacts = {
            impact_category: allocator.allocate_impact(total_impact)
            for impact_category, total_impact in impacts.items()
        }
        
        # Validate allocation results against research factors
        if method in self._rf_allocation_factors:
            protein_factor = self._get_protein_allocation_factor(allocated_impacts)
            expected_factor = self._rf_allocation_factors[method]
            if abs(protein_factor - expected_factor) > 0.05:  # 5% tolerance
                print(f"Warning: Calculated allocation factor {protein_factor:.3f} differs significantly from research factor {expected_factor:.3f}")
        
        return allocated_impacts
        
    def _get_protein_allocation_factor(self, allocated_impacts: Dict[str, Dict[str, float]]) -> float:
        """Calculate the protein allocation factor from allocated impacts"""
        if not allocated_impacts:
            return 0.0
            
        # Take first impact category to determine allocation factor
        first_impact = next(iter(allocated_impacts.values()))
        total_impact = sum(first_impact.values())
        protein_impact = first_impact.get('protein_concentrate', 0)
        
        return protein_impact / total_impact if total_impact > 0 else 0.0
        
    def get_allocation_factors(self, 
                             method: Literal['economic', 'physical', 'hybrid'] = 'economic'
                             ) -> Dict[str, float]:
        """Get allocation factors for specified method
        
        Args:
            method: Allocation method to get factors for
            
        Returns:
            Dictionary mapping products to their allocation factors
        """
        if method == 'hybrid':
            # For hybrid, combine economic and physical factors using configured weights
            economic_factors = self.economic_allocator.get_allocation_factors()
            physical_factors = self.physical_allocator.get_allocation_factors()
            
            # Combine factors using weights from research
            hybrid_factors = {}
            for product in economic_factors:
                hybrid_factors[product] = (
                    self._hybrid_weights['economic'] * economic_factors[product] +
                    self._hybrid_weights['physical'] * physical_factors[product]
                )
            return hybrid_factors
            
        return {
            'economic': self.economic_allocator.get_allocation_factors(),
            'physical': self.physical_allocator.get_allocation_factors()
        }[method] 