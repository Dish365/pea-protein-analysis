"""Database configuration for Django application."""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',  # This will be created in your project root
        'TEST': {
            'NAME': 'test_db.sqlite3',
        },
    }
}

# Database configuration for different environments
DATABASE_CONFIGS = {
    'development': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev_db.sqlite3',
    },
    'testing': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    },
    'production': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nrc_db',
        'USER': 'nrc_user',
        'PASSWORD': '',  # Set this via environment variable
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Database routers
DATABASE_ROUTERS = []

# Database connection age (in seconds)
CONN_MAX_AGE = 60

# Database connection health check
DATABASE_HEALTH_CHECK_TIMEOUT = 5

# Maximum number of database connections
DATABASE_MAX_CONNECTIONS = 100

# Database SSL configuration
DATABASE_SSL_CONFIG = {
    'require': False,
    'verify-full': False,
    'ca': None,
    'cert': None,
    'key': None,
}

# Database backup configuration
DATABASE_BACKUP = {
    'BACKUP_PATH': 'backups/',
    'BACKUP_COUNT': 30,  # Number of backups to keep
    'COMPRESS': True,
}
