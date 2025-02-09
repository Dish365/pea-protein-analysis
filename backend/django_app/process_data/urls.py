from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProcessAnalysisViewSet

router = DefaultRouter()
router.register(r'', ProcessAnalysisViewSet, basename='process')

app_name = 'process_data'

urlpatterns = [
    path('', include(router.urls)),
]

# URL Pattern Documentation
"""
API Endpoints for Process Analysis:

1. List/Create Process Analysis
   - Path: /api/v1/process/
   - Methods:
     * GET: List all processes
     * POST: Create new process analysis
   
2. Process Details
   - Path: /api/v1/process/{id}/
   - Methods:
     * GET: Get detailed information about specific process
   
3. Analysis Status
   - Path: /api/v1/process/{id}/status/
   - Methods:
     * GET: Get current status and progress of analysis
   
4. Analysis Results
   - Path: /api/v1/process/{id}/results/
   - Methods:
     * GET: Get complete analysis results
"""
