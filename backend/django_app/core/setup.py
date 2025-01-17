import os
import sys
from pathlib import Path

def setup_django_for_fastapi():
    """Set up Django environment for FastAPI integration"""
    # Get the path to the django_app directory
    django_path = Path(__file__).resolve().parent.parent
    
    # Add django_app to Python path
    sys.path.append(str(django_path))
    
    # Set up Django settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")
    
    # Set up Django
    import django
    django.setup() 