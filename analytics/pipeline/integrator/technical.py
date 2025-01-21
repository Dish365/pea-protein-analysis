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
        # Extract protein content values with proper fallbacks
        initial_protein = process_data.get("initial_protein_content", 0)
        final_protein = process_data.get("final_protein_content", 0)
        initial_moisture = process_data.get("initial_moisture_content", 0)
        final_moisture = process_data.get("final_moisture_content", 0)
        
        recovery_params = {
            "input_mass": process_data.get("input_mass", 0),
            "output_mass": process_data.get("output_mass", 0),
            "initial_protein_content": initial_protein,
            "output_protein_content": final_protein,
            "process_type": process_data.get("process_type", "baseline")
        }
        
        feed_composition = {
            "protein": initial_protein,
            "moisture": initial_moisture,
            "other": max(0, 100 - initial_protein - initial_moisture)
        }
        
        product_composition = {
            "protein": final_protein,
            "moisture": final_moisture,
            "other": max(0, 100 - final_protein - final_moisture)
        }
        
        mass_flow = {
            "input": process_data.get("input_mass", 0),
            "output": process_data.get("output_mass", 0)
        }
        
        separation_params = {
            "separation_data": {
                "feed_composition": feed_composition,
                "product_composition": product_composition,
                "mass_flow": mass_flow
            }
        }

        # Extract particle size parameters with validation
        particle_params = None
        has_particle_data = all(key in process_data for key in ["d10_particle_size", "d50_particle_size", "d90_particle_size"])
        
        if has_particle_data:
            # Get full particle size distribution if available
            particle_sizes = process_data.get("particle_sizes", [])
            particle_weights = process_data.get("particle_weights", None)
            
            # If no full distribution, create one from percentiles
            if not particle_sizes:
                particle_sizes = [
                    process_data["d10_particle_size"],
                    process_data["d50_particle_size"],
                    process_data["d90_particle_size"]
                ]
            
            # Prepare target ranges if any target values are provided
            target_ranges = None
            target_keys = [
                ("D10", "target_d10_min", "target_d10_max"),
                ("D50", "target_d50_min", "target_d50_max"),
                ("D90", "target_d90_min", "target_d90_max"),
                ("span", "target_span_min", "target_span_max"),
                ("cv", "target_cv_min", "target_cv_max")
            ]
            
            if any(min_key in process_data or max_key in process_data 
                  for _, min_key, max_key in target_keys):
                target_ranges = {}
                for key, min_key, max_key in target_keys:
                    if min_key in process_data or max_key in process_data:
                        min_val = process_data.get(min_key, 0)
                        max_val = process_data.get(max_key, 10000 if key in {"D10", "D50", "D90"} else 100)
                        target_ranges[key] = (min_val, max_val)
            
            particle_params = {
                "particle_sizes": particle_sizes,
                "weights": particle_weights,
                "density": process_data.get("particle_density", 1.5),  # Default protein density
                "initial_moisture": initial_moisture,
                "final_moisture": final_moisture,
                "treatment_type": process_data.get("process_type", "baseline"),
                "target_ranges": target_ranges
            }
        
        return {
            "recovery_params": recovery_params,
            "separation_params": separation_params,
            "particle_params": particle_params,
            "process_params": {
                "feed_rate": process_data.get("input_mass", 0),
                "air_flow_rate": process_data.get("air_flow", 0),
                "classifier_speed": process_data.get("classifier_speed", 0)
            }
        }

    async def analyze_protein_recovery(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate protein recovery using FastAPI endpoint"""
        try:
            # Validate required fields
            required_fields = ["input_mass", "output_mass", "initial_protein_content", "output_protein_content", "process_type"]
            missing_fields = [field for field in required_fields if field not in process_data]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate numeric fields are positive
            numeric_fields = ["input_mass", "output_mass", "initial_protein_content", "output_protein_content"]
            for field in numeric_fields:
                if process_data[field] <= 0:
                    raise ValueError(f"{field} must be positive")

            # Validate protein content percentages
            for field in ["initial_protein_content", "output_protein_content"]:
                if not 0 < process_data[field] <= 100:
                    raise ValueError(f"{field} must be between 0 and 100%")

            # Validate mass conservation
            if process_data["output_mass"] > process_data["input_mass"]:
                raise ValueError("Output mass cannot exceed input mass")

            # Make API call
            response = await self.client.post(
                f"{self.api_base_url}/recovery/",
                json=process_data
            )
            
            if response.status_code != 200:
                error_detail = response.json().get("detail", response.text)
                raise RuntimeError(f"Protein recovery API call failed: {error_detail}")
                
            return response.json()
            
        except ValueError as ve:
            logger.error(f"Validation error in protein recovery analysis: {str(ve)}")
            raise RuntimeError(f"Protein recovery validation failed: {str(ve)}")
        except Exception as e:
            logger.error(f"Protein recovery analysis failed: {str(e)}")
            raise RuntimeError(f"Protein recovery analysis failed: {str(e)}")

    async def analyze_separation_efficiency(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate separation efficiency using FastAPI endpoint"""
        try:
            # Extract separation data
            if "separation_data" not in process_data:
                raise ValueError("Missing separation data in process data")
                
            separation_data = process_data["separation_data"]
            
            # Validate required fields
            required_fields = ["feed_composition", "product_composition", "mass_flow"]
            missing_fields = [field for field in required_fields if field not in separation_data]
            if missing_fields:
                raise ValueError(f"Missing required fields in separation data: {', '.join(missing_fields)}")
            
            # Validate compositions
            for comp_type in ["feed_composition", "product_composition"]:
                composition = separation_data[comp_type]
                if "protein" not in composition:
                    raise ValueError(f"Missing protein content in {comp_type}")
                total = sum(composition.values())
                if not (99.5 <= total <= 100.5):
                    raise ValueError(f"{comp_type} percentages must sum to approximately 100% (got {total}%)")
            
            # Validate mass flows
            mass_flow = separation_data["mass_flow"]
            if mass_flow["output"] > mass_flow["input"]:
                raise ValueError("Output mass cannot exceed input mass")
            if any(flow <= 0 for flow in mass_flow.values()):
                raise ValueError("Mass flows must be positive")
            
            response = await self.client.post(
                f"{self.api_base_url}/separation/",
                json=separation_data
            )
            
            if response.status_code != 200:
                error_detail = response.json().get("detail", response.text)
                raise RuntimeError(f"Separation efficiency API call failed: {error_detail}")
                
            result = response.json()
            
            # Validate required fields in response
            required_fields = ["separation_efficiency", "component_recoveries"]
            if not all(field in result for field in required_fields):
                raise RuntimeError("Incomplete separation efficiency results")
                
            return result
            
        except Exception as e:
            logger.error(f"Separation efficiency analysis failed: {str(e)}")
            raise RuntimeError(f"Separation efficiency analysis failed: {str(e)}")

    async def analyze_particle_size(self, process_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyze particle size distribution using FastAPI endpoint.
        
        Args:
            process_data: Dictionary containing:
                - particle_sizes: List of particle sizes in μm
                - weights: Optional weights for each size
                - density: Optional particle density in g/cm³
                - initial_moisture: Initial moisture content percentage
                - final_moisture: Optional final moisture content percentage
                - treatment_type: Optional pre-treatment type
                - target_ranges: Optional target ranges for quality evaluation
                
        Returns:
            Dictionary containing:
                - Distribution metrics (D10, D50, D90, span, cv)
                - Surface area calculations (if density provided)
                - Quality scores (if target ranges provided)
                - Moisture status
        """
        if not process_data:
            logger.debug("No particle size data provided, skipping analysis")
            return {}
            
        try:
            # Validate required fields
            if "particle_sizes" not in process_data:
                raise ValueError("Particle sizes are required for analysis")
            if "initial_moisture" not in process_data:
                raise ValueError("Initial moisture content is required")
                
            # Validate numeric arrays
            particle_sizes = process_data["particle_sizes"]
            if not particle_sizes or len(particle_sizes) < 2:
                raise ValueError("At least 2 particle sizes are required")
            if not all(isinstance(x, (int, float)) and x > 0 for x in particle_sizes):
                raise ValueError("All particle sizes must be positive numbers")
            if any(x > 10000 for x in particle_sizes):
                raise ValueError("Particle sizes cannot exceed 10000 μm")
                
            # Validate weights if provided
            weights = process_data.get("weights")
            if weights is not None:
                if len(weights) != len(particle_sizes):
                    raise ValueError("Number of weights must match number of particle sizes")
                if not all(isinstance(x, (int, float)) and x >= 0 for x in weights):
                    raise ValueError("All weights must be non-negative numbers")
                    
            # Validate density if provided
            density = process_data.get("density")
            if density is not None:
                if not isinstance(density, (int, float)) or density <= 0 or density >= 10:
                    raise ValueError("Density must be a positive number less than 10 g/cm³")
                    
            # Make API call
            response = await self.client.post(
                f"{self.api_base_url}/particle-size/",
                json=process_data
            )
            
            if response.status_code != 200:
                error_detail = response.json().get("detail", response.text)
                raise RuntimeError(f"Particle size API call failed: {error_detail}")
                
            result = response.json()
            
            # Validate response data
            required_metrics = {"D10", "D50", "D90", "mean", "std_dev"}
            if not all(key in result for key in required_metrics):
                raise RuntimeError("Incomplete particle size analysis results")
                
            return result
            
        except ValueError as ve:
            logger.error(f"Validation error in particle size analysis: {str(ve)}")
            raise RuntimeError(f"Particle size validation failed: {str(ve)}")
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
        """Compile all analysis results into a single response matching Django model structure"""
        
        # Extract separation metrics
        separation_metrics = {
            "separation_efficiency": separation_results.get("separation_efficiency", 0),
            "component_recoveries": separation_results.get("component_recoveries", {}),
        }
        
        # Add process performance metrics if available
        if "cumulative_efficiency" in separation_results:
            separation_metrics.update({
                "process_performance": {
                    "cumulative_efficiency": separation_results["cumulative_efficiency"],
                    "average_step_efficiency": separation_results.get("average_step_efficiency"),
                    "purity_achievement": separation_results.get("purity_achievement"),
                }
            })
            
        # Add stage analysis if available
        if "stage_analysis" in separation_results:
            separation_metrics["stage_analysis"] = separation_results["stage_analysis"]
        
        return {
            "technical_results": {
                "protein_recovery": recovery_results.get("protein_recovery", 0),
                "separation_efficiency": separation_metrics,
                "process_efficiency": (
                    recovery_results.get("protein_recovery", 0) * 
                    separation_metrics["separation_efficiency"] / 100
                ),
                "particle_metrics": {
                    "d10": particle_results.get("D10", 0),
                    "d50": particle_results.get("D50", 0),
                    "d90": particle_results.get("D90", 0),
                    "span": particle_results.get("span", 0),
                    "cv": particle_results.get("cv", 0),
                    "surface_area": particle_results.get("specific_surface_area", 0),
                    "quality_score": particle_results.get("overall", 0)
                } if particle_results else None,
                "moisture_status": particle_results.get("moisture_status", {})
            },
            "process_parameters": {
                "feed_rate": process_params.get("feed_rate", 0),
                "air_flow": process_params.get("air_flow_rate", 0),
                "classifier_speed": process_params.get("classifier_speed", 0)
            },
            "metadata": {
                "units": {
                    "protein_recovery": "%",
                    "separation_efficiency": "%",
                    "process_efficiency": "%",
                    "particle_size": "μm",
                    "surface_area": "cm²/g",
                    "feed_rate": "kg/h",
                    "air_flow": "m³/h",
                    "classifier_speed": "rpm"
                }
            }
        }
