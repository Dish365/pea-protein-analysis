import os
import django
from django.conf import settings

def setup_django():
    """Configure Django settings if not already configured"""
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.django_app.core.settings.development')
        django.setup() 