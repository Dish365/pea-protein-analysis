from typing import Dict, List, Optional
import numpy as np

class EconomicIndicators:
    """Economic performance indicators for eco-efficiency analysis"""
    
    def __init__(self):
        self.indicators: Dict[str, float] = {}
        
    def calculate_production_cost(self,
                                capex: float,
                                opex: float,
                                production_volume: float) -> float:
        """Calculate production cost per unit
        
        Args:
            capex: Capital expenditure ($)
            opex: Operating expenditure ($/year)
            production_volume: Annual production volume (kg/year)
        """
        total_cost = capex + opex
        unit_cost = total_cost / production_volume
        self.indicators['unit_production_cost'] = unit_cost
        return unit_cost
        
    def calculate_value_added(self,
                            product_prices: Dict[str, float],
                            production_volumes: Dict[str, float],
                            raw_material_cost: float) -> float:
        """Calculate value added by the process
        
        Args:
            product_prices: Prices of products ($/kg)
            production_volumes: Production volumes (kg/year)
            raw_material_cost: Total raw material cost ($/year)
        """
        revenue = sum(price * production_volumes[product] 
                     for product, price in product_prices.items())
        value_added = revenue - raw_material_cost
        self.indicators['value_added'] = value_added
        return value_added
        
    def calculate_profitability(self,
                              revenue: float,
                              total_cost: float) -> float:
        """Calculate profitability ratio
        
        Args:
            revenue: Total revenue ($)
            total_cost: Total cost ($)
        """
        profitability = (revenue - total_cost) / revenue
        self.indicators['profitability'] = profitability
        return profitability
        
    def get_indicators(self) -> Dict[str, float]:
        """Get all economic indicators"""
        return self.indicators 