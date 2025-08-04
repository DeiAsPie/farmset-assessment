from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API endpoints
router = DefaultRouter()
router.register(r'weather', views.WeatherDataViewSet, basename='weather')
router.register(r'regions', views.RegionViewSet)
router.register(r'parameters', views.WeatherParameterViewSet)

urlpatterns = [
    # Frontend
    path('', views.home, name='home'),
    
    # API
    path('api/', views.api_overview, name='api_overview'),
    path('api/', include(router.urls)),
]
