from django.urls import path
from .views.process_views import ProcessAnalysisView

urlpatterns = [
    # List all processes and create new analysis
    path('', ProcessAnalysisView.as_view(), name='process-list'),
    
    # Process-specific endpoints
    path('<int:process_id>/', ProcessAnalysisView.as_view(), name='process-detail'),
    path('<int:process_id>/status/', ProcessAnalysisView.as_view(), name='process-status'),
    path('<int:process_id>/results/', ProcessAnalysisView.as_view(), name='process-results'),
] 