from typing import Dict, Any, Type, Optional
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
import sys
from pathlib import Path
import logging

from ..orchestrator.workflow_types import WorkflowType  # Update import path

logger = logging.getLogger(__name__)

# Add backend/django_app to Python path
django_app_path = Path(__file__).resolve().parent.parent.parent.parent / "backend" / "django_app"
sys.path.append(str(django_app_path))

# Import and run Django setup
from backend.django_app.core.setup import setup_django_for_fastapi
setup_django_for_fastapi()

# Now import Django models
from backend.django_app.process_data.models.baseline import BaselineProcess
from backend.django_app.process_data.models.rf_treatment import RFTreatmentProcess
from backend.django_app.process_data.models.ir_treatment import IRTreatmentProcess

class ModelIntegrator:
    """Handles integration between Django models and analysis pipeline"""
    
    def __init__(self):
        # Map workflow types using enum values
        self.workflow_models = {
            WorkflowType.BASELINE.value: BaselineProcess,
            WorkflowType.RF_TREATMENT.value: RFTreatmentProcess,
            WorkflowType.IR_TREATMENT.value: IRTreatmentProcess
        }
        logger.debug(f"Initialized ModelIntegrator with workflows: {list(self.workflow_models.keys())}")

    def get_model_for_process_type(self, workflow_type: str) -> Type[models.Model]:
        """Get the appropriate model class for a process type"""
        logger.debug(f"Getting model for workflow type: '{workflow_type}'")
        logger.debug(f"Available workflow types: {list(self.workflow_models.keys())}")
        
        # Normalize workflow type to string value
        if isinstance(workflow_type, WorkflowType):
            workflow_type = workflow_type.value
            
        if workflow_type not in self.workflow_models:
            error_msg = f"Unknown workflow type: {workflow_type}"
            logger.error(f"{error_msg}. Available types: {list(self.workflow_models.keys())}")
            raise ValueError(error_msg)
            
        model_class = self.workflow_models[workflow_type]
        logger.debug(f"Found model class: {model_class.__name__}")
        return model_class

    @staticmethod
    def transform_baseline_to_analysis_input(model_instance: BaselineProcess) -> Dict[str, Any]:
        """Transform baseline process model to analysis input format"""
        return {
            'technical': {
                'protein_data': {
                    'feed_rate': model_instance.feed_rate,
                    'air_flow_rate': model_instance.air_flow_rate,
                    'classifier_speed': model_instance.classifier_speed
                },
                'process_conditions': {
                    'temperature': model_instance.temperature,
                    'humidity': model_instance.humidity,
                    'pressure': model_instance.pressure
                }
            },
            'metadata': {
                'process_id': model_instance.process_id,
                'timestamp': model_instance.timestamp.isoformat(),
                'process_type': WorkflowType.BASELINE.value
            }
        }

    @staticmethod
    def transform_rf_treatment_to_analysis_input(model_instance: RFTreatmentProcess) -> Dict[str, Any]:
        """Transform RF treatment model to analysis input format"""
        return {
            'technical': {
                'material_properties': {
                    'moisture_content': model_instance.moisture_content,
                    'dielectric_properties': {
                        'constant': model_instance.dielectric_constant,
                        'loss_factor': model_instance.loss_factor
                    }
                },
                'rf_parameters': {
                    'power': model_instance.power,
                    'frequency': model_instance.frequency,
                    'treatment_time': model_instance.treatment_time
                }
            },
            'metadata': {
                'process_id': model_instance.process_id,
                'timestamp': model_instance.timestamp.isoformat(),
                'process_type': WorkflowType.RF_TREATMENT.value
            }
        }

    @staticmethod
    def transform_ir_treatment_to_analysis_input(model_instance: IRTreatmentProcess) -> Dict[str, Any]:
        """Transform IR treatment model to analysis input format"""
        return {
            'technical': {
                'material_properties': {
                    'moisture_content': model_instance.moisture_content,
                    'surface_temperature': model_instance.surface_temperature
                },
                'ir_parameters': {
                    'power_density': model_instance.power_density,
                    'wavelength': model_instance.wavelength,
                    'treatment_time': model_instance.treatment_time
                }
            },
            'metadata': {
                'process_id': model_instance.process_id,
                'timestamp': model_instance.timestamp.isoformat(),
                'process_type': WorkflowType.IR_TREATMENT.value
            }
        }

    @staticmethod
    def transform_analysis_results_to_model(
        results: Dict[str, Any], 
        model_class: Type[models.Model],
        process_id: str
    ) -> Dict[str, Any]:
        """Transform analysis results to model fields"""
        # Define field mappings for different model types
        field_mappings = {
            BaselineProcess.__name__: {
                'technical_results': {
                    'protein_recovery': 'protein_yield',
                    'separation_efficiency': 'separation_efficiency',
                    'feed_rate_actual': 'feed_rate',
                    'air_flow_actual': 'air_flow_rate',
                    'classifier_efficiency': 'classifier_speed'
                }
            },
            RFTreatmentProcess.__name__: {
                'technical_results': {
                    'final_moisture': 'moisture_content',
                    'power_efficiency': 'power',
                    'treatment_effectiveness': 'treatment_time',
                    'dielectric_response': 'dielectric_constant'
                }
            },
            IRTreatmentProcess.__name__: {
                'technical_results': {
                    'final_moisture': 'moisture_content',
                    'surface_temp_actual': 'surface_temperature',
                    'treatment_effectiveness': 'treatment_time',
                    'power_density_actual': 'power_density'
                }
            }
        }

        # Get the appropriate field mapping
        model_name = model_class.__name__
        if model_name not in field_mappings:
            raise ValueError(f"No field mapping defined for model: {model_name}")

        mapping = field_mappings[model_name]
        
        # Transform results to model fields
        model_data = {
            'process_id': process_id,
            'timestamp': datetime.now()
        }
        
        for result_category, fields in mapping.items():
            if result_category in results:
                for result_key, model_field in fields.items():
                    if result_key in results[result_category]:
                        model_data[model_field] = results[result_category][result_key]

        return model_data

    @staticmethod
    def validate_model_data(model_class: Type[models.Model], data: Dict[str, Any]) -> None:
        """Validate data against model field constraints"""
        try:
            # Create temporary instance for validation
            instance = model_class(**data)
            instance.full_clean()
        except ValidationError as e:
            raise ValidationError(f"Model validation failed: {str(e)}") 