import httpx
from typing import Dict, Any, Tuple, List
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
                    raise RuntimeError(f"Error in {analysis_type} analysis: {str(result)}")
                    
            technical_results, economic_results, environmental_results = results
            
            # Prepare data for eco-efficiency analysis
            production_volume = data.get('production_volume', 1000.0)  # Get production volume once
            input_mass = data.get('input_mass', production_volume)
            output_mass = data.get('output_mass', input_mass * 0.8)  # Assume 80% yield if not specified
            
            # Calculate product streams based on mass balance
            main_product_volume = max(0.1, output_mass)  # Ensure non-zero main product volume
            waste_volume = max(0.0, input_mass - output_mass)  # Ensure non-negative waste volume
            
            # Get economic values with validation and logging
            economic_defaults, economic_values = self._validate_and_extract_metrics(economic_results, 'economic')
            
            # Get technical values with validation and logging
            technical_defaults, technical_values = self._validate_and_extract_metrics(technical_results, 'technical')
            
            # Get environmental values with validation and logging
            environmental_defaults, env_values = self._validate_and_extract_metrics(environmental_results, 'environmental')
            
            # Log warnings for default usage
            if economic_defaults:
                logger.warning(f"Using default values for economic metrics: {', '.join(economic_defaults)}")
            if technical_defaults:
                logger.warning(f"Using default values for technical metrics: {', '.join(technical_defaults)}")
            if environmental_defaults:
                logger.warning(f"Using default values for environmental metrics: {', '.join(environmental_defaults)}")
            
            # Log actual calculated values
            logger.info(
                f"Using calculated economic values - CAPEX: {economic_values['total_capex']}, "
                f"OPEX: {economic_values['total_opex']}, MCSP: {economic_values['mcsp']}"
            )
            logger.info(
                f"Using calculated technical values - Recovery: {technical_values['protein_recovery']}, "
                f"Efficiency: {technical_values['separation_efficiency']}, "
                f"Process: {technical_values['process_efficiency']}"
            )
            logger.info(
                f"Using calculated environmental values - "
                f"GWP: {env_values['gwp']}, HCT: {env_values['hct']}, "
                f"FRS: {env_values['frs']}, Water: {env_values['water_consumption']}"
            )
            
            # Extract CAPEX values from economic results
            capex_summary = economic_results.get('capex_analysis', {}).get('capex_summary', {})
            total_capex = economic_values['total_capex']
            
            # Extract OPEX values
            opex_summary = economic_results.get('opex_analysis', {}).get('opex_summary', {})
            total_opex = economic_values['total_opex']
            
            # Extract MCSP and raw material costs
            mcsp = economic_values['mcsp']
            raw_material_cost = economic_values['raw_material_cost']
            
            # Prepare efficiency data with validated values
            efficiency_data = {
                "economic_data": {
                    "capex": {
                        "total_capex": total_capex,
                        "equipment_cost": capex_summary.get('equipment_costs', total_capex * 0.7),
                        "installation_cost": capex_summary.get('installation_costs', total_capex * 0.2),
                        "indirect_cost": capex_summary.get('indirect_costs', total_capex * 0.1)
                    },
                    "opex": {
                        "total_annual_cost": total_opex,
                        "utilities_cost": opex_summary.get('utility_costs', total_opex * 0.3),
                        "materials_cost": raw_material_cost,
                        "labor_cost": opex_summary.get('labor_costs', total_opex * 0.2),
                        "maintenance_cost": opex_summary.get('maintenance_costs', total_opex * 0.1)
                    },
                    "production_volume": production_volume,
                    "product_prices": {
                        "main_product": mcsp,
                        "waste_product": 0.1
                    },
                    "production_volumes": {
                        "main_product": main_product_volume,
                        "waste_product": waste_volume
                    },
                    "raw_material_cost": raw_material_cost
                },
                "quality_metrics": {
                    "protein_recovery": technical_values['protein_recovery'],
                    "separation_efficiency": technical_values['separation_efficiency'],
                    "process_efficiency": technical_values['process_efficiency'],
                    "particle_size_distribution": {
                        "d10": data.get('d10_particle_size', 0.0),
                        "d50": data.get('d50_particle_size', 0.0),
                        "d90": data.get('d90_particle_size', 0.0)
                    }
                },
                "environmental_impacts": {
                    "gwp": env_values['gwp'],
                    "hct": env_values['hct'],
                    "frs": env_values['frs'],
                    "water_consumption": env_values['water_consumption'],
                    "allocated_impacts": environmental_results.get('impact_assessment', {})
                },
                "resource_inputs": {
                    "energy_consumption": data.get('electricity_consumption', 0.0) + data.get('cooling_consumption', 0.0),
                    "water_usage": data.get('water_consumption', 0.0),
                    "raw_material_input": data.get('input_mass', 0.0)
                },
                "process_type": data.get('process_type', 'baseline')
            }
            
            try:
                # Get eco-efficiency analysis with its own retry mechanism
                efficiency_results = await self._analyze_efficiency(efficiency_data)
            except Exception as e:
                logger.error(f"Error in eco-efficiency analysis: {str(e)}")
                raise RuntimeError(f"Error in eco-efficiency analysis: {str(e)}")
            
            # Compile final results
            final_results = {
                'technical_results': {
                    'protein_recovery': technical_values['protein_recovery'],
                    'separation_efficiency': technical_values['separation_efficiency'],
                    'process_efficiency': technical_values['process_efficiency'],
                    'particle_size_distribution': technical_results.get('particle_size_distribution', {})
                },
                'economic_analysis': economic_results,
                'environmental_results': {
                    'impact_assessment': {
                        'gwp': env_values['gwp'],
                        'hct': env_values['hct'],
                        'frs': env_values['frs'],
                        'water_consumption': env_values['water_consumption']
                    },
                    'consumption_metrics': {
                        'electricity': data.get('electricity_consumption') if data.get('process_type') == 'rf' else None,
                        'cooling': data.get('cooling_consumption') if data.get('process_type') == 'ir' else None,
                        'water': data.get('water_consumption')
                    }
                },
                'efficiency_results': efficiency_results,
                'process_type': data.get('process_type'),
                'electricity_consumption': data.get('electricity_consumption'),
                'cooling_consumption': data.get('cooling_consumption')
            }
            
            logger.info("Process analysis completed successfully")
            return final_results
            
        except Exception as e:
            logger.error(f"Error in process analysis: {str(e)}", exc_info=True)
            # Don't wrap the exception in RuntimeError if it's already a RuntimeError
            if isinstance(e, RuntimeError):
                raise
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
            # Structure the request data according to EcoEfficiencyRequest model
            request_data = {
                "economic_data": {
                    "capex": data.get("economic_data", {}).get("capex", {}),
                    "opex": data.get("economic_data", {}).get("opex", {}),
                    "production_volume": data.get("economic_data", {}).get("production_volume", 0.0),
                    "product_prices": data.get("economic_data", {}).get("product_prices", {}),
                    "production_volumes": data.get("economic_data", {}).get("production_volumes", {}),
                    "raw_material_cost": data.get("economic_data", {}).get("raw_material_cost", 0.0)
                },
                "quality_metrics": {
                    "protein_recovery": data.get("quality_metrics", {}).get("protein_recovery", 0.0),
                    "separation_efficiency": data.get("quality_metrics", {}).get("separation_efficiency", 0.0),
                    "process_efficiency": data.get("quality_metrics", {}).get("process_efficiency", 0.0),
                    "particle_size_distribution": {
                        "d10": data.get("quality_metrics", {}).get("particle_size_distribution", {}).get("d10", 0.0),
                        "d50": data.get("quality_metrics", {}).get("particle_size_distribution", {}).get("d50", 0.0),
                        "d90": data.get("quality_metrics", {}).get("particle_size_distribution", {}).get("d90", 0.0)
                    }
                },
                "environmental_impacts": {
                    "gwp": data.get("environmental_impacts", {}).get("gwp", 0.0),
                    "hct": data.get("environmental_impacts", {}).get("hct", 0.0),
                    "frs": data.get("environmental_impacts", {}).get("frs", 0.0),
                    "water_consumption": data.get("environmental_impacts", {}).get("water_consumption", 0.0),
                    "allocated_impacts": data.get("environmental_impacts", {}).get("allocated_impacts", {})
                },
                "resource_inputs": {
                    "energy_consumption": data.get("resource_inputs", {}).get("energy_consumption", 0.0),
                    "water_usage": data.get("resource_inputs", {}).get("water_usage", 0.0),
                    "raw_material_input": data.get("resource_inputs", {}).get("raw_material_input", 0.0)
                },
                "process_type": data.get("process_type", "baseline")
            }

            response = await self.client.post(
                f"{self.base_url}/environmental/eco-efficiency/calculate",
                json=request_data,
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
    
    def _validate_and_extract_metrics(self, results: Dict[str, Any], metric_type: str) -> Tuple[List[str], Dict[str, float]]:
        """
        Extract and validate metrics with proper error handling and logging
        
        Args:
            results: Raw results dictionary
            metric_type: Metric type ('economic', 'technical', or 'environmental')
            
        Returns:
            Tuple of (defaults_used, extracted_values)
        """
        defaults_used = []
        extracted_values = {}
        
        def extract_nested_value(data: Dict[str, Any], path: List[str], default: float = 0.0) -> Tuple[float, bool]:
            """Extract value from nested dict and determine if it's a calculated value"""
            current = data
            for key in path[:-1]:  # Navigate to parent
                if not isinstance(current, dict):
                    return default, False
                current = current.get(key, {})
            
            if not isinstance(current, dict):
                return default, False
                
            value = current.get(path[-1])
            if value is None:
                return default, False
            try:
                return float(value), True
            except (TypeError, ValueError):
                return default, False

        # Define metric paths and their default values
        metric_paths = {
            'economic': {
                'total_capex': (['capex_analysis', 'summary', 'total_capex'], 1000.0),
                'total_opex': (['opex_analysis', 'summary', 'total_opex'], 500.0),
                'mcsp': (['profitability_analysis', 'metrics', 'mcsp', 'mcsp'], 1.0),
                'raw_material_cost': (['opex_analysis', 'summary', 'raw_material_costs'], 0.5)
            },
             'technical': {
                'protein_recovery': (['technical_results', 'protein_recovery'], 0.0),
                'separation_efficiency': (['technical_results', 'separation_efficiency', 'separation_efficiency'], 0.0),
                'process_efficiency': (['technical_results', 'process_efficiency'], 0.0)
            },
            'environmental': {
                'gwp': (['gwp'], 0.0),
                'hct': (['hct'], 0.0),
                'frs': (['frs'], 0.0),
                'water_consumption': (['water_consumption'], 0.0)
            }
        }

        paths = metric_paths.get(metric_type, {})
        for metric_name, (path, default) in paths.items():
            value = None
            is_calculated = False
            
            # Try direct path first
            value, is_calculated = extract_nested_value(results, path, default)
            
            # If not found, try alternative paths based on metric type
            if not is_calculated:
                if metric_type == 'technical':
                    if metric_name == 'protein_recovery':
                        # Get from technical_results structure
                        value, is_calculated = extract_nested_value(results, ['technical_results', 'protein_recovery'], default)
                            
                    elif metric_name == 'separation_efficiency':
                        # Get from technical_results structure
                        value, is_calculated = extract_nested_value(results, ['technical_results', 'separation_efficiency', 'separation_efficiency'], default)
                    
                    elif metric_name == 'process_efficiency':
                        # Get from technical_results structure
                        value, is_calculated = extract_nested_value(results, ['technical_results', 'process_efficiency'], default)
                
                elif metric_type == 'environmental':
                    # Try direct access first (from impact calculation endpoint)
                    if not is_calculated:
                        value, is_calculated = extract_nested_value(results, [metric_name], default)
                    
                    # Try under environmental_results (from compiled results)
                    if not is_calculated:
                        value, is_calculated = extract_nested_value(results, ['environmental_results', metric_name], default)
                    
                    # Try under impact_assessment (from stored results)
                    if not is_calculated:
                        value, is_calculated = extract_nested_value(results, ['impact_assessment', metric_name], default)
                    
                    # Finally try under environmental_results.impact_assessment
                    if not is_calculated:
                        value, is_calculated = extract_nested_value(results, ['environmental_results', 'impact_assessment', metric_name], default)
            
            # Only mark as default if we don't have a calculated value
            if not is_calculated:
                defaults_used.append(metric_name)
                value = default
            
            # Ensure non-negative values
            value = max(0.0, value)
            if metric_name in ['total_capex', 'total_opex', 'mcsp', 'raw_material_cost']:
                value = max(0.1, value)  # Ensure minimum positive values for economic metrics
                
            extracted_values[metric_name] = value
            logger.debug(f"Extracted {metric_type} metric {metric_name}: {value} (calculated: {is_calculated})")

        return defaults_used, extracted_values 