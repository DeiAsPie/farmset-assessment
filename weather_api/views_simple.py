from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Region, WeatherParameter, WeatherData
from .serializers import RegionSerializer, WeatherParameterSerializer, WeatherDataSerializer
import requests
from django.http import JsonResponse


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Region model."""
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    ordering = ['name']


class WeatherParameterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for WeatherParameter model."""
    queryset = WeatherParameter.objects.all()
    serializer_class = WeatherParameterSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'code', 'unit']
    ordering_fields = ['name', 'code']
    ordering = ['name']


class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for WeatherData model."""
    queryset = WeatherData.objects.select_related('region', 'parameter').all()
    serializer_class = WeatherDataSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region', 'parameter', 'year', 'month']
    search_fields = ['region__name', 'parameter__name']
    ordering_fields = ['year', 'month', 'value', 'created_at']
    ordering = ['-year', '-month']

    @action(detail=False, methods=['post'])
    def fetch_data(self, request):
        """Fetch weather data from UK MetOffice."""
        try:
            url = request.data.get('url')
            if not url:
                return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            response = requests.get(url)
            response.raise_for_status()
            
            return Response({
                'message': 'Data fetched successfully',
                'url': url,
                'content_length': len(response.content)
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def home_view(request):
    """Simple home page with API information."""
    return JsonResponse({
        'message': 'Welcome to FarmSetu Weather API',
        'endpoints': {
            'regions': '/api/regions/',
            'parameters': '/api/weather-parameters/',
            'weather-data': '/api/weather-data/',
            'admin': '/admin/',
            'dashboard': '/frontend/'
        }
    })
