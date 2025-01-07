# Database setup script
$dbName = "pea_protein_db"

# Check if psql is available
try {
    $psqlVersion = psql --version
    Write-Host "PostgreSQL client found: $psqlVersion"
} catch {
    Write-Error "PostgreSQL is not installed or not in PATH"
    exit 1
}

# Create database if it doesn't exist
$dbExists = psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$dbName'"
if ($dbExists) {
    Write-Host "Database '$dbName' already exists"
} else {
    Write-Host "Creating database '$dbName'..."
    psql -U postgres -c "CREATE DATABASE $dbName"
}

# Create Django database settings file
$dbSettingsPath = "backend\django_app\settings\database.py"
$dbSettings = @"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$dbName',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"@

New-Item -ItemType File -Path $dbSettingsPath -Force
Set-Content -Path $dbSettingsPath -Value $dbSettings

# Update base.py to include database settings
$basePath = "backend\django_app\settings\base.py"
$baseSettings = @"
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-your-secret-key-here'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'process_data',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Import database settings
from .database import DATABASES

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"@

Set-Content -Path $basePath -Value $baseSettings

# Create core/urls.py
$urlsPath = "backend\django_app\core\urls.py"
$urlsContent = @"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
"@

New-Item -ItemType File -Path $urlsPath -Force
Set-Content -Path $urlsPath -Value $urlsContent

Write-Host "`nDatabase configuration completed!"
Write-Host "Next steps:"
Write-Host "1. Run Django migrations:"
Write-Host "   cd backend\django_app"
Write-Host "   python manage.py makemigrations"
Write-Host "   python manage.py migrate"
Write-Host "2. Create a superuser:"
Write-Host "   python manage.py createsuperuser" 