import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.core.cache import cache
from django.conf import settings
from unittest.mock import AsyncMock, patch
import asyncio
import json

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

@pytest.fixture
def mock_fastapi_response():
    return {
        "technical": {
            "protein_recovery": 85.0,
            "moisture_content": 12.0,
            "particle_size": {"d50": 250}
        },
        "economic": {
            "capex": {"total_investment": 1000000},
            "opex": {"total_annual_cost": 500000},
            "profitability": {
                "npv": 2000000,
                "irr": 15.5,
                "payback_period": 3.5
            }
        },
        "environmental": {
            "direct_impacts": {
                "gwp": 1000,
                "water": 500
            },
            "allocated_impacts": {
                "product": {"gwp": 800, "water": 400},
                "byproduct": {"gwp": 200, "water": 100}
            }
        },
        "efficiency": {
            "technical_score": 0.85,
            "economic_score": 0.75,
            "environmental_score": 0.90,
            "overall_efficiency": 0.83
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
def mock_fastapi_service():
    with patch('process_data.services.fastapi_service.FastAPIService') as mock:
        service = mock.return_value
        service.analyze_process = AsyncMock(return_value=mock_fastapi_response())
        service.get_status = AsyncMock(return_value={"status": "completed", "progress": 100})
        yield service

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

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