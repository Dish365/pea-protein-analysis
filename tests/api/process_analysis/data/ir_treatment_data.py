"""Test data for IR treatment process"""

from analytics.pipeline.orchestrator.workflow_types import WorkflowType

IR_TREATMENT_TEST_DATA = {
    "workflow_type": WorkflowType.IR_TREATMENT.value,
    "process_id": "test_ir_001", 
    "analysis_type": "technical",
    "input_data": {
        "technical": {
            "material_properties": {
                "moisture_content": 12.0,
                "surface_temperature": 80.0  # °C
            },
            "ir_parameters": {
                "power_density": 5.0,  # kW/m²
                "wavelength": 3.4,  # μm
                "treatment_time": 3.0  # minutes
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
                    "ir_heater": 65000.0,
                    "conveyor_system": 45000.0,
                    "auxiliary_equipment": 25000.0
                },
                "installation_factor": 0.2,
                "indirect_costs_factor": 0.15
            }
        }
    }
} 