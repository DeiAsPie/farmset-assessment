"""weather_project URL Configuration - Simplified"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("weather_api.urls")),
]
