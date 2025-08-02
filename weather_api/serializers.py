from rest_framework import serializers
from .models import Region, WeatherParameter, WeatherData


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for Region model."""
    data_count = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'data_count']

    def get_data_count(self, obj):
        return obj.weather_data.count()


class WeatherParameterSerializer(serializers.ModelSerializer):
    """Serializer for WeatherParameter model."""
    data_count = serializers.SerializerMethodField()

    class Meta:
        model = WeatherParameter
        fields = ['id', 'name', 'code', 'unit', 'data_count']

    def get_data_count(self, obj):
        return obj.weather_data.count()


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer for WeatherData model."""
    region_name = serializers.CharField(source='region.name', read_only=True)
    parameter_name = serializers.CharField(source='parameter.name', read_only=True)
    parameter_unit = serializers.CharField(source='parameter.unit', read_only=True)

    class Meta:
        model = WeatherData
        fields = [
            'id', 'region', 'region_name', 'parameter', 'parameter_name', 
            'parameter_unit', 'year', 'month', 'value', 'source_url', 'created_at'
        ]
