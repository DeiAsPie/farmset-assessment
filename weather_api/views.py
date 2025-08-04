from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import Region, WeatherParameter, WeatherData
from .serializers import RegionSerializer, WeatherParameterSerializer, WeatherDataSerializer


def home(request):
    """Simple frontend dashboard."""
    return render(request, 'weather_api/simple.html')


@api_view(['GET'])
def api_overview(request):
    """API overview endpoint."""
    return Response({
        'message': 'UK Weather Data API',
        'endpoints': {
            'weather_data': '/api/weather/',
            'regions': '/api/regions/',
            'parameters': '/api/parameters/'
        },
        'filters': {
            'region': '?region=UK',
            'year': '?year=2023',
            'parameter': '?parameter=Tmax'
        }
    })


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """Weather data API endpoint."""
    serializer_class = WeatherDataSerializer
    
    def get_queryset(self):
        queryset = WeatherData.objects.select_related('region', 'parameter').all()
        
        # Simple filtering
        region = self.request.query_params.get('region')
        year = self.request.query_params.get('year')
        parameter = self.request.query_params.get('parameter')
        
        if region:
            queryset = queryset.filter(region__code=region)
        if year:
            queryset = queryset.filter(year=year)
        if parameter:
            queryset = queryset.filter(parameter__code=parameter)
            
        return queryset.order_by('-year', '-month')


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """Regions API endpoint."""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class WeatherParameterViewSet(viewsets.ReadOnlyModelViewSet):
    """Weather parameters API endpoint."""
    queryset = WeatherParameter.objects.all()
    serializer_class = WeatherParameterSerializer
