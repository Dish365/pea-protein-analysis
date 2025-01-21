import pytest
from django.test import AsyncClient
from rest_framework.test import APIClient
from process_data.models.process import ProcessAnalysis, AnalysisResult
from django.core.cache import cache
from unittest.mock import AsyncMock, patch
import asyncio

@pytest.fixture(autouse=True)
async def clear_cache():
    """Clear cache before each test"""
    cache.clear()
    yield
    cache.clear()

@pytest.fixture
def api_client():
    """Sync API client for testing"""
    return APIClient()

@pytest.fixture
async def async_client():
    """Async client for testing"""
    return AsyncClient()

@pytest.fixture
def mock_fastapi_service():
    """Mock FastAPI service for testing"""
    with patch('process_data.services.fastapi_service.FastAPIService', autospec=True) as mock_service:
        service_instance = mock_service.return_value
        service_instance.__aenter__ = AsyncMock(return_value=service_instance)
        service_instance.__aexit__ = AsyncMock(return_value=None)
        service_instance.analyze_process = AsyncMock()
        yield service_instance

@pytest.fixture
def valid_process_data():
    """Valid process analysis input data"""
    return {
        "process_type": "baseline",
        "air_flow": 100.0,
        "classifier_speed": 1000.0,
        "input_mass": 100.0,
        "output_mass": 80.0,
        "initial_protein_content": 25.0,
        "final_protein_content": 45.0,
        "initial_moisture_content": 15.0,
        "final_moisture_content": 10.0,
        "d10_particle_size": 10.0,
        "d50_particle_size": 50.0,
        "d90_particle_size": 90.0,
        "equipment": {"name": "test_equipment", "type": "classifier"},
        "equipment_cost": 50000.0,
        "maintenance_cost": 5000.0,
        "installation_factor": 0.2,
        "indirect_costs_factor": 0.15,
        "maintenance_factor": 0.05,
        "indirect_factors": {"engineering": 0.1, "contingency": 0.05},
        "raw_material_cost": 2.5,
        "utility_cost": 1.5,
        "labor_cost": 25.0,
        "utilities": {"electricity": 150.0, "water": 200.0},
        "raw_materials": {"feed": {"quantity": 100.0, "cost": 2.5}},
        "labor_config": {"workers": 2, "hours": 8, "rate": 25.0},
        "project_duration": 10,
        "discount_rate": 0.1,
        "production_volume": 1000.0,
        "revenue_per_year": 500000.0,
        "cash_flows": [],
        "sensitivity_range": 0.2,
        "steps": 10,
        "electricity_consumption": 150.0,
        "cooling_consumption": 50.0,
        "water_consumption": 200.0,
        "transport_consumption": 100.0,
        "equipment_mass": 1000.0,
        "thermal_ratio": 0.3,
        "energy_consumption": {"electricity": 150.0, "cooling": 50.0},
        "production_data": {"input": 100.0, "output": 80.0},
        "product_values": {"protein": 10.0, "starch": 5.0},
        "allocation_method": "hybrid",
        "hybrid_weights": {"economic": 0.5, "physical": 0.5}
    }

@pytest.fixture
def mock_analysis_results():
    """Mock analysis results from FastAPI service"""
    return {
        "technical_results": {
            "protein_recovery": 0.8,
            "separation_efficiency": 0.85,
            "process_efficiency": 0.75,
            "particle_size_distribution": {
                "d10": 10.0,
                "d50": 50.0,
                "d90": 90.0
            }
        },
        "economic_results": {
            "capex_analysis": {
                "summary": {
                    "equipment_costs": 50000.0,
                    "installation_costs": 10000.0,
                    "indirect_costs": 7500.0,
                    "total_capex": 67500.0
                },
                "equipment_breakdown": []
            },
            "opex_analysis": {
                "summary": {
                    "utilities_cost": 5000.0,
                    "materials_cost": 5000.0,
                    "labor_cost": 3000.0,
                    "maintenance_cost": 2000.0,
                    "total_opex": 15000.0
                }
            },
            "profitability_analysis": {
                "metrics": {
                    "npv": 250000.0,
                    "roi": 0.25,
                    "payback_period": 4.5,
                    "profitability_index": 1.25
                }
            }
        },
        "environmental_results": {
            "gwp": 125.0,
            "hct": 0.5,
            "frs": 2.5,
            "water_consumption": 200.0
        },
        "efficiency_results": {
            "efficiency_metrics": {
                "economic_indicators": {"npv_efficiency": 0.85},
                "quality_indicators": {"protein_efficiency": 0.8},
                "resource_efficiency": {"resource_efficiency": 0.75}
            },
            "performance_indicators": {
                "eco_efficiency_index": 0.85,
                "relative_performance": 1.2
            }
        }
    }

@pytest.fixture
async def create_test_process():
    """Create a test process for testing"""
    async def _create_process(data):
        process = await ProcessAnalysis.objects.acreate(**data)
        return process
    return _create_process

@pytest.fixture
async def create_test_result():
    """Create a test result for testing"""
    async def _create_result(process, data):
        result = await AnalysisResult.objects.acreate(process=process, **data)
        return result
    return _create_result
