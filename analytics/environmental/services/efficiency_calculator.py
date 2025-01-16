from typing import Dict, List, Optional
from ..eco_efficiency.indicators import EconomicIndicators
from ..eco_efficiency.quality import QualityIndicators
from ..eco_efficiency.relative import RelativeEfficiencyCalculator

class EfficiencyCalculator:
    """Service for calculating eco-efficiency metrics"""
    
    def __init__(self):
        self.economic_indicators = EconomicIndicators()
        self.quality_indicators = QualityIndicators()
        self.relative_calculator = RelativeEfficiencyCalculator()
        self.efficiency_results: Dict[str, Dict[str, float]] = {}
        
    def calculate_efficiency_metrics(self,
                                   economic_data: Dict[str, float],
                                   quality_data: Dict[str, float],
                                   environmental_impacts: Dict[str, float],
                                   resource_inputs: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Calculate comprehensive eco-efficiency metrics
        
        Args:
            economic_data: Economic performance data
            quality_data: Product quality data
            environmental_impacts: Environmental impact data
            resource_inputs: Resource consumption data
        """
        # Calculate economic indicators
        production_cost = self.economic_indicators.calculate_production_cost(
            economic_data['capex'],
            economic_data['opex'],
            economic_data['production_volume']
        )
        
        value_added = self.economic_indicators.calculate_value_added(
            economic_data['product_prices'],
            economic_data['production_volumes'],
            economic_data['raw_material_cost']
        )
        
        # Calculate quality indicators
        protein_recovery = self.quality_indicators.calculate_protein_recovery(
            quality_data['recovered_protein'],
            quality_data['initial_protein']
        )
        
        protein_purity = self.quality_indicators.calculate_protein_purity(
            quality_data['protein_content'],
            quality_data['total_mass']
        )
        
        # Calculate relative efficiency metrics
        environmental_efficiency = self.relative_calculator.calculate_environmental_efficiency(
            value_added,
            environmental_impacts
        )
        
        resource_efficiency = self.relative_calculator.calculate_resource_efficiency(
            economic_data['production_volume'],
            resource_inputs
        )
        
        quality_efficiency = self.relative_calculator.calculate_quality_efficiency(
            protein_purity,
            production_cost
        )
        
        # Compile results
        self.efficiency_results = {
            'economic_indicators': self.economic_indicators.get_indicators(),
            'quality_indicators': self.quality_indicators.get_indicators(),
            'efficiency_metrics': self.relative_calculator.get_efficiency_metrics()
        }
        
        return self.efficiency_results
        
    def get_efficiency_results(self) -> Dict[str, Dict[str, float]]:
        """Get all calculated efficiency metrics"""
        return self.efficiency_results 