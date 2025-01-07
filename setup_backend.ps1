# Create backend directory structure
$projectRoot = "C:\Users\USER\Desktop\Dev_Projects\nrc"

# Function to create directory if it doesn't exist
function EnsureDirectory {
    param([string]$path)
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created directory: $path"
    }
}

# Function to create Python file with basic content
function CreatePythonFile {
    param(
        [string]$path,
        [string]$content = ""
    )
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Path $path -Force | Out-Null
        Set-Content -Path $path -Value $content
        Write-Host "Created Python file: $path"
    }
}

# Create main backend directories
$dirs = @(
    "backend",
    "backend\django_app",
    "backend\django_app\settings",
    "backend\django_app\process_data",
    "backend\django_app\process_data\models",
    "backend\django_app\process_data\views",
    "backend\django_app\process_data\serializers",
    "backend\django_app\process_data\tests",
    "backend\django_app\core",
    "backend\fastapi_app",
    "backend\fastapi_app\process_analysis",
    "backend\fastapi_app\services",
    "backend\fastapi_app\models",
    "backend\fastapi_app\tests",
    "backend\rust_modules",
    "backend\rust_modules\src",
    "backend\rust_modules\src\protein_analysis",
    "backend\rust_modules\src\monte_carlo",
    "backend\rust_modules\src\matrix_ops",
    "backend\rust_modules\tests"
)

# Create directories
foreach ($dir in $dirs) {
    EnsureDirectory "$projectRoot\$dir"
}

# Create Django files
$djangoFiles = @{
    "backend\django_app\settings\__init__.py" = ""
    "backend\django_app\settings\base.py" = "# Base Django settings"
    "backend\django_app\settings\development.py" = "from .base import *`n`nDEBUG = True"
    "backend\django_app\settings\production.py" = "from .base import *`n`nDEBUG = False"
    "backend\django_app\process_data\models\__init__.py" = ""
    "backend\django_app\process_data\models\baseline.py" = "from django.db import models`n`n# Baseline process models"
    "backend\django_app\process_data\models\rf_treatment.py" = "from django.db import models`n`n# RF treatment models"
    "backend\django_app\process_data\models\ir_treatment.py" = "from django.db import models`n`n# IR treatment models"
    "backend\django_app\core\__init__.py" = ""
    "backend\django_app\core\models.py" = "from django.db import models`n`n# Core models"
    "backend\django_app\core\views.py" = "from django.views import View`n`n# Core views"
    "backend\django_app\core\serializers.py" = "from rest_framework import serializers`n`n# Core serializers"
    "backend\django_app\manage.py" = @"
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"@
}

# Create FastAPI files
$fastapiFiles = @{
    "backend\fastapi_app\main.py" = @"
from fastapi import FastAPI

app = FastAPI(title="Pea Protein Analysis API")

@app.get("/")
async def root():
    return {"message": "Pea Protein Analysis API"}
"@
    "backend\fastapi_app\process_analysis\protein_endpoints.py" = "from fastapi import APIRouter`n`n# Protein analysis endpoints"
    "backend\fastapi_app\process_analysis\economic_endpoints.py" = "from fastapi import APIRouter`n`n# Economic analysis endpoints"
    "backend\fastapi_app\process_analysis\environmental_endpoints.py" = "from fastapi import APIRouter`n`n# Environmental analysis endpoints"
    "backend\fastapi_app\services\calculations.py" = "# Core calculation services"
    "backend\fastapi_app\services\helpers.py" = "# Helper functions"
}

# Create Rust files
$rustFiles = @{
    "backend\rust_modules\src\lib.rs" = "// Main library file"
    "backend\rust_modules\src\protein_analysis\mod.rs" = "// Protein analysis module"
    "backend\rust_modules\src\monte_carlo\mod.rs" = "// Monte Carlo simulation module"
    "backend\rust_modules\src\matrix_ops\mod.rs" = "// Matrix operations module"
    "backend\rust_modules\Cargo.toml" = @"
[package]
name = 'pea_protein_analysis'
version = '0.1.0'
edition = '2021'

[dependencies]
"@
}

# Create all Python files
foreach ($file in $djangoFiles.Keys) {
    CreatePythonFile "$projectRoot\$file" $djangoFiles[$file]
}

foreach ($file in $fastapiFiles.Keys) {
    CreatePythonFile "$projectRoot\$file" $fastapiFiles[$file]
}

# Create all Rust files
foreach ($file in $rustFiles.Keys) {
    CreatePythonFile "$projectRoot\$file" $rustFiles[$file]
}

Write-Host "`nProject structure created successfully!"
Write-Host "Next steps:"
Write-Host "1. Create and activate Python virtual environment"
Write-Host "2. Install required Python packages"
Write-Host "3. Initialize Git repository"
Write-Host "4. Set up database configurations" 