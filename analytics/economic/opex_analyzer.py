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
    utilities_breakdown: Dict[str, Any]  # Updated to include consumption rates
    labor_breakdown: Dict[str, Any]  # Updated to include shift information
    production_volume: float
    reference_volume: float


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
        self._production_volume: Optional[float] = None
        self._reference_volume: Optional[float] = None
        self._cached_result: Optional[OpexResult] = None

    def set_production_volume(self, volume: float, reference_volume: Optional[float] = None) -> None:
        """Set production volume and optional reference volume for scaling calculations"""
        if volume <= 0:
            raise ValueError("Production volume must be positive")
        self._production_volume = volume
        self._reference_volume = reference_volume or volume
        self._invalidate_cache()

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
        if self._production_volume is None:
            raise EmptyDataError("Production volume must be set")

    def calculate_total_opex(self) -> Dict[str, Any]:
        """
        Calculate total operational expenditure including all components with proper scaling
        
        Returns:
            Dictionary containing total OPEX and its components with detailed breakdowns
        """
        # Check cache first
        if self._cached_result:
            logger.debug("Using cached OPEX results")
            return self._format_result(self._cached_result)

        try:
            # Validate input data
            self._validate_data()

            # Calculate raw material costs with scaling
            raw_material_result = calculate_raw_material_costs(
                self._raw_materials,
                self._production_volume,
                self._reference_volume
            )
            logger.debug(f"Calculated raw material costs: {raw_material_result}")

            # Calculate utility costs with scaling
            utility_result = calculate_utility_costs(
                self._utilities,
                self._production_volume,
                self._reference_volume
            )
            logger.debug(f"Calculated utility costs: {utility_result}")

            # Calculate labor costs with scaling
            labor_result = calculate_labor_costs(
                self._labor_data,
                self._production_volume
            )
            logger.debug(f"Calculated labor costs: {labor_result}")

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
                labor_result["total_cost"] +
                maintenance_costs
            )
            logger.debug(f"Calculated total OPEX: {total_opex}")

            # Create and cache result
            result = OpexResult(
                total_opex=total_opex,
                raw_material_costs=raw_material_result["total_cost"],
                utility_costs=utility_result["total_cost"],
                labor_costs=labor_result["total_cost"],
                maintenance_costs=maintenance_costs,
                raw_materials_breakdown=raw_material_result["materials_breakdown"],
                utilities_breakdown={
                    "costs": utility_result["costs_by_utility"],
                    "consumption": utility_result["consumption_rates"]
                },
                labor_breakdown={
                    "costs": {
                        "direct": labor_result["direct_labor"],
                        "benefits": labor_result["benefits"],
                        "total": labor_result["total_cost"]
                    },
                    "staffing": {
                        "shifts": labor_result["shifts"],
                        "workers_per_shift": labor_result["workers_per_shift"],
                        "total_workers": labor_result["total_workers"]
                    }
                },
                production_volume=self._production_volume,
                reference_volume=self._reference_volume
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
            "cost_breakdown": {
                "raw_materials": result.raw_material_costs,
                "utilities": result.utility_costs,
                "labor": result.labor_costs,
                "maintenance": result.maintenance_costs
            },
            "detailed_breakdown": {
                "raw_materials": result.raw_materials_breakdown,
                "utilities": result.utilities_breakdown,
                "labor": result.labor_breakdown
            },
            "scaling_info": {
                "production_volume": result.production_volume,
                "reference_volume": result.reference_volume,
                "volume_ratio": result.production_volume / result.reference_volume
            }
        }

    def get_raw_materials_breakdown(self) -> List[Dict[str, float]]:
        """Get detailed breakdown of raw material costs"""
        if not self._cached_result:
            raise ValueError("Must calculate OPEX first")
        return self._cached_result.raw_materials_breakdown

    def get_utilities_breakdown(self) -> Dict[str, Any]:
        """Get detailed breakdown of utility costs and consumption"""
        if not self._cached_result:
            raise ValueError("Must calculate OPEX first")
        return self._cached_result.utilities_breakdown

    def get_labor_breakdown(self) -> Dict[str, Any]:
        """Get detailed breakdown of labor costs and staffing"""
        if not self._cached_result:
            raise ValueError("Must calculate OPEX first")
        return self._cached_result.labor_breakdown
