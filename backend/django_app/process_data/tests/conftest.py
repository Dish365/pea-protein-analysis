import pytest
from django.test import Client
from rest_framework.test import APIClient
from django.core.cache import cache
from django.conf import settings

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