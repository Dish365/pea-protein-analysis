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
        """Extract and organize process parameters for analysis"""
        impact_params = {
            'energy_consumption': {
                'electricity': process_data.get('electricity_kwh', 0),
                'cooling': process_data.get('cooling_kwh', 0)
            },
            'water_consumption': process_data.get('water_kg', 0),
            'emission_factors': process_data.get('emission_factors', {}),
            'process_type': process_data.get('process_type', 'baseline')
        }
        
        allocation_params = {
            'product_values': process_data.get('product_values', {}),
            'mass_flows': process_data.get('mass_flows', {}),
            'method': process_data.get('allocation_method', 'hybrid'),
            'hybrid_weights': process_data.get('hybrid_weights')
        }
        
        return {
            'impact_params': impact_params,
            'allocation_params': allocation_params
        }

    async def calculate_impacts(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate environmental impacts using impact endpoints"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/impact/calculate",
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
        """Compile all analysis results into a single response"""
        return {
            'status': 'success',
            'impact_assessment': {
                'gwp': impact_results.get('impacts', {}).get('gwp'),
                'hct': impact_results.get('impacts', {}).get('hct'),
                'frs': impact_results.get('impacts', {}).get('frs'),
                'water_consumption': impact_results.get('impacts', {}).get('water_consumption')
            },
            'allocation_results': {
                'method': allocation_results.get('method'),
                'allocated_impacts': allocation_results.get('allocated_impacts', {}),
                'allocation_factors': allocation_results.get('allocation_factors', {})
            },
            'metadata': {
                'process_type': impact_results.get('process_type'),
                'calculation_timestamp': impact_results.get('timestamp')
            }
        }

