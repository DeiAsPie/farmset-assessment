from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'regions', views.RegionViewSet)
router.register(r'weather-parameters', views.WeatherParameterViewSet)
router.register(r'weather-data', views.WeatherDataViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home_view, name='home'),
]
