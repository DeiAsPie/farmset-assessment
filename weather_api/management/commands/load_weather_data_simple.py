from django.core.management.base import BaseCommand
from weather_api.models import Region, WeatherParameter, WeatherData


class Command(BaseCommand):
    help = 'Load sample weather data'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample weather data...')
        
        # Create basic regions
        regions = [
            {'code': 'UK', 'name': 'United Kingdom'},
            {'code': 'England', 'name': 'England'},
            {'code': 'Scotland', 'name': 'Scotland'},
        ]
        
        for region_data in regions:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults={'name': region_data['name']}
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')
        
        # Create basic weather parameters  
        parameters = [
            {'code': 'Tmax', 'name': 'Maximum Temperature', 'unit': '°C'},
            {'code': 'Tmin', 'name': 'Minimum Temperature', 'unit': '°C'},
            {'code': 'Rainfall', 'name': 'Rainfall', 'unit': 'mm'},
        ]
        
        for param_data in parameters:
            param, created = WeatherParameter.objects.get_or_create(
                code=param_data['code'],
                defaults={
                    'name': param_data['name'], 
                    'unit': param_data['unit']
                }
            )
            if created:
                self.stdout.write(f'Created parameter: {param.name}')
        
        # Add sample weather data
        sample_data = [
            {'region': 'UK', 'parameter': 'Tmax', 'year': 2023, 'month': 1, 'value': 8.2},
            {'region': 'UK', 'parameter': 'Tmin', 'year': 2023, 'month': 1, 'value': 2.1},
            {'region': 'UK', 'parameter': 'Rainfall', 'year': 2023, 'month': 1, 'value': 89.5},
        ]
        
        for data in sample_data:
            region = Region.objects.get(code=data['region'])
            parameter = WeatherParameter.objects.get(code=data['parameter'])
            
            weather_data, created = WeatherData.objects.get_or_create(
                region=region,
                parameter=parameter,
                year=data['year'],
                month=data['month'],
                defaults={
                    'value': data['value'],
                    'source_url': 'https://www.metoffice.gov.uk/research/climate/maps-and-data'
                }
            )
            if created:
                self.stdout.write(f'Created weather data: {weather_data}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample weather data!')
        )
