from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# API Version 1 URL Patterns
api_v1_patterns = [
    path("process/", include("process_data.urls", namespace="process_data")),
]

# Main URL Configuration
urlpatterns = [
    # Admin Interface
    path("admin/", admin.site.urls),

    # API Versions
    path("api/v1/", include((api_v1_patterns, "api_v1"), namespace="v1")),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
]

# Development Tools
if settings.DEBUG:
    # Debug Toolbar
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

# URL Pattern Documentation
"""
API URL Structure:

1. API Version 1 (/api/v1/):
   - Process Analysis API:
     * Base Path: /api/v1/process/
     * Endpoints:
       - List/Create: /api/v1/process/
       - Details: /api/v1/process/{id}/
       - Status: /api/v1/process/{id}/status/
       - Results: /api/v1/process/{id}/results/
       - Analysis:
         * Create: /api/v1/process/analysis/create/
         * Update Step: /api/v1/process/analysis/{id}/update/
         * Submit: /api/v1/process/analysis/{id}/submit/
         * Technical: /api/v1/process/analysis/{id}/technical/
         * Economic: /api/v1/process/analysis/{id}/economic/
         * Environmental: /api/v1/process/analysis/{id}/environmental/

2. Admin Interface:
   - Path: /admin/
   - Django Admin interface for database management

3. Development Tools (DEBUG mode only):
   - Debug Toolbar: /__debug__/
"""
