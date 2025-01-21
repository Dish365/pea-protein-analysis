from django.urls import path
from .views.process_views import ProcessAnalysisView

app_name = 'process_data'  # Namespace for URL reversing

urlpatterns = [
    # Process Analysis Endpoints
    path('', 
         ProcessAnalysisView.as_view(),
         name='process-list-create'),  # GET: List all, POST: Create new
    
    path('<int:process_id>/',
         ProcessAnalysisView.as_view(),
         name='process-detail'),  # GET: Get specific process details
    
    path('<int:process_id>/status/',
         ProcessAnalysisView.as_view(),
         name='process-status'),  # GET: Get analysis status and progress
    
    path('<int:process_id>/results/',
         ProcessAnalysisView.as_view(),
         name='process-results'),  # GET: Get complete analysis results
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