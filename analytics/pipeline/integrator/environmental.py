from typing import Dict, Any
import httpx
import logging

logger = logging.getLogger(__name__)

class EnvironmentalIntegrator:
    """
    Integrates environmental analysis components with FastAPI endpoints.
    
    This class coordinates between:
    1. Impact assessment endpoints
    2. Allocation endpoints
    3. Environmental analysis components
    
    The integrator ensures proper flow of data between components and
    maintains a clean separation of concerns.
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8001/api/v1/environmental"):
        """
        Initialize the environmental integrator with API components.
        
        Args:
            api_base_url: Base URL for FastAPI endpoints
        """
        self.client = httpx.AsyncClient()
        self.api_base_url = api_base_url
        logger.info("EnvironmentalIntegrator initialized successfully")

    async def analyze_environmental_impacts(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate complete environmental impact analysis using FastAPI endpoints.
        
        Args:
            process_data: Dictionary containing process parameters and measurements
            
        Returns:
            Dictionary containing comprehensive environmental analysis results
        """
        try:
            logger.debug(f"Starting environmental analysis with data: {process_data}")
            
            # Extract process parameters
            params = self._extract_process_parameters(process_data)
            
            # Calculate impacts first
            impact_results = await self.calculate_impacts(params['impact_params'])
            
            # Use impact results for allocation
            allocation_params = {
                **params['allocation_params'],
                'impacts': impact_results['impacts']
            }
            allocation_results = await self.allocate_impacts(allocation_params)
            
            return self._compile_analysis_results(
                impact_results,
                allocation_results
            )
            
        except Exception as e:
            logger.error(f"Environmental analysis failed: {str(e)}")
            raise RuntimeError(f"Environmental analysis failed: {str(e)}")

    def _extract_process_parameters(self, process_data: Dict[str, Any]) -> Dict[str, Dict]:
        """
        Extract and organize process parameters for analysis.
        
        Args:
            process_data: Raw process data dictionary
            
        Returns:
            Dictionary containing formatted impact and allocation parameters
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        try:
            # Extract nested data with validation
            energy = process_data.get('energy_consumption', {})
            if not isinstance(energy, dict):
                raise ValueError("energy_consumption must be a dictionary")
                
            production = process_data.get('production_data', {})
            if not isinstance(production, dict):
                raise ValueError("production_data must be a dictionary")
            
            # Calculate waste from mass balance
            input_mass = production.get('input_mass', 0)
            output_mass = production.get('output_mass', 0)
            waste_mass = max(0, input_mass - output_mass)  # Ensure non-negative
            
            # Map and validate impact parameters
            impact_params = {
                'electricity_kwh': float(energy.get('electricity', 0)),
                'cooling_kwh': float(energy.get('cooling', 0)),
                'water_kg': float(process_data.get('water_consumption', 0)),
                'transport_ton_km': float(process_data.get('transport_consumption', 0)),
                'product_kg': float(output_mass),
                'equipment_kg': float(process_data.get('equipment_mass', 0)),
                'waste_kg': float(waste_mass),
                'thermal_ratio': min(1.0, max(0.0, float(process_data.get('thermal_ratio', 0.3)))),
                'process_type': str(process_data.get('process_type', 'baseline'))
            }
            
            # Validate non-negative values
            for key, value in impact_params.items():
                if key != 'process_type' and value < 0:
                    raise ValueError(f"Parameter {key} cannot be negative")
            
            # Map allocation parameters with matching product keys
            product_values = {
                'main_product': process_data.get('revenue_per_year', 100000.0),  # Default value if not provided
                'waste_product': process_data.get('waste_value', 0.0)  # Default to 0 if not provided
            }
            
            mass_flows = {
                'main_product': float(output_mass),
                'waste_product': float(waste_mass)
            }
            
            allocation_params = {
                'product_values': product_values,
                'mass_flows': mass_flows,
                'method': process_data.get('allocation_method', 'hybrid'),
                'hybrid_weights': process_data.get('hybrid_weights', {'physical': 0.5, 'economic': 0.5})
            }
            
            # Validate allocation method
            if allocation_params['method'] not in ['economic', 'physical', 'hybrid']:
                raise ValueError(f"Invalid allocation method: {allocation_params['method']}")
            
            return {
                'impact_params': impact_params,
                'allocation_params': allocation_params
            }
            
        except (TypeError, ValueError) as e:
            logger.error(f"Error extracting process parameters: {str(e)}")
            raise ValueError(f"Invalid process data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in parameter extraction: {str(e)}")
            raise RuntimeError(f"Failed to extract process parameters: {str(e)}")

    async def calculate_impacts(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate environmental impacts using impact endpoints"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/impact/calculate-impacts",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Impact calculation API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Impact calculation failed: {str(e)}")
            raise RuntimeError(f"Impact calculation failed: {str(e)}")

    async def allocate_impacts(self, allocation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate environmental impacts using allocation endpoints"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/allocation/calculate",
                json=allocation_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Impact allocation API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Impact allocation failed: {str(e)}")
            raise RuntimeError(f"Impact allocation failed: {str(e)}")

    def _compile_analysis_results(
        self,
        impact_results: Dict[str, Any],
        allocation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compile all analysis results into a single response matching Django model structure"""
        return {
            'status': 'success',
            'environmental_results': {
                'gwp': impact_results.get('impacts', {}).get('gwp'),
                'hct': impact_results.get('impacts', {}).get('hct'),
                'frs': impact_results.get('impacts', {}).get('frs'),
                'water_consumption': impact_results.get('impacts', {}).get('water_consumption'),
                'allocated_impacts': {
                    'method': allocation_results.get('method'),
                    'factors': allocation_results.get('allocation_factors', {}),
                    'results': allocation_results.get('allocated_impacts', {})
                }
            },
            'metadata': {
                'process_type': impact_results.get('process_type'),
                'calculation_timestamp': impact_results.get('timestamp'),
                'units': {
                    'gwp': 'CO2eq',
                    'hct': 'CTUh',
                    'frs': 'kg oil eq',
                    'water_consumption': 'm3'
                }
            }
        }

