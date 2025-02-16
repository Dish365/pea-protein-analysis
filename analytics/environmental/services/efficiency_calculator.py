from typing import Dict, List, Optional
from analytics.environmental.eco_efficiency.indicators import EconomicIndicators
from analytics.environmental.eco_efficiency.quality import QualityIndicators
from analytics.environmental.eco_efficiency.relative import RelativeEfficiencyCalculator

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
        # Ensure production volume is not zero
        production_volume = economic_data.get('production_volume', 0.0)
        if production_volume <= 0:
            raise ValueError("Production volume must be greater than 0")
            
        # Calculate economic indicators with validation
        total_capex = economic_data.get('capex', {}).get('total_capex', 0.0)
        total_opex = economic_data.get('opex', {}).get('total_annual_cost', 0.0)
        
        production_cost = self.economic_indicators.calculate_production_cost(
            total_capex,
            total_opex,
            production_volume
        )
        
        # Calculate value added with validation
        product_prices = economic_data.get('product_prices', {})
        production_volumes = economic_data.get('production_volumes', {'main_product': production_volume})
        raw_material_cost = economic_data.get('raw_material_cost', 0.0)
        
        if not product_prices or not any(production_volumes.values()):
            raise ValueError("Product prices and production volumes must be provided and non-zero")
            
        value_added = self.economic_indicators.calculate_value_added(
            product_prices,
            production_volumes,
            raw_material_cost
        )
        
        # Calculate quality indicators with validation
        recovered_protein = quality_data.get('recovered_protein', 0.0)
        initial_protein = quality_data.get('initial_protein', 100.0)
        
        if initial_protein <= 0:
            raise ValueError("Initial protein content must be greater than 0")
            
        protein_recovery = self.quality_indicators.calculate_protein_recovery(
            recovered_protein,
            initial_protein
        )
        
        protein_content = quality_data.get('protein_content', 0.0)
        total_mass = quality_data.get('total_mass', 1.0)
        
        if total_mass <= 0:
            raise ValueError("Total mass must be greater than 0")
            
        protein_purity = self.quality_indicators.calculate_protein_purity(
            protein_content,
            total_mass
        )
        
        # Calculate relative efficiency metrics with validation
        if not any(environmental_impacts.values()):
            raise ValueError("Environmental impacts must be provided")
            
        environmental_efficiency = self.relative_calculator.calculate_environmental_efficiency(
            value_added,
            environmental_impacts
        )
        self.relative_calculator.set_environmental_efficiency(environmental_efficiency)
        
        if not any(resource_inputs.values()):
            raise ValueError("Resource inputs must be provided")
            
        resource_efficiency = self.relative_calculator.calculate_resource_efficiency(
            production_volume,
            resource_inputs
        )
        self.relative_calculator.set_resource_efficiency(resource_efficiency)
        
        if production_cost <= 0:
            raise ValueError("Production cost must be greater than 0")
            
        quality_efficiency = self.relative_calculator.calculate_quality_efficiency(
            protein_purity,
            production_cost
        )
        self.relative_calculator.set_quality_efficiency(quality_efficiency)
        
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