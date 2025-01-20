from django.contrib import admin
from django.urls import path, include
from django.conf import settings

# API URL Patterns
api_urlpatterns = [
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
