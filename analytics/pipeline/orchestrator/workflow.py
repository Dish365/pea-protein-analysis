from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime

from ..integrator.technical import TechnicalIntegrator
from ..integrator.economic import EconomicIntegrator
from ..integrator.environmental import EnvironmentalIntegrator
from ..integrator.model_integration import ModelIntegrator
from .error_handling import (
    handle_error, 
    retry_operation,
    TechnicalAnalysisError,
    EconomicAnalysisError,
    EnvironmentalAnalysisError,
    log_execution_time,
    track_workflow_errors
)

logger = logging.getLogger(__name__)

class AnalysisWorkflow:
    """Orchestrates the complete analysis workflow"""
    
    def __init__(self):
        self.technical = TechnicalIntegrator()
        self.economic = EconomicIntegrator()
        self.environmental = EnvironmentalIntegrator()
        self.model_integrator = ModelIntegrator()

    @log_execution_time()
    async def execute_workflow(
        self, 
        input_data: Dict[str, Any], 
        workflow_type: str,
        process_id: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Execute analysis workflow with validation and error handling"""
        try:
            # Validate input data
            if not self.validate_input_data(input_data, workflow_type):
                raise ValueError(f"Invalid input data for workflow type: {workflow_type}")

            logger.info(f"Starting {workflow_type} workflow execution for process {process_id}")

            # Get appropriate model class
            model_class = self.model_integrator.get_model_for_process_type(workflow_type)

            # Transform input data if from model
            if 'model_instance' in input_data:
                input_data = self._transform_model_input(input_data['model_instance'], workflow_type)

            # Execute appropriate workflow
            results = await self._execute_workflow_by_type(
                workflow_type, 
                input_data,
                max_retries
            )

            # Transform results for model storage
            model_data = self.model_integrator.transform_analysis_results_to_model(
                results,
                model_class,
                process_id
            )

            # Validate transformed data
            self.model_integrator.validate_model_data(model_class, model_data)

            return {
                'analysis_results': results,
                'model_data': model_data
            }

        except Exception as e:
            await track_workflow_errors(workflow_type, e)
            raise

    def _transform_model_input(
        self, 
        model_instance: Any, 
        workflow_type: str
    ) -> Dict[str, Any]:
        """Transform model instance to analysis input format"""
        transform_methods = {
            'baseline': self.model_integrator.transform_baseline_to_analysis_input,
            'rf_treatment': self.model_integrator.transform_rf_treatment_to_analysis_input,
            'ir_treatment': self.model_integrator.transform_ir_treatment_to_analysis_input
        }
        
        if workflow_type not in transform_methods:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
            
        return transform_methods[workflow_type](model_instance)

    async def _execute_workflow_by_type(
        self,
        workflow_type: str,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute specific workflow type with retry logic"""
        workflow_methods = {
            'technical': self._run_technical_workflow,
            'economic': self._run_economic_workflow,
            'environmental': self._run_environmental_workflow
        }

        if workflow_type not in workflow_methods:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

        return await workflow_methods[workflow_type](input_data, max_retries)

    @retry_operation(max_retries=3)
    async def _run_technical_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute technical analysis workflow"""
        try:
            return await self.technical.analyze_technical(input_data)
        except Exception as e:
            raise TechnicalAnalysisError(f"Technical analysis failed: {str(e)}")

    @retry_operation(max_retries=3)
    async def _run_economic_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute economic analysis workflow"""
        try:
            return await self.economic.analyze_economic(input_data)
        except Exception as e:
            raise EconomicAnalysisError(f"Economic analysis failed: {str(e)}")

    @retry_operation(max_retries=3)
    async def _run_environmental_workflow(
        self,
        input_data: Dict[str, Any],
        max_retries: int
    ) -> Dict[str, Any]:
        """Execute environmental analysis workflow"""
        try:
            return await self.environmental.analyze_environmental(input_data)
        except Exception as e:
            raise EnvironmentalAnalysisError(f"Environmental analysis failed: {str(e)}")
