from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from analytics.economic.capex.equipment_costs import calculate_equipment_costs
from analytics.economic.capex.installation import calculate_installation_costs
from analytics.economic.capex.indirect_costs import calculate_indirect_costs
import logging

logger = logging.getLogger(__name__)


class EmptyEquipmentListError(ValueError):
    """Exception raised when equipment list is empty"""
    pass


@dataclass
class CapexResult:
    """Structured result for CAPEX calculations"""
    total_capex: float
    equipment_costs: float
    installation_costs: float
    indirect_costs: float
    equipment_breakdown: List[Dict[str, float]]
    indirect_factors: List[Dict[str, Any]]


class CapitalExpenditureAnalysis:
    """
    Analyzes capital expenditure for protein extraction processes.
    Based on paper Section 3.2.1
    """

    def __init__(self):
        self._equipment_list: List[Dict[str, float]] = []
        self._indirect_factors: List[Dict[str, Any]] = []
        self._cached_results: Optional[CapexResult] = None

    def add_equipment(self, equipment: Dict[str, float]) -> None:
        """Add equipment to the analysis and invalidate cache"""
        self._equipment_list.append(equipment)
        self._invalidate_cache()

    def add_indirect_factor(self, factor: Dict[str, Any]) -> None:
        """Add indirect cost factor to the analysis and invalidate cache"""
        self._indirect_factors.append(factor)
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        """Invalidate cached calculations when data changes"""
        self._cached_results = None

    def calculate_total_capex(self, 
                            installation_factor: float = 0.2,
                            indirect_costs_factor: float = 0.15,
                            indirect_factors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Calculate total capital expenditure and its components
        
        Args:
            installation_factor: Factor for installation costs calculation
            indirect_costs_factor: Factor for indirect costs calculation
            indirect_factors: Optional list of indirect cost factors
            
        Returns:
            Dictionary containing total CAPEX and its components
        """
        if not self._equipment_list:
            raise EmptyEquipmentListError("Cannot calculate CAPEX with empty equipment list")

        # Use cache if available and no parameters changed
        if (self._cached_results and 
            not indirect_factors and  # Only use cache if not overriding factors
            len(self._indirect_factors) > 0):  # And we have stored factors
            logger.debug("Using cached CAPEX results")
            return self._format_result(self._cached_results)

        try:
            # Calculate equipment costs
            equipment_costs = calculate_equipment_costs(self._equipment_list)
            logger.debug(f"Calculated equipment costs: {equipment_costs}")

            # Calculate installation costs
            installation_costs = calculate_installation_costs(
                equipment_costs,
                installation_factor,
                indirect_costs_factor
            )
            logger.debug(f"Calculated installation costs: {installation_costs}")

            # Use provided indirect factors or stored ones
            factors_to_use = indirect_factors or self._indirect_factors
            indirect_costs = calculate_indirect_costs(factors_to_use)
            logger.debug(f"Calculated indirect costs: {indirect_costs}")

            # Calculate total CAPEX
            total_capex = equipment_costs + installation_costs + indirect_costs

            # Create and cache result
            result = CapexResult(
                total_capex=total_capex,
                equipment_costs=equipment_costs,
                installation_costs=installation_costs,
                indirect_costs=indirect_costs,
                equipment_breakdown=self._equipment_list.copy(),
                indirect_factors=factors_to_use.copy() if factors_to_use else []
            )
            
            if not indirect_factors:  # Only cache if using stored factors
                self._cached_results = result
                logger.debug("Cached new CAPEX results")

            return self._format_result(result)

        except Exception as e:
            logger.error(f"Error calculating CAPEX: {str(e)}")
            raise

    def _format_result(self, result: CapexResult) -> Dict[str, Any]:
        """Format CapexResult into API response structure"""
        return {
            "total_capex": result.total_capex,
            "equipment_costs": result.equipment_costs,
            "installation_costs": result.installation_costs,
            "indirect_costs": result.indirect_costs,
            "equipment_breakdown": result.equipment_breakdown,
            "indirect_factors": result.indirect_factors
        }

    def get_equipment_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of equipment costs"""
        return self._equipment_list.copy()

    def get_indirect_factors(self) -> List[Dict[str, Any]]:
        """Get detailed breakdown of indirect cost factors"""
        return self._indirect_factors.copy()
