from django.db import models
from django.utils import timezone


class Region(models.Model):
    """UK regions for weather data."""

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class WeatherParameter(models.Model):
    """Weather parameters like Tmax, Tmin, etc."""

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    unit = models.CharField(max_length=20, default="°C")

    def __str__(self):
        return f"{self.name} ({self.unit})"


class WeatherData(models.Model):
    """Parsed weather data from UK MetOffice."""

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(WeatherParameter, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)  # null for annual data
    value = models.FloatField()
    source_url = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        period = (
            f"{self.year}" if self.month is None else f"{self.year}-{self.month:02d}"
        )
        return f"{self.region.name} {self.parameter.name} {period}: {self.value}"

    class Meta:
        unique_together = ["region", "parameter", "year", "month"]
        ordering = ["-year", "-month"]
