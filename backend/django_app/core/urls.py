from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, ProcessStepViewSet, AnalysisViewSet

router = DefaultRouter()
router.register(r"equipment", EquipmentViewSet)
router.register(r"process-steps", ProcessStepViewSet)
router.register(r"analyses", AnalysisViewSet, basename="analysis")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
