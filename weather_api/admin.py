from django.contrib import admin
from .models import Region, WeatherParameter, WeatherData


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(WeatherParameter)
class WeatherParameterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'unit']
    search_fields = ['name', 'code']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['region', 'parameter', 'year', 'month', 'value', 'created_at']
    list_filter = ['region', 'parameter', 'year']
    search_fields = ['region__name', 'parameter__name']
    ordering = ['-year', '-month']
