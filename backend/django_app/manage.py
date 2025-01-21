#!/usr/bin/env python
import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    # Add the parent directory to sys.path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
