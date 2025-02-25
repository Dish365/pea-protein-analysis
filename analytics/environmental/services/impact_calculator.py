from typing import Dict, TypedDict, List, Optional, Union
from dataclasses import dataclass
from ..impact.gwp import GWPCalculator
from ..impact.hct import HCTCalculator
from ..impact.frs import FRSCalculator
from ..impact.water import WaterConsumptionCalculator
from ..impact.base import ProcessContribution

@dataclass
class ProcessInputs:
    """Data class for process inputs to ensure type safety"""
    rf_electricity_kwh: float
    rf_frequency_mhz: float
    rf_anode_current_a: float
    rf_grid_current_a: float
    air_classifier_milling_kwh: float
    air_classification_kwh: float
    hammer_milling_kwh: float
    dehulling_kwh: float
    tempering_water_kg: float
    initial_moisture_content: float
    final_moisture_content: float
    target_moisture_content: float
    product_kg: float
    equipment_kg: float
    transport_ton_km: float
    waste_kg: float
    rf_temperature_outfeed_c: float
    rf_temperature_electrode_c: float
    conveyor_speed_m_min: float
    material_depth_mm: float
    electrode_gap_mm: float
    thermal_ratio: float

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
    metadata: Dict[str, Union[float, Dict[str, float]]]
    rf_parameters: Dict[str, float]

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
            rf_electricity_kwh: RF unit electricity consumption
            air_classifier_milling_kwh: Air classifier mill energy
            air_classification_kwh: Air classification energy
            hammer_milling_kwh: Hammer mill energy
            dehulling_kwh: Dehulling energy
            tempering_water_kg: Water used for tempering
            product_kg: Product mass
            equipment_kg: Equipment mass
            transport_ton_km: Transport in ton-km
            waste_kg: Waste mass
            rf_temperature_outfeed_c: RF outfeed temperature
            rf_temperature_electrode_c: RF electrode temperature
            thermal_ratio: Ratio of thermal processing
        """
        # Convert kwargs to ProcessInputs for type safety
        inputs = ProcessInputs(**kwargs)
        self._validate_inputs(inputs)
        
        try:
            # Calculate total electricity consumption
            total_electricity = (
                inputs.rf_electricity_kwh +
                inputs.air_classifier_milling_kwh +
                inputs.air_classification_kwh +
                inputs.hammer_milling_kwh +
                inputs.dehulling_kwh
            )
            
            # Calculate GWP
            gwp = self._calculators['gwp'].calculate_total_impact(
                electricity_kwh=total_electricity,
                water_kg=inputs.tempering_water_kg,
                transport_ton_km=inputs.transport_ton_km
            )
            
            # Calculate HCT
            hct = self._calculators['hct'].calculate_total_impact(
                electricity_kwh=total_electricity,
                water_treated_kg=inputs.tempering_water_kg,
                waste_kg=inputs.waste_kg
            )
            
            # Calculate FRS
            frs = self._calculators['frs'].calculate_total_impact(
                electricity_kwh=total_electricity,
                thermal_product_kg=inputs.product_kg * inputs.thermal_ratio,
                mechanical_product_kg=inputs.product_kg * (1 - inputs.thermal_ratio)
            )
            
            # Calculate Water Consumption
            water = self._calculators['water'].calculate_total_impact(
                product_kg=inputs.product_kg,
                equipment_kg=inputs.equipment_kg,
                cooling_kwh=total_electricity  # Using total electricity for cooling water calculation
            )
            
            # Store results with RF-specific parameters
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
                    'energy_intensity': total_electricity / inputs.product_kg if inputs.product_kg > 0 else 0,
                    'water_intensity': inputs.tempering_water_kg / inputs.product_kg if inputs.product_kg > 0 else 0,
                    'thermal_ratio': inputs.thermal_ratio
                },
                'rf_parameters': {
                    'temperature_outfeed': inputs.rf_temperature_outfeed_c,
                    'temperature_electrode': inputs.rf_temperature_electrode_c,
                    'energy_consumption': inputs.rf_electricity_kwh,
                    'contribution_percentage': (inputs.rf_electricity_kwh / total_electricity * 100)
                    if total_electricity > 0 else 0
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