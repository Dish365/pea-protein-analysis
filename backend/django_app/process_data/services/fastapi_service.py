import httpx
from typing import Dict, Any
import logging
import asyncio
from django.conf import settings
from analytics.pipeline.integrator.technical import TechnicalIntegrator
from analytics.pipeline.integrator.economic import EconomicIntegrator
from analytics.pipeline.integrator.environmental import EnvironmentalIntegrator
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class FastAPIService:
    def __init__(self):
        self.base_url = settings.FASTAPI_BASE_URL
        self.timeout = settings.FASTAPI_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
        
        # Initialize integrators without redundant URLs
        self.technical_integrator = TechnicalIntegrator()
        self.economic_integrator = EconomicIntegrator()
        self.environmental_integrator = EnvironmentalIntegrator()
        
        logger.info("FastAPI service initialized with integrators")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        await self.technical_integrator.client.aclose()
        await self.economic_integrator.client.aclose()
        await self.environmental_integrator.client.aclose()
    
    @retry(stop=stop_after_attempt(settings.FASTAPI_RETRY_COUNT),
           wait=wait_exponential(multiplier=0.5, min=1, max=10),
           retry=lambda e: isinstance(e, (httpx.ConnectError, httpx.TimeoutException)))
    async def analyze_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze process using integrators and FastAPI endpoints
        """
        try:
            logger.info(f"Starting process analysis for type: {data.get('process_type')}")
            
            # Prepare data for each analysis
            technical_data = self._prepare_technical_data(data)
            economic_data = self._prepare_economic_data(data)
            environmental_data = self._prepare_environmental_data(data)
            
            # Run analyses in parallel
            technical_task = self.technical_integrator.analyze_technical(technical_data)
            economic_task = self.economic_integrator.analyze_economics(economic_data)
            environmental_task = self.environmental_integrator.analyze_environmental_impacts(environmental_data)
            
            # Wait for all analyses to complete
            results = await asyncio.gather(
                technical_task, economic_task, environmental_task,
                return_exceptions=True
            )
            
            # Check for exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    analysis_type = ['technical', 'economic', 'environmental'][i]
                    logger.error(f"Error in {analysis_type} analysis: {str(result)}")
                    # Don't wrap the exception in RuntimeError if it's already a RuntimeError
                    if isinstance(result, RuntimeError):
                        raise result
                    raise RuntimeError(f"Error in {analysis_type} analysis: {str(result)}")
                    
            technical_results, economic_results, environmental_results = results
            
            # Prepare data for eco-efficiency analysis
            efficiency_data = {
                "economic_data": {
                    "capex": economic_results.get('capex_analysis', {}),
                    "opex": economic_results.get('opex_analysis', {}),
                    "profitability": economic_results.get('profitability_analysis', {})
                },
                "quality_metrics": technical_results.get('technical_results', {}),
                "environmental_impacts": environmental_results.get('environmental_results', {}),
                "resource_inputs": {
                    "energy_consumption": data.get('electricity_consumption', 0) + data.get('cooling_consumption', 0),
                    "water_usage": data.get('water_consumption', 0),
                    "raw_material_input": data.get('input_mass', 0)
                },
                "process_type": data.get('process_type', 'baseline')
            }
            
            try:
                # Get eco-efficiency analysis with its own retry mechanism
                efficiency_results = await self._analyze_efficiency(efficiency_data)
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                # Re-raise retryable errors to trigger retry at analyze_process level
                raise
            
            # Compile final results
            final_results = {
                'technical_results': technical_results.get('technical_results', {}),
                'economic_analysis': economic_results,
                'environmental_results': {
                    'environmental_results': environmental_results.get('environmental_results', {})
                },
                'efficiency_results': efficiency_results
            }
            
            logger.info("Process analysis completed successfully")
            return final_results
            
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # Log and re-raise retryable errors without wrapping
            logger.warning(f"Retryable error in process analysis: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in process analysis: {str(e)}", exc_info=True)
            # Don't wrap the exception in RuntimeError if it's already a RuntimeError
            if isinstance(e, RuntimeError):
                raise e
            raise RuntimeError(str(e))
    
    def _prepare_technical_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for technical analysis.
        Validates and transforms process data for the technical integrator.
        """
        # Validate required fields
        required_fields = [
            "input_mass", "output_mass", 
            "initial_protein_content", "final_protein_content",
            "initial_moisture_content", "final_moisture_content",
            "process_type"
        ]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields for technical analysis: {', '.join(missing_fields)}")

        # Validate numeric values
        if data["output_mass"] > data["input_mass"]:
            raise ValueError("Output mass cannot exceed input mass")
        
        if not (0 < data["initial_protein_content"] <= 100 and 0 < data["final_protein_content"] <= 100):
            raise ValueError("Protein content must be between 0 and 100%")
            
        # Validate moisture content
        if data["final_moisture_content"] > data["initial_moisture_content"]:
            raise ValueError("Final moisture content cannot be higher than initial moisture content")

        # Prepare separation data
        feed_composition = {
            "protein": data["initial_protein_content"],
            "moisture": data["initial_moisture_content"],
            "other": max(0, 100 - data["initial_protein_content"] - data["initial_moisture_content"])
        }
        
        product_composition = {
            "protein": data["final_protein_content"],
            "moisture": data["final_moisture_content"],
            "other": max(0, 100 - data["final_protein_content"] - data["final_moisture_content"])
        }
        
        separation_data = {
            "feed_composition": feed_composition,
            "product_composition": product_composition,
            "mass_flow": {
                "input": data["input_mass"],
                "output": data["output_mass"]
            }
        }

        # Add process data if multi-stage analysis is needed
        if data.get("process_stages"):
            separation_data["process_data"] = data["process_stages"]
            separation_data["target_purity"] = data.get("target_protein_content")

        return {
            # Recovery data
            "input_mass": data["input_mass"],
            "output_mass": data["output_mass"],
            "initial_protein_content": data["initial_protein_content"],
            "final_protein_content": data["final_protein_content"],  # Keep original field name
            "output_protein_content": data["final_protein_content"],  # Add mapped field for API
            "process_type": data["process_type"],
            
            # Separation data
            "separation_data": separation_data,
            
            # Particle data
            "particle_data": {
                "sizes": data.get("particle_sizes", []),
                "weights": data.get("particle_weights", []),
                "percentiles": {
                    "d10": data["d10_particle_size"],
                    "d50": data["d50_particle_size"],
                    "d90": data["d90_particle_size"]
                },
                "density": data.get("particle_density", 1.5),
                "initial_moisture": data["initial_moisture_content"],
                "final_moisture": data["final_moisture_content"]
            }
        }
    
    def _prepare_economic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare data for economic analysis.
        Structures data to match FastAPI endpoint models.
        """
        try:
            # Validate required fields
            required_fields = [
                "equipment_cost", "maintenance_cost", "raw_material_cost",
                "utility_cost", "labor_cost", "project_duration",
                "discount_rate", "production_volume", "electricity_consumption"
            ]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValueError(f"Missing required fields for economic analysis: {', '.join(missing_fields)}")

            # Extract project parameters with validation
            project_params = {
                "duration": data["project_duration"],
                "discount_rate": data["discount_rate"],
                "production_volume": data["production_volume"]
            }
            
            # Create economic factors with validation
            economic_factors = {
                "installation_factor": data.get("installation_factor", 0.2),
                "indirect_costs_factor": data.get("indirect_costs_factor", 0.15),
                "maintenance_factor": data.get("maintenance_factor", 0.05),
                "project_duration": project_params["duration"],
                "discount_rate": project_params["discount_rate"],
                "production_volume": project_params["production_volume"]
            }
            
            # Equipment data with validation
            equipment = [{
                "name": "main_equipment",
                "cost": data["equipment_cost"],
                "efficiency": data.get("equipment_efficiency", 0.85),
                "maintenance_cost": data["maintenance_cost"],
                "energy_consumption": data["electricity_consumption"],
                "processing_capacity": data["production_volume"]
            }]
            
            # Utilities with validation
            utilities = []
            if data.get("electricity_consumption"):
                utilities.append({
                    "name": "electricity",
                    "consumption": data["electricity_consumption"],
                    "unit_price": data["utility_cost"],
                    "unit": "kWh"
                })
            if data.get("cooling_consumption"):
                utilities.append({
                    "name": "cooling",
                    "consumption": data["cooling_consumption"],
                    "unit_price": data["utility_cost"],
                    "unit": "kWh"
                })
            if data.get("water_consumption"):
                utilities.append({
                    "name": "water",
                    "consumption": data["water_consumption"],
                    "unit_price": data["utility_cost"],
                    "unit": "kg"
                })

            # Raw materials with validation
            raw_materials = [{
                "name": "feed_material",
                "quantity": data["input_mass"],
                "unit_price": data["raw_material_cost"],
                "unit": "kg"
            }]
            
            # Labor configuration with validation
            labor_config = {
                "hourly_wage": data["labor_cost"],
                "hours_per_week": data.get("hours_per_week", 40),
                "weeks_per_year": data.get("weeks_per_year", 52),
                "num_workers": data.get("num_workers", 1)
            }

            # Calculate costs
            capex = {
                "total_investment": data["equipment_cost"] * (1 + economic_factors["installation_factor"]),
                "equipment_cost": data["equipment_cost"],
                "installation_cost": data["equipment_cost"] * economic_factors["installation_factor"],
                "indirect_cost": data["equipment_cost"] * economic_factors["indirect_costs_factor"]
            }

            # Calculate annual costs
            annual_utility_cost = sum(util["consumption"] * util["unit_price"] for util in utilities)
            annual_material_cost = data["input_mass"] * data["raw_material_cost"]
            annual_labor_cost = (
                labor_config["hourly_wage"] 
                * labor_config["hours_per_week"] 
                * labor_config["weeks_per_year"] 
                * labor_config["num_workers"]
            )
            maintenance_cost = data["equipment_cost"] * economic_factors["maintenance_factor"]

            opex = {
                "total_annual_cost": annual_utility_cost + annual_material_cost + annual_labor_cost + maintenance_cost,
                "utilities_cost": annual_utility_cost,
                "materials_cost": annual_material_cost,
                "labor_cost": annual_labor_cost,
                "maintenance_cost": maintenance_cost
            }

            return {
                "equipment": equipment,
                "utilities": utilities,
                "raw_materials": raw_materials,
                "labor_config": labor_config,
                "project_parameters": project_params,
                "process_type": data.get("process_type", "baseline"),
                "economic_factors": economic_factors,
                "capex": capex,
                "opex": opex,
                "monte_carlo_iterations": data.get("monte_carlo_iterations", 1000),
                "uncertainty": data.get("uncertainty", 0.1),
                "revenue": data.get("revenue", []),
                "cash_flows": []  # Will be calculated by profitability analyzer
            }

        except Exception as e:
            logger.error(f"Error preparing economic data: {str(e)}", exc_info=True)
            raise ValueError(f"Error preparing economic data: {str(e)}")
    
    def _prepare_environmental_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for environmental analysis"""
        return {
            "energy_consumption": {
                "electricity": data["electricity_consumption"],
                "cooling": data["cooling_consumption"]
            },
            "water_consumption": data["water_consumption"],
            "process_type": data["process_type"],
            "production_data": {
                "input_mass": data["input_mass"],
                "output_mass": data["output_mass"],
                "production_volume": data["production_volume"]
            }
        }
    
    @retry(stop=stop_after_attempt(settings.FASTAPI_RETRY_COUNT),
           wait=wait_exponential(multiplier=0.5, min=1, max=10),
           retry=lambda e: isinstance(e, (httpx.ConnectError, httpx.TimeoutException)))
    async def _analyze_efficiency(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to eco-efficiency analysis endpoint"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/environmental/eco-efficiency/calculate",
                json=data,
                timeout=settings.PROCESS_ANALYSIS.get('EFFICIENCY_TIMEOUT', self.timeout)
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Eco-efficiency analysis completed: {result}")
            
            # Ensure the response matches our expected structure
            if not all(key in result for key in ["efficiency_metrics", "performance_indicators"]):
                raise ValueError("Invalid response structure from eco-efficiency endpoint")
                
            return result
            
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # Log and re-raise retryable errors
            logger.warning(f"Retryable error in eco-efficiency analysis: {str(e)}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"HTTP error in eco-efficiency analysis: {str(e)}")
            raise RuntimeError(f"HTTP error in eco-efficiency analysis: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in eco-efficiency analysis: {str(e)}")
            raise RuntimeError(f"Unexpected error in eco-efficiency analysis: {str(e)}")
    
    async def _store_results(self,
                           process_id: int,
                           technical_results: Dict[str, Any],
                           economic_results: Dict[str, Any],
                           environmental_results: Dict[str, Any],
                           efficiency_results: Dict[str, Any]) -> None:
        """Store analysis results in the database"""
        from process_data.models import AnalysisResult
        
        await AnalysisResult.objects.acreate(
            process_id=process_id,
            technical_results=technical_results,
            economic_results=economic_results,
            environmental_results=environmental_results,
            efficiency_results=efficiency_results
        )
    
    async def _update_status(self,
                           process_id: int,
                           status: str,
                           progress: int) -> None:
        """Update process status and progress"""
        from process_data.models import ProcessAnalysis
        
        await ProcessAnalysis.objects.filter(id=process_id).aupdate(
            status=status,
            progress=progress
        ) 