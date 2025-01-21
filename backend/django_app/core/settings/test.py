from .base import *

# Test settings
DEBUG = False
TEMPLATE_DEBUG = False

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use console email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use local memory cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Disable password hashing to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable CSRF protection in tests
MIDDLEWARE = [m for m in MIDDLEWARE if 'csrf' not in m.lower()]

# Test-specific logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# FastAPI test settings
FASTAPI_BASE_URL = 'http://testserver:8001/api/v1'
FASTAPI_TIMEOUT = 1  # Short timeout for tests
FASTAPI_RETRY_COUNT = 1  # Minimal retries for tests

# Process Analysis test settings
PROCESS_ANALYSIS = {
    'DEFAULT_TIMEOUT': 1,
    'MAX_RETRIES': 1,
    'BACKOFF_FACTOR': 0.1,
    'CONCURRENT_REQUESTS': 2
}

# Disable celery tasks during testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True 