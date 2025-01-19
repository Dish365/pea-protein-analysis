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
    
    @retry(stop=stop_after_attempt(settings.FASTAPI_RETRY_COUNT),
           wait=wait_exponential(multiplier=0.5, min=1, max=10))
    async def analyze_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze process using integrators and FastAPI endpoints
        """
        try:
            logger.info(f"Starting process analysis for type: {data.get('process_type')}")
            
            # Run analyses in parallel
            technical_task = self.technical_integrator.analyze_technical(
                self._prepare_technical_data(data)
            )
            economic_task = self.economic_integrator.analyze_economics(
                self._prepare_economic_data(data)
            )
            environmental_task = self.environmental_integrator.analyze_environmental_impacts(
                self._prepare_environmental_data(data)
            )
            
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
                    raise result
                    
            technical_results, economic_results, environmental_results = results
            
            # Prepare data for eco-efficiency analysis
            efficiency_data = await self._prepare_efficiency_data(
                technical_results,
                economic_results,
                environmental_results,
                data
            )
            
            # Get eco-efficiency analysis
            efficiency_results = await self._analyze_efficiency(efficiency_data)
            
            # Compile final results
            final_results = self._compile_final_results(
                technical_results,
                economic_results,
                environmental_results,
                efficiency_results
            )
            
            logger.info("Process analysis completed successfully")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in process analysis: {str(e)}", exc_info=True)
            raise
    
    def _prepare_technical_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for technical analysis"""
        return {
            "process_parameters": {
                "feed_rate": data["input_mass"],
                "output_mass": data["output_mass"],
                "process_type": data["process_type"]
            },
            "material_properties": {
                "initial_protein_content": data["initial_protein_content"],
                "final_protein_content": data["final_protein_content"],
                "initial_moisture_content": data["initial_moisture_content"],
                "final_moisture_content": data["final_moisture_content"],
                "particle_size": {
                    "d10": data["d10_particle_size"],
                    "d50": data["d50_particle_size"],
                    "d90": data["d90_particle_size"]
                }
            },
            "operating_conditions": {
                "processing_time": 1.0,  # Default to 1 hour for rate calculations
                "electricity_consumption": data["electricity_consumption"],
                "cooling_consumption": data["cooling_consumption"]
            }
        }
    
    def _prepare_economic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for economic analysis"""
        return {
            "equipment": {
                "cost": data["equipment_cost"],
                "maintenance_factor": data["maintenance_cost"] / data["equipment_cost"]
            },
            "operating_costs": {
                "raw_materials": {
                    "unit_cost": data["raw_material_cost"],
                    "annual_consumption": data["input_mass"] * data["production_volume"]
                },
                "utilities": {
                    "electricity_cost": data["utility_cost"],
                    "annual_consumption": data["electricity_consumption"] * data["production_volume"]
                },
                "labor": {
                    "hourly_cost": data["labor_cost"],
                    "annual_hours": 8760  # Assuming 24/7 operation
                }
            },
            "project_parameters": {
                "duration": data["project_duration"],
                "discount_rate": data["discount_rate"],
                "production_volume": data["production_volume"]
            }
        }
    
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
    
    async def _prepare_efficiency_data(self,
                                     technical_results: Dict[str, Any],
                                     economic_results: Dict[str, Any],
                                     environmental_results: Dict[str, Any],
                                     input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for eco-efficiency analysis"""
        try:
            # Extract required metrics from results
            tech_metrics = technical_results.get("technical_results", {})
            econ_metrics = economic_results.get("economic_analysis", {})
            env_metrics = environmental_results.get("environmental_results", {})
            
            return {
                "economic_data": {
                    "capex": {
                        "equipment_cost": economic_results["capex_analysis"]["equipment_cost"],
                        "installation_cost": economic_results["capex_analysis"]["installation_cost"],
                        "indirect_cost": economic_results["capex_analysis"]["indirect_cost"],
                        "total_capex": economic_results["capex_analysis"]["total_capex"]
                    },
                    "opex": {
                        "utilities_cost": economic_results["opex_analysis"]["utilities_cost"],
                        "materials_cost": economic_results["opex_analysis"]["materials_cost"],
                        "labor_cost": economic_results["opex_analysis"]["labor_cost"],
                        "maintenance_cost": economic_results["opex_analysis"]["maintenance_cost"],
                        "total_opex": economic_results["opex_analysis"]["total_opex"]
                    },
                    "npv": economic_results["profitability_analysis"]["metrics"]["npv"],
                    "roi": economic_results["profitability_analysis"]["metrics"]["roi"],
                    "payback_period": economic_results["profitability_analysis"]["metrics"]["payback_period"],
                    "profitability_index": economic_results["profitability_analysis"]["metrics"]["profitability_index"],
                    "sensitivity_analysis": economic_results["sensitivity_analysis"]
                },
                "quality_metrics": {
                    "protein_recovery": tech_metrics["protein_recovery"],
                    "separation_efficiency": tech_metrics["separation_efficiency"],
                    "process_efficiency": tech_metrics["process_efficiency"],
                    "particle_size_distribution": tech_metrics["particle_size_distribution"]
                },
                "environmental_impacts": {
                    "gwp": env_metrics["gwp"],
                    "hct": env_metrics["hct"],
                    "frs": env_metrics["frs"],
                    "water_consumption": env_metrics["water_consumption"],
                    "allocated_impacts": env_metrics["allocated_impacts"]
                },
                "resource_inputs": {
                    "energy_consumption": input_data["electricity_consumption"] + input_data["cooling_consumption"],
                    "water_usage": input_data["water_consumption"],
                    "raw_material_input": input_data["input_mass"]
                },
                "process_type": input_data["process_type"]
            }
            
        except KeyError as e:
            logger.error(f"Missing required data for efficiency analysis: {str(e)}")
            raise ValueError(f"Missing required data for efficiency analysis: {str(e)}")
    
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
                
            return {
                "efficiency_metrics": {
                    "economic_indicators": result["efficiency_metrics"]["economic_indicators"],
                    "quality_indicators": result["efficiency_metrics"]["quality_indicators"],
                    "efficiency_metrics": result["efficiency_metrics"]["efficiency_metrics"]
                },
                "performance_indicators": {
                    "eco_efficiency_index": result["performance_indicators"]["eco_efficiency_index"],
                    "relative_performance": result["performance_indicators"]["relative_performance"]
                },
                "rust_calculations": result.get("rust_calculations", {})
            }
            
        except httpx.HTTPError as e:
            logger.error(f"Eco-efficiency analysis failed: {str(e)}")
            raise RuntimeError(f"Eco-efficiency analysis failed: {str(e)}")
    
    def _compile_final_results(self,
                             technical_results: Dict[str, Any],
                             economic_results: Dict[str, Any],
                             environmental_results: Dict[str, Any],
                             efficiency_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compile all analysis results into final format"""
        return {
            "technical_analysis": technical_results.get("technical_results", {}),
            "economic_analysis": {
                "capex": economic_results.get("capex_analysis", {}),
                "opex": economic_results.get("opex_analysis", {}),
                "profitability": economic_results.get("profitability_analysis", {}),
                "sensitivity": economic_results.get("sensitivity_analysis", {})
            },
            "environmental_analysis": environmental_results.get("environmental_results", {}),
            "eco_efficiency_analysis": {
                "metrics": efficiency_results.get("efficiency_metrics", {}),
                "performance": efficiency_results.get("performance_indicators", {}),
                "rust_analysis": efficiency_results.get("rust_calculations", {})
            }
        }
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        # Close integrator clients
        await self.technical_integrator.client.aclose()
        await self.economic_integrator.client.aclose()
        await self.environmental_integrator.client.aclose() 