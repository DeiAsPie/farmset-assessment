from django.db import models
from django.utils import timezone


class Region(models.Model):
    """Model to store UK regions."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WeatherParameter(models.Model):
    """Model to store weather parameters like Tmax, Tmin, etc."""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    unit = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ['name']


class WeatherData(models.Model):
    """Model to store parsed weather data from UK MetOffice."""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='weather_data')
    parameter = models.ForeignKey(WeatherParameter, on_delete=models.CASCADE, related_name='weather_data')
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    value = models.FloatField()
    source_url = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        period = f"{self.year}" if self.month is None else f"{self.year}-{self.month:02d}"
        return f"{self.region.name} - {self.parameter.name} - {period}: {self.value}"

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['region', 'parameter', 'year', 'month']
