from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from analytics.economic.opex.raw_materials import calculate_raw_material_costs
from analytics.economic.opex.utilities import calculate_utility_costs
from analytics.economic.opex.labor import calculate_labor_costs
from analytics.economic.opex.maintenance import calculate_maintenance_costs

logger = logging.getLogger(__name__)


class EmptyDataError(ValueError):
    """Exception raised when required data is missing"""
    pass


@dataclass
class OpexResult:
    """Structured result for OPEX calculations"""
    total_opex: float
    raw_material_costs: float
    utility_costs: float
    labor_costs: float
    maintenance_costs: float
    raw_materials_breakdown: List[Dict[str, float]]
    utilities_breakdown: List[Dict[str, float]]
    labor_breakdown: Dict[str, float]


class OperationalExpenditureAnalysis:
    """
    Analyzes operational expenditure for protein extraction processes.
    Based on paper Section 3.2.2
    """

    def __init__(self):
        self._raw_materials: List[Dict[str, float]] = []
        self._utilities: List[Dict[str, float]] = []
        self._labor_data: Dict[str, float] = {}
        self._maintenance_factors: Dict[str, float] = {}
        self._cached_result: Optional[OpexResult] = None

    def add_raw_material(self, material: Dict[str, float]) -> None:
        """Add raw material to the analysis and invalidate cache"""
        self._raw_materials.append(material)
        self._invalidate_cache()

    def add_utility(self, utility: Dict[str, float]) -> None:
        """Add utility consumption data and invalidate cache"""
        self._utilities.append(utility)
        self._invalidate_cache()

    def set_labor_data(self, labor_data: Dict[str, float]) -> None:
        """Set labor cost data and invalidate cache"""
        self._labor_data = labor_data
        self._invalidate_cache()

    def set_maintenance_factors(self, factors: Dict[str, float]) -> None:
        """Set maintenance cost factors and invalidate cache"""
        self._maintenance_factors = factors
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        """Invalidate cached calculations when data changes"""
        self._cached_result = None

    def _validate_data(self) -> None:
        """Validate that all required data is present"""
        if not self._raw_materials:
            raise EmptyDataError("Raw materials list cannot be empty")
        if not self._utilities:
            raise EmptyDataError("Utilities list cannot be empty")
        if not self._labor_data:
            raise EmptyDataError("Labor data must be provided")
        if not self._maintenance_factors:
            raise EmptyDataError("Maintenance factors must be provided")

    def calculate_total_opex(self) -> Dict[str, Any]:
        """
        Calculate total operational expenditure including all components
        
        Returns:
            Dictionary containing total OPEX and its components
        """
        # Check cache first
        if self._cached_result:
            logger.debug("Using cached OPEX results")
            return self._format_result(self._cached_result)

        try:
            # Validate input data
            self._validate_data()

            # Calculate raw material costs
            raw_material_result = calculate_raw_material_costs(self._raw_materials)
            logger.debug(f"Calculated raw material costs: {raw_material_result}")

            # Calculate utility costs
            utility_result = calculate_utility_costs(self._utilities)
            logger.debug(f"Calculated utility costs: {utility_result}")

            # Calculate labor costs
            labor_costs = calculate_labor_costs(
                hourly_wage=self._labor_data["hourly_wage"],
                hours_per_week=self._labor_data["hours_per_week"],
                weeks_per_year=self._labor_data["weeks_per_year"],
                num_workers=int(self._labor_data["num_workers"])
            )
            logger.debug(f"Calculated labor costs: {labor_costs}")

            # Calculate maintenance costs
            maintenance_costs = calculate_maintenance_costs(
                equipment_costs=self._maintenance_factors["equipment_cost"],
                maintenance_factor=self._maintenance_factors["maintenance_factor"]
            )
            logger.debug(f"Calculated maintenance costs: {maintenance_costs}")

            # Calculate total OPEX
            total_opex = (
                raw_material_result["total_cost"] +
                utility_result["total_cost"] +
                labor_costs +
                maintenance_costs
            )
            logger.debug(f"Calculated total OPEX: {total_opex}")

            # Create and cache result
            result = OpexResult(
                total_opex=total_opex,
                raw_material_costs=raw_material_result["total_cost"],
                utility_costs=utility_result["total_cost"],
                labor_costs=labor_costs,
                maintenance_costs=maintenance_costs,
                raw_materials_breakdown=self._raw_materials.copy(),
                utilities_breakdown=self._utilities.copy(),
                labor_breakdown=self._get_labor_breakdown()
            )
            
            self._cached_result = result
            logger.debug("Cached new OPEX results")

            return self._format_result(result)

        except Exception as e:
            logger.error(f"Error calculating OPEX: {str(e)}")
            raise

    def _format_result(self, result: OpexResult) -> Dict[str, Any]:
        """Format OpexResult into API response structure"""
        return {
            "total_opex": result.total_opex,
            "raw_material_costs": result.raw_material_costs,
            "utility_costs": result.utility_costs,
            "labor_costs": result.labor_costs,
            "maintenance_costs": result.maintenance_costs,
            "raw_materials_breakdown": result.raw_materials_breakdown,
            "utilities_breakdown": result.utilities_breakdown,
            "labor_breakdown": result.labor_breakdown
        }

    def _get_labor_breakdown(self) -> Dict[str, float]:
        """Calculate detailed breakdown of labor costs"""
        annual_hours = self._labor_data["hours_per_week"] * self._labor_data["weeks_per_year"]
        annual_cost_per_worker = (
            self._labor_data["hourly_wage"] * 
            self._labor_data["hours_per_week"] * 
            self._labor_data["weeks_per_year"]
        )
        
        return {
            "hourly_wage": self._labor_data["hourly_wage"],
            "hours_per_week": self._labor_data["hours_per_week"],
            "weeks_per_year": self._labor_data["weeks_per_year"],
            "num_workers": self._labor_data["num_workers"],
            "annual_hours": annual_hours,
            "annual_cost_per_worker": annual_cost_per_worker,
            "total_annual_cost": annual_cost_per_worker * self._labor_data["num_workers"]
        }

    def get_raw_materials_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of raw material costs"""
        return self._raw_materials.copy()

    def get_utilities_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of utility costs"""
        return self._utilities.copy()

    def get_labor_breakdown(self) -> Dict[str, float]:
        """Get detailed breakdown of labor costs"""
        return self._get_labor_breakdown()
