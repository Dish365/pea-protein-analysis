from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, ProcessStepViewSet, AnalysisViewSet

# API Router for ViewSets
router = DefaultRouter()
router.register(r"equipment", EquipmentViewSet)
router.register(r"process-steps", ProcessStepViewSet)
router.register(r"analyses", AnalysisViewSet, basename="analysis")

# API URL Patterns
api_urlpatterns = [
    path("", include(router.urls)),
    path("process/", include("process_data.urls")),
]

# Main URL Patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urlpatterns)),
]

# Debug Toolbar (Development Only)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
