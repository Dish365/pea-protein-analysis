from typing import Dict, Any
from .indicators import EconomicIndicators
from .quality import QualityIndicators
from .relative import RelativeEfficiencyCalculator

class EcoEfficiencyAnalysis:
    """
    Analyzes eco-efficiency metrics for protein extraction processes.
    """

    def __init__(self):
        self.economic_indicators = EconomicIndicators()
        self.quality_indicators = QualityIndicators()
        self.relative_calculator = RelativeEfficiencyCalculator()

    def calculate_efficiency_indicators(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate efficiency indicators"""
        economic_metrics = self.economic_indicators.calculate_production_cost(
            data['capex'],
            data['opex'],
            data['production_volume']
        )
        
        quality_metrics = self.quality_indicators.calculate_protein_recovery(
            data['recovered_protein'],
            data['initial_protein']
        )
        
        return {
            'economic': economic_metrics,
            'quality': quality_metrics
        }

    def analyze_sustainability_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sustainability metrics"""
        environmental_efficiency = self.relative_calculator.calculate_environmental_efficiency(
            data['economic_value'],
            data['environmental_impact']
        )
        
        resource_efficiency = self.relative_calculator.calculate_resource_efficiency(
            data['product_output'],
            data['resource_input']
        )
        
        return {
            'environmental_efficiency': environmental_efficiency,
            'resource_efficiency': resource_efficiency
        } 