from typing import Dict,  Any
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

class TechnicalIntegrator:
    """
    Integrates technical analysis components with FastAPI.
    
    This class coordinates between:
    1. FastAPI endpoints for protein analysis
    2. Python-based analysis components
    
    The integrator ensures no duplication of logic while maintaining 
    high performance through optimized Python calculations.
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8001/api/v1/technical/protein-analysis"):
        """
        Initialize the technical integrator with API components.
        
        Args:
            api_base_url: Base URL for FastAPI endpoints
        """
        # Initialize FastAPI client
        self.client = httpx.AsyncClient()
        self.api_base_url = api_base_url
        
        logger.info("TechnicalIntegrator initialized successfully")

    async def analyze_technical(self, process_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate complete technical analysis using FastAPI endpoints.
        
        Args:
            process_data: Dictionary containing process parameters and measurements
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        try:
            logger.debug(f"Starting technical analysis with data: {process_data}")
            
            # Extract process parameters
            params = self._extract_process_parameters(process_data)
            
            # Parallel execution of analysis tasks
            recovery_task = self.analyze_protein_recovery(params['recovery_params'])
            separation_task = self.analyze_separation_efficiency(params['separation_params'])
            particle_task = self.analyze_particle_size(params['particle_params']) if params['particle_params'] else None
            
            # Gather results
            results = await asyncio.gather(recovery_task, separation_task)
            recovery_results, separation_results = results
            
            # Add particle analysis if available
            particle_results = await particle_task if particle_task else {}
            
            return self._compile_analysis_results(
                recovery_results, 
                separation_results, 
                particle_results,
                params['process_params']
            )
            
        except Exception as e:
            logger.error(f"Technical analysis failed: {str(e)}")
            raise RuntimeError(f"Technical analysis failed: {str(e)}")

    def _extract_process_parameters(self, process_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Extract and organize process parameters for analysis"""
        process_params = process_data.get("process_parameters", {})
        material_props = process_data.get("material_properties", {})
        operating_conds = process_data.get("operating_conditions", {})
        
        recovery_params = {
            "input_mass": process_params.get("feed_rate", 0) * operating_conds.get("processing_time", 0),
            "output_mass": process_params.get("output_mass", 0),
            "initial_protein_content": material_props.get("initial_protein_content", 0),
            "output_protein_content": material_props.get("final_protein_content", 0)
        }
        
        separation_params = {
            "feed_composition": {
                "protein": material_props.get("initial_protein_content", 0),
                "moisture": material_props.get("initial_moisture", 0)
            },
            "product_composition": {
                "protein": material_props.get("final_protein_content", 0),
                "moisture": material_props.get("final_moisture", 0)
            },
            "mass_flow": {
                "input": process_params.get("feed_rate", 0),
                "output": process_params.get("output_rate", 0)
            }
        }
        
        particle_params = None
        if "particle_size" in material_props:
            particle_data = material_props["particle_size"]
            particle_params = {
                "particle_sizes": [
                    particle_data.get("d10", 0),
                    particle_data.get("d50", 0),
                    particle_data.get("d90", 0)
                ]
            }
        
        return {
            "recovery_params": recovery_params,
            "separation_params": separation_params,
            "particle_params": particle_params,
            "process_params": process_params
        }

    async def analyze_protein_recovery(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate protein recovery using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/recovery/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Protein recovery API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Protein recovery analysis failed: {str(e)}")
            raise RuntimeError(f"Protein recovery analysis failed: {str(e)}")

    async def analyze_separation_efficiency(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate separation efficiency using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/separation/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Separation efficiency API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Separation efficiency analysis failed: {str(e)}")
            raise RuntimeError(f"Separation efficiency analysis failed: {str(e)}")

    async def analyze_particle_size(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Analyze particle size distribution using FastAPI endpoint"""
        try:
            response = await self.client.post(
                f"{self.api_base_url}/particle-size/",
                json=process_data
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Particle size API call failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            logger.error(f"Particle size analysis failed: {str(e)}")
            raise RuntimeError(f"Particle size analysis failed: {str(e)}")

    def _compile_analysis_results(
        self,
        recovery_results: Dict[str, float],
        separation_results: Dict[str, float],
        particle_results: Dict[str, float],
        process_params: Dict[str, float]
    ) -> Dict[str, Any]:
        """Compile all analysis results into a single response"""
        return {
            "protein_recovery": recovery_results,
            "separation_efficiency": separation_results,
            "particle_analysis": particle_results,
            "process_parameters": {
                "feed_rate_actual": process_params.get("feed_rate", 0),
                "air_flow_actual": process_params.get("air_flow_rate", 0),
                "classifier_efficiency": process_params.get("classifier_speed", 0)
            }
        }
