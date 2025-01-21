"""Test data for RF treatment process"""

from analytics.pipeline.orchestrator.workflow_types import WorkflowType

RF_TREATMENT_TEST_DATA = {
    "workflow_type": WorkflowType.RF_TREATMENT.value,
    "process_id": "test_rf_001",
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
                "power": 3.0,  # kW
                "frequency": 27.12,  # MHz
                "treatment_time": 5.0  # minutes
            },
            "operating_conditions": {
                "temperature": 25.0,  # °C
                "humidity": 45.0,  # %
                "pressure": 1.01  # bar
            }
        },
        "economic": {
            "capital_costs": {
                "equipment": {
                    "rf_generator": 85000.0,
                    "treatment_chamber": 35000.0,
                    "auxiliary_equipment": 25000.0
                },
                "installation_factor": 0.2,
                "indirect_costs_factor": 0.15
            }
        }
    }
} 