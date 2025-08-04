from rest_framework import serializers
from .models import Region, WeatherParameter, WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    parameter_name = serializers.CharField(source='parameter.name', read_only=True)
    parameter_unit = serializers.CharField(source='parameter.unit', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = ['id', 'region_name', 'parameter_name', 'parameter_unit', 
                 'year', 'month', 'value', 'created_at']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'code']


class WeatherParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherParameter
        fields = ['id', 'name', 'code', 'unit']
