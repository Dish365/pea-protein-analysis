from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
from enum import Enum

from ..integrator.technical import TechnicalIntegrator
from ..integrator.economic import EconomicIntegrator
from ..integrator.environmental import EnvironmentalIntegrator
from ..integrator.model_integration import ModelIntegrator
from .error_handling import (
    retry_operation,
    log_execution_time,
    track_workflow_errors
)
from .workflow_types import WorkflowType

logger = logging.getLogger(__name__)

class AnalysisWorkflow:
    """
    Orchestrates the complete analysis workflow.
    
    This class coordinates between:
    1. Different types of analysis (technical, economic, environmental)
    2. Model integration and data transformation
    3. Error handling and retries
    4. Workflow execution and monitoring
    """
    
    def __init__(self):
        self.technical = TechnicalIntegrator()
        self.economic = EconomicIntegrator()
        self.environmental = EnvironmentalIntegrator()
        self.model_integrator = ModelIntegrator()
        
        # Initialize workflow type mapping
        self.workflow_mapping = {
            WorkflowType.BASELINE: self._run_baseline_workflow,
            WorkflowType.RF_TREATMENT: self._run_rf_workflow,
            WorkflowType.IR_TREATMENT: self._run_ir_workflow
        }
        logger.debug(f"Initialized AnalysisWorkflow with valid types: {WorkflowType.values()}")

    @log_execution_time()
    async def execute_workflow(
        self, 
        input_data: Dict[str, Any], 
        workflow_type: WorkflowType,
        process_id: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Execute analysis workflow with validation and error handling"""
        try:
            logger.info(f"Starting {workflow_type.value} workflow execution for process {process_id}")
            
            # Input validation and normalization
            workflow_type = self._validate_workflow_type(workflow_type)
            input_data = await self._validate_and_transform_input(input_data, workflow_type, process_id)
            
            # Execute workflow with retries
            results = await self._execute_workflow_with_retries(
                workflow_type,
                input_data,
                max_retries
            )
            
            # Transform and validate results
            final_results = await self._transform_and_validate_results(
                results,
                workflow_type,
                process_id
            )
            
            logger.info(f"Successfully completed {workflow_type.value} workflow for process {process_id}")
            return final_results
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            await track_workflow_errors(workflow_type.value, e)
            raise

    async def _validate_and_transform_input(
        self,
        input_data: Dict[str, Any],
        workflow_type: WorkflowType,
        process_id: str
    ) -> Dict[str, Any]:
        """Validate and transform input data"""
        try:
            # Get model class for workflow type
            model_class = self.model_integrator.get_model_for_process_type(workflow_type.value)
            
            # Transform model instance if present
            if 'model_instance' in input_data:
                input_data = self._transform_model_input(
                    input_data['model_instance'],
                    workflow_type.value
                )
            
            # Validate transformed input
            if not self.validate_input_data(input_data, workflow_type.value):
                raise ValueError(f"Invalid input data for workflow type: {workflow_type.value}")
                
            return input_data
            
        except Exception as e:
            logger.error(f"Input validation/transformation failed: {str(e)}")
            raise

    @retry_operation(max_retries=3)
    async def _execute_workflow_with_retries(
        self,
        workflow_type: WorkflowType,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute workflow with retry mechanism"""
        try:
            # Get appropriate workflow handler
            workflow_handler = self.workflow_mapping.get(workflow_type)
            if not workflow_handler:
                raise ValueError(f"No handler found for workflow type: {workflow_type.value}")
                
            # Execute workflow
            results = await workflow_handler(input_data, max_retries)
            
            # Add metadata
            results.update({
                'workflow_type': workflow_type.value,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return results
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            raise

    async def _run_baseline_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute baseline analysis workflow"""
        try:
            # Execute analyses in parallel
            technical_task = self.technical.analyze_technical(input_data.get("technical", {}))
            economic_task = self.economic.analyze_economics(input_data.get("economic", {}))
            environmental_task = self.environmental.analyze_environmental_impacts(
                input_data.get("environmental", {})
            )
            
            # Wait for all analyses to complete
            technical_results, economic_results, environmental_results = await asyncio.gather(
                technical_task,
                economic_task,
                environmental_task
            )
            
            return {
                "technical_results": technical_results,
                "economic_results": economic_results,
                "environmental_results": environmental_results,
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Baseline workflow failed: {str(e)}")
            raise

    async def _run_rf_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute RF treatment workflow with specific RF processing"""
        try:
            logger.info("Starting RF treatment workflow")
            
            # Prepare RF-specific technical parameters
            rf_technical_data = {
                **input_data.get("technical", {}),
                "treatment_type": "rf",
                "rf_parameters": input_data.get("technical", {}).get("rf_parameters", {})
            }
            
            # Execute analyses in parallel with RF-specific parameters
            technical_task = self.technical.analyze_technical(rf_technical_data)
            economic_task = self.economic.analyze_economics({
                **input_data.get("economic", {}),
                "equipment_type": "rf_system",
                "energy_consumption": rf_technical_data.get("rf_parameters", {}).get("power", 0)
            })
            environmental_task = self.environmental.analyze_environmental({
                **input_data.get("environmental", {}),
                "energy_type": "rf_electrical",
                "power_consumption": rf_technical_data.get("rf_parameters", {}).get("power", 0),
                "treatment_duration": rf_technical_data.get("rf_parameters", {}).get("treatment_time", 0)
            })
            
            # Wait for all analyses to complete
            technical_results, economic_results, environmental_results = await asyncio.gather(
                technical_task,
                economic_task,
                environmental_task
            )
            
            # Add RF-specific metadata
            results = {
                "technical_results": {
                    **technical_results,
                    "rf_effectiveness": self._calculate_rf_effectiveness(
                        technical_results,
                        rf_technical_data
                    )
                },
                "economic_results": economic_results,
                "environmental_results": environmental_results,
                "status": "completed",
                "treatment_type": "rf"
            }
            
            logger.info("RF treatment workflow completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"RF treatment workflow failed: {str(e)}")
            raise

    async def _run_ir_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute IR treatment workflow with specific IR processing"""
        try:
            logger.info("Starting IR treatment workflow")
            
            # Prepare IR-specific technical parameters
            ir_technical_data = {
                **input_data.get("technical", {}),
                "treatment_type": "ir",
                "ir_parameters": input_data.get("technical", {}).get("ir_parameters", {})
            }
            
            # Execute analyses in parallel with IR-specific parameters
            technical_task = self.technical.analyze_technical(ir_technical_data)
            economic_task = self.economic.analyze_economics({
                **input_data.get("economic", {}),
                "equipment_type": "ir_system",
                "energy_consumption": self._calculate_ir_energy_consumption(
                    ir_technical_data.get("ir_parameters", {})
                )
            })
            environmental_task = self.environmental.analyze_environmental({
                **input_data.get("environmental", {}),
                "energy_type": "ir_thermal",
                "power_density": ir_technical_data.get("ir_parameters", {}).get("power_density", 0),
                "treatment_duration": ir_technical_data.get("ir_parameters", {}).get("treatment_time", 0)
            })
            
            # Wait for all analyses to complete
            technical_results, economic_results, environmental_results = await asyncio.gather(
                technical_task,
                economic_task,
                environmental_task
            )
            
            # Add IR-specific metadata
            results = {
                "technical_results": {
                    **technical_results,
                    "ir_effectiveness": self._calculate_ir_effectiveness(
                        technical_results,
                        ir_technical_data
                    )
                },
                "economic_results": economic_results,
                "environmental_results": environmental_results,
                "status": "completed",
                "treatment_type": "ir"
            }
            
            logger.info("IR treatment workflow completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"IR treatment workflow failed: {str(e)}")
            raise

    def _calculate_rf_effectiveness(
        self,
        technical_results: Dict[str, Any],
        rf_data: Dict[str, Any]
    ) -> float:
        """Calculate RF treatment effectiveness based on technical results"""
        try:
            power = rf_data.get("rf_parameters", {}).get("power", 0)
            frequency = rf_data.get("rf_parameters", {}).get("frequency", 0)
            treatment_time = rf_data.get("rf_parameters", {}).get("treatment_time", 0)
            
            if not all([power, frequency, treatment_time]):
                raise ValueError("Missing required RF parameters")
                
            # Calculate effectiveness based on power, frequency, and treatment time
            energy_density = power * treatment_time
            effectiveness = (energy_density * frequency) / 1000  # Normalized score
            
            return min(max(effectiveness, 0), 100)  # Clamp between 0-100
            
        except Exception as e:
            logger.error(f"Error calculating RF effectiveness: {str(e)}")
            return 0

    def _calculate_ir_effectiveness(
        self,
        technical_results: Dict[str, Any],
        ir_data: Dict[str, Any]
    ) -> float:
        """Calculate IR treatment effectiveness based on technical results"""
        try:
            power_density = ir_data.get("ir_parameters", {}).get("power_density", 0)
            wavelength = ir_data.get("ir_parameters", {}).get("wavelength", 0)
            treatment_time = ir_data.get("ir_parameters", {}).get("treatment_time", 0)
            
            if not all([power_density, wavelength, treatment_time]):
                raise ValueError("Missing required IR parameters")
                
            # Calculate effectiveness based on power density, wavelength, and treatment time
            energy_density = power_density * treatment_time
            effectiveness = (energy_density / wavelength) * 100  # Normalized score
            
            return min(max(effectiveness, 0), 100)  # Clamp between 0-100
            
        except Exception as e:
            logger.error(f"Error calculating IR effectiveness: {str(e)}")
            return 0

    def _calculate_ir_energy_consumption(self, ir_parameters: Dict[str, Any]) -> float:
        """Calculate energy consumption for IR treatment"""
        try:
            power_density = ir_parameters.get("power_density", 0)
            treatment_time = ir_parameters.get("treatment_time", 0)
            surface_area = ir_parameters.get("surface_area", 1.0)  # Default 1.0 m²
            
            # Calculate total energy consumption in kWh
            energy_consumption = (power_density * surface_area * treatment_time) / 3600
            
            return max(energy_consumption, 0)
            
        except Exception as e:
            logger.error(f"Error calculating IR energy consumption: {str(e)}")
            return 0

    def _validate_workflow_type(self, workflow_type: Any) -> WorkflowType:
        """Validate and normalize workflow type"""
        if isinstance(workflow_type, str):
            return WorkflowType.from_str(workflow_type)
        elif isinstance(workflow_type, WorkflowType):
            return workflow_type
        else:
            raise ValueError(f"Invalid workflow type: {workflow_type}")

    async def _transform_and_validate_results(
        self,
        results: Dict[str, Any],
        workflow_type: WorkflowType,
        process_id: str
    ) -> Dict[str, Any]:
        """Transform and validate workflow results"""
        try:
            # Get model class
            model_class = self.model_integrator.get_model_for_process_type(workflow_type.value)
            
            # Transform results
            transformed_results = self.model_integrator.transform_analysis_results_to_model(
                results,
                model_class,
                process_id
            )
            
            # Validate transformed results
            self.model_integrator.validate_model_data(model_class, transformed_results)
            
            return transformed_results
            
        except Exception as e:
            logger.error(f"Results transformation/validation failed: {str(e)}")
            raise

    def _transform_model_input(
        self, 
        model_instance: Any, 
        workflow_type: str
    ) -> Dict[str, Any]:
        """Transform model instance to analysis input format"""
        transform_methods = {
            WorkflowType.BASELINE.value: self.model_integrator.transform_baseline_to_analysis_input,
            WorkflowType.RF_TREATMENT.value: self.model_integrator.transform_rf_treatment_to_analysis_input,
            WorkflowType.IR_TREATMENT.value: self.model_integrator.transform_ir_treatment_to_analysis_input
        }
        
        if workflow_type not in transform_methods:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
            
        return transform_methods[workflow_type](model_instance)

    def validate_input_data(self, input_data: Dict[str, Any], workflow_type: str) -> bool:
        """Validate input data for workflow type"""
        try:
            logger.debug(f"=== Validating Input Data ===")
            logger.debug(f"Workflow Type: '{workflow_type}'")
            logger.debug(f"Input Data Keys: {list(input_data.keys())}")
            
            if not input_data:
                logger.error("Input data is empty")
                return False
            
            # Define required fields for each workflow type
            workflow_requirements = {
                WorkflowType.BASELINE.value: {
                    "technical": {
                        "process_parameters": ["feed_rate", "air_flow_rate", "classifier_speed"],
                        "material_properties": ["initial_protein_content", "initial_moisture", "particle_size"],
                        "operating_conditions": ["temperature", "humidity", "pressure"]
                    }
                },
                WorkflowType.RF_TREATMENT.value: {
                    "technical": {
                        "material_properties": ["moisture_content", "dielectric_properties"],
                        "rf_parameters": ["power", "frequency", "treatment_time"],
                        "operating_conditions": ["temperature", "humidity", "pressure"]
                    }
                },
                WorkflowType.IR_TREATMENT.value: {
                    "technical": {
                        "material_properties": ["moisture_content", "surface_temperature"],
                        "ir_parameters": ["power_density", "wavelength", "treatment_time"],
                        "operating_conditions": ["temperature", "humidity", "pressure"]
                    }
                }
            }
            
            # Check if workflow type is supported
            if workflow_type not in workflow_requirements:
                logger.error(f"Unknown workflow type: {workflow_type}")
                logger.error(f"Supported types: {list(workflow_requirements.keys())}")
                return False
            
            # Get requirements for this workflow type
            requirements = workflow_requirements[workflow_type]
            logger.debug(f"Requirements for {workflow_type}: {requirements}")
            
            # Validate against requirements
            for category, fields in requirements.items():
                if category not in input_data:
                    logger.error(f"Missing category: {category}")
                    return False
                    
                for section, required in fields.items():
                    if section not in input_data[category]:
                        logger.error(f"Missing section: {section} in {category}")
                        return False
                        
                    for field in required:
                        if field not in input_data[category][section]:
                            logger.error(f"Missing field: {field} in {category}.{section}")
                            return False
                            
            logger.debug("Input data validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Error validating input data: {str(e)}", exc_info=True)
            return False

class WorkflowOrchestrator:
    def __init__(self):
        self.workflow_handlers = {
            WorkflowType.BASELINE: self._handle_baseline_workflow,
            WorkflowType.RF_TREATMENT: self._handle_rf_workflow,
            WorkflowType.IR_TREATMENT: self._handle_ir_workflow
        }
        self.workflow = AnalysisWorkflow()
    
    async def process_workflow(self, workflow_type: WorkflowType, process_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the workflow based on type"""
        logger.debug(f"Processing workflow type: {workflow_type}")
        logger.debug(f"Available handlers: {[t.value for t in self.workflow_handlers.keys()]}")
        
        if workflow_type not in self.workflow_handlers:
            error_msg = f"Unknown workflow type: {workflow_type.value}"
            logger.error(f"{error_msg}. Available types: {[t.value for t in self.workflow_handlers.keys()]}")
            raise ValueError(error_msg)
            
        handler = self.workflow_handlers[workflow_type]
        logger.debug(f"Using handler: {handler.__name__}")
        return await handler(process_id, input_data)

    async def _handle_baseline_workflow(self, process_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Handling baseline workflow for process {process_id}")
        return await self.workflow.execute_workflow(input_data, WorkflowType.BASELINE, process_id)

    async def _handle_rf_workflow(self, process_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Handling RF treatment workflow for process {process_id}")
        return await self.workflow.execute_workflow(input_data, WorkflowType.RF_TREATMENT, process_id)

    async def _handle_ir_workflow(self, process_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"Handling IR treatment workflow for process {process_id}")
        return await self.workflow.execute_workflow(input_data, WorkflowType.IR_TREATMENT, process_id)