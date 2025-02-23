from typing import Dict, TypedDict, List, Optional
from dataclasses import dataclass
from ..impact.gwp import GWPCalculator
from ..impact.hct import HCTCalculator
from ..impact.frs import FRSCalculator
from ..impact.water import WaterConsumptionCalculator
from ..impact.base import ProcessContribution

@dataclass
class ProcessInputs:
    """Data class for process inputs to ensure type safety"""
    electricity_kwh: float
    water_kg: float
    transport_ton_km: float
    product_kg: float
    equipment_kg: float
    cooling_kwh: float
    waste_kg: float
    thermal_ratio: float = 0.3

class ImpactResults(TypedDict):
    """Type definition for impact calculation results"""
    gwp: float  # Global Warming Potential
    hct: float  # Human Carcinogenic Toxicity
    frs: float  # Fossil Resource Scarcity
    water_consumption: float  # Water Consumption

class DetailedImpactResults(TypedDict):
    """Type definition for detailed impact results including process contributions"""
    total_impacts: ImpactResults
    process_contributions: Dict[str, Dict[str, ProcessContribution]]
    metadata: Dict[str, float]

class ImpactCalculator:
    """Environmental Impact Calculator Service"""
    
    def __init__(self):
        """Initialize all impact calculators"""
        self._calculators = {
            'gwp': GWPCalculator(),
            'hct': HCTCalculator(),
            'frs': FRSCalculator(),
            'water': WaterConsumptionCalculator()
        }
        self._results: Optional[DetailedImpactResults] = None

    def _validate_inputs(self, inputs: ProcessInputs) -> None:
        """Validate process inputs"""
        if not 0 <= inputs.thermal_ratio <= 1:
            raise ValueError("Thermal ratio must be between 0 and 1")
        
        # All other validations are handled by individual calculators
        # through their ValidationConfig

    def calculate_process_impacts(self, **kwargs) -> ImpactResults:
        """Calculate all environmental impacts for the process
        
        Args:
            electricity_kwh: Electricity consumption in kWh
            water_kg: Water consumption in kg
            transport_ton_km: Transport in ton-km
            product_kg: Product mass in kg
            equipment_kg: Equipment mass in kg
            cooling_kwh: Cooling energy in kWh
            waste_kg: Waste mass in kg
            thermal_ratio: Ratio of product going through thermal treatment (default: 0.3)
        
        Returns:
            Dictionary containing all calculated impacts
        """
        # Convert kwargs to ProcessInputs for type safety
        inputs = ProcessInputs(**kwargs)
        self._validate_inputs(inputs)
        
        try:
            # Calculate GWP
            gwp = self._calculators['gwp'].calculate_total_impact(
                electricity_kwh=inputs.electricity_kwh,
                water_kg=inputs.water_kg,
                transport_ton_km=inputs.transport_ton_km
            )
            
            # Calculate HCT
            hct = self._calculators['hct'].calculate_total_impact(
                electricity_kwh=inputs.electricity_kwh,
                water_treated_kg=inputs.water_kg,
                waste_kg=inputs.waste_kg
            )
            
            # Calculate FRS
            frs = self._calculators['frs'].calculate_total_impact(
                electricity_kwh=inputs.electricity_kwh,
                thermal_product_kg=inputs.product_kg * inputs.thermal_ratio,
                mechanical_product_kg=inputs.product_kg * (1 - inputs.thermal_ratio)
            )
            
            # Calculate Water Consumption
            water = self._calculators['water'].calculate_total_impact(
                product_kg=inputs.product_kg,
                equipment_kg=inputs.equipment_kg,
                cooling_kwh=inputs.cooling_kwh
            )
            
            # Store results
            self._results = {
                'total_impacts': {
                    'gwp': gwp,
                    'hct': hct,
                    'frs': frs,
                    'water_consumption': water
                },
                'process_contributions': self.get_process_contributions(),
                'metadata': {
                    'total_mass': inputs.product_kg,
                    'energy_intensity': inputs.electricity_kwh / inputs.product_kg if inputs.product_kg > 0 else 0,
                    'water_intensity': inputs.water_kg / inputs.product_kg if inputs.product_kg > 0 else 0,
                    'thermal_ratio': inputs.thermal_ratio
                }
            }
            
            return self._results['total_impacts']
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Error in impact calculation: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in impact calculation: {str(e)}")

    def get_process_contributions(self) -> Dict[str, Dict[str, ProcessContribution]]:
        """Get detailed breakdown of environmental impacts by process"""
        return {
            'gwp': self._calculators['gwp'].get_process_contributions(),
            'hct': self._calculators['hct'].get_process_contributions(),
            'frs': self._calculators['frs'].get_process_contributions(),
            'water': self._calculators['water'].get_process_contributions()
        }

    def get_detailed_results(self) -> Optional[DetailedImpactResults]:
        """Get detailed results including totals, process contributions and metadata"""
        return self._results

    def get_impact_factors(self) -> Dict[str, Dict[str, Dict]]:
        """Get all impact factors used in calculations"""
        return {
            calculator_name: calculator.IMPACT_FACTORS
            for calculator_name, calculator in self._calculators.items()
        } 