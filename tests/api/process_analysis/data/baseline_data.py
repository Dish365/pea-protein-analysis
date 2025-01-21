"""Test data for baseline process"""

from analytics.pipeline.orchestrator.workflow_types import WorkflowType

BASELINE_TEST_DATA = {
    "workflow_type": WorkflowType.BASELINE.value,
    "process_id": "test_baseline_001",
    "analysis_type": "technical",
    "input_data": {
        "technical": {
            "process_parameters": {
                "feed_rate": 50.0,
                "air_flow_rate": 35.0,
                "classifier_speed": 3000,
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
        }
    }
} 