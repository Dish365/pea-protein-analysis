import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.core.cache import cache
from django.conf import settings
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
import json
import logging
from process_data.services.fastapi_service import FastAPIService

logger = logging.getLogger(__name__)

# Cache Configuration
@pytest.fixture(autouse=True)
def use_test_cache():
    """Configure cache for testing"""
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test"""
    cache.clear()
    yield
    cache.clear()

# Client Fixtures
@pytest.fixture
def client():
    """Test client for API requests"""
    return APIClient()

@pytest.fixture
def async_client():
    """Async test client for API requests"""
    return APIClient()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def django_client():
    return Client()

# Mock Response Fixtures
@pytest.fixture
def mock_fastapi_response():
    return {
        "technical_results": {
            "protein_recovery": {
                "mass": 36.0,
                "content": 45.0,
                "yield": 0.8
            },
            "separation_efficiency": 0.85,
            "process_efficiency": 0.75,
            "particle_size_distribution": {
                "d10": 10.0,
                "d50": 50.0,
                "d90": 90.0
            }
        },
        "economic_analysis": {
            "capex_analysis": {
                "total_capex": 75000.0,
                "equipment_cost": 50000.0,
                "installation_cost": 15000.0,
                "indirect_cost": 10000.0
            },
            "opex_analysis": {
                "total_opex": 15000.0,
                "utilities_cost": 5000.0,
                "materials_cost": 5000.0,
                "labor_cost": 3000.0,
                "maintenance_cost": 2000.0
            },
            "profitability_analysis": {
                "npv": 250000.0,
                "roi": 0.25,
                "irr": 15.5,
                "payback_period": 3.5
            }
        },
        "environmental_results": {
            "impact_assessment": {
                "gwp": 125.0,
                "hct": 0.5,
                "frs": 2.5
            },
            "consumption_metrics": {
                "electricity": None,
                "cooling": None,
                "water": None
            },
            "allocated_impacts": {
                "product": {"gwp": 800, "water": 400},
                "byproduct": {"gwp": 200, "water": 100}
            }
        },
        "efficiency_results": {
            "efficiency_metrics": {
                "eco_efficiency_index": 0.85,
                "technical_score": 0.85,
                "economic_score": 0.75,
                "environmental_score": 0.90
            },
            "performance_indicators": {
                "relative_performance": 1.2,
                "overall_efficiency": 0.83
            }
        }
    }

@pytest.fixture
def mock_process_input():
    return {
        "process_type": "baseline",
        "technical_params": {
            "initial_moisture": 35.0,
            "target_moisture": 12.0,
            "particle_size": {
                "d10": 100,
                "d50": 250,
                "d90": 500
            }
        },
        "economic_params": {
            "project_duration": 10,
            "discount_rate": 0.1,
            "capacity": 1000
        },
        "environmental_params": {
            "electricity_consumption": 100,
            "water_consumption": 50,
            "allocation_method": "mass"
        }
    }

@pytest.fixture
def mock_rust_response():
    return {
        "protein_calculations": {
            "recovery": 85.0,
            "concentration": 55.0
        },
        "monte_carlo_results": {
            "iterations": 1000,
            "npv_distribution": [1800000, 2000000, 2200000],
            "irr_distribution": [14.5, 15.5, 16.5]
        },
        "impact_allocations": {
            "mass_based": {"product": 0.8, "byproduct": 0.2},
            "economic_based": {"product": 0.85, "byproduct": 0.15}
        }
    }

# Service Mocks
@pytest.fixture
def mock_fastapi_service():
    """Mock FastAPI service"""
    with patch('process_data.services.fastapi_service.FastAPIService', autospec=True) as mock_service:
        service_instance = mock_service.return_value
        service_instance.__aenter__ = AsyncMock(return_value=service_instance)
        service_instance.__aexit__ = AsyncMock(return_value=None)
        service_instance.analyze_process = AsyncMock()
        service_instance.analyze_process.return_value = mock_fastapi_response()
        service_instance.get_status = AsyncMock(return_value={"status": "completed", "progress": 100})
        service_instance.client = AsyncMock()
        service_instance.client.post = AsyncMock()
        service_instance.client.post.return_value.status_code = 200
        service_instance.client.post.return_value.json = AsyncMock(
            return_value=service_instance.analyze_process.return_value
        )
        service_instance.client.aclose = AsyncMock()
        yield service_instance

@pytest.fixture
async def real_fastapi_service():
    """Create a real FastAPI service instance"""
    async with FastAPIService() as service:
        yield service

# Event Loop
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()