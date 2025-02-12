from django.urls import path
from .views.process_views import (
    ProcessAnalysisView,
    ProcessAnalysisCreateView,
    ProcessAnalysisUpdateView,
    ProcessAnalysisSubmitView
)

app_name = "process_data"

urlpatterns = [
    # Base process endpoints
    path("", ProcessAnalysisView.as_view(), name="process-list"),
    path("<int:process_id>/", ProcessAnalysisView.as_view(), name="process-detail"),
    path("<int:process_id>/status/", ProcessAnalysisView.as_view(), name="process-status"),
    path("<int:process_id>/results/", ProcessAnalysisView.as_view(), name="process-results"),
    
    # Step-by-step analysis endpoints
    path("analysis/create/", ProcessAnalysisCreateView.as_view(), name="analysis-create"),
    path("analysis/<int:process_id>/update/", ProcessAnalysisUpdateView.as_view(), name="analysis-update"),
    path("analysis/<int:process_id>/submit/", ProcessAnalysisSubmitView.as_view(), name="analysis-submit"),
] 