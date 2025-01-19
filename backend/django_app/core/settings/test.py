from .base import *

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Use in-memory cache for testing
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

# Use test FastAPI URL
FASTAPI_BASE_URL = 'http://testserver:8001/api/v1'
FASTAPI_TIMEOUT = 5  # Shorter timeout for tests
FASTAPI_RETRY_COUNT = 2  # Fewer retries for tests

# Process Analysis test settings
PROCESS_ANALYSIS = {
    'DEFAULT_TIMEOUT': 10,  # seconds
    'MAX_RETRIES': 2,
    'BACKOFF_FACTOR': 0.1,
    'CONCURRENT_REQUESTS': 5
}

# Disable celery tasks during testing
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable logging during tests unless explicitly needed
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
        'level': 'CRITICAL',
    },
} 