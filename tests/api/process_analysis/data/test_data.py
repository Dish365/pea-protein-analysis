from typing import Dict, Any
from datetime import datetime
from analytics.pipeline.orchestrator.workflow_types import WorkflowType

class TestDataGenerator:
    """Generate test data for different process types"""
    
    @staticmethod
    def get_baseline_data(process_id: str = "test_baseline_001") -> Dict[str, Any]:
        """Get baseline process test data"""
        return {
            "workflow_type": WorkflowType.BASELINE.value,
            "process_id": process_id,
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "process_parameters": {
                        "feed_rate": 50.0,
                        "air_flow_rate": 35.0,
                        "classifier_speed": 3000
                    },
                    "material_properties": {
                        "initial_protein_content": 23.5,
                        "initial_moisture": 12.0,
                        "particle_size": {
                            "d10": 15.0,
                            "d50": 45.0,
                            "d90": 120.0
                        }
                    },
                    "operating_conditions": {
                        "temperature": 25.0,
                        "humidity": 45.0,
                        "pressure": 1.01,
                        "processing_time": 8.0
                    }
                },
                "economic": {
                    "equipment_list": [
                        {
                            "name": "classifier",
                            "cost": 50000.0,
                            "efficiency": 0.85,
                            "maintenance_cost": 2500.0,
                            "energy_consumption": 15.0,
                            "processing_capacity": 1000.0
                        }
                    ],
                    "indirect_factors": [
                        {
                            "name": "engineering",
                            "cost": 50000.0,
                            "percentage": 0.15
                        }
                    ],
                    "installation_factor": 0.2,
                    "indirect_costs_factor": 0.15,
                    "utilities": [
                        {
                            "name": "electricity",
                            "consumption": 100.0,
                            "unit_price": 0.12,
                            "unit": "kWh"
                        }
                    ],
                    "raw_materials": [
                        {
                            "name": "peas",
                            "quantity": 1000.0,
                            "unit_price": 0.8,
                            "unit": "kg"
                        }
                    ],
                    "labor_config": {
                        "hourly_wage": 25.0,
                        "hours_per_week": 40.0,
                        "weeks_per_year": 52.0,
                        "num_workers": 2
                    },
                    "maintenance_factor": 0.05,
                    "revenue": [100000.0, 120000.0, 150000.0],
                    "project_duration": 10,
                    "discount_rate": 0.1
                }
            }
        }

    @staticmethod
    def get_rf_treatment_data(process_id: str = "test_rf_001") -> Dict[str, Any]:
        """Get RF treatment test data"""
        return {
            "workflow_type": WorkflowType.RF_TREATMENT.value,
            "process_id": process_id,
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "material_properties": {
                        "moisture_content": 12.0,
                        "dielectric_properties": {
                            "constant": 4.5,
                            "loss_factor": 0.8
                        }
                    },
                    "rf_parameters": {
                        "power": 3.0,
                        "frequency": 27.12,
                        "treatment_time": 5.0
                    }
                }
            }
        }

    @staticmethod
    def get_ir_treatment_data(process_id: str = "test_ir_001") -> Dict[str, Any]:
        """Get IR treatment test data"""
        return {
            "workflow_type": WorkflowType.IR_TREATMENT.value,
            "process_id": process_id,
            "analysis_type": "technical",
            "input_data": {
                "technical": {
                    "material_properties": {
                        "moisture_content": 12.0,
                        "surface_temperature": 80.0
                    },
                    "ir_parameters": {
                        "power_density": 5.0,
                        "wavelength": 3.4,
                        "treatment_time": 3.0
                    }
                }
            }
        } 