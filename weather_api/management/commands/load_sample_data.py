from django.core.management.base import BaseCommand
from weather_api.models import Region, WeatherParameter, WeatherData


class Command(BaseCommand):
    help = 'Load sample weather data from UK MetOffice'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample weather data...')
        
        # Create sample regions
        regions = [
            {'name': 'UK', 'code': 'UK'},
            {'name': 'England', 'code': 'England'},
            {'name': 'Scotland', 'code': 'Scotland'},
        ]
        
        for region_data in regions:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults={'name': region_data['name']}
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')

        # Create sample parameters
        parameters = [
            {'name': 'Maximum Temperature', 'code': 'Tmax', 'unit': '°C'},
            {'name': 'Minimum Temperature', 'code': 'Tmin', 'unit': '°C'},
            {'name': 'Rainfall', 'code': 'Rainfall', 'unit': 'mm'},
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

        # Create sample data
        uk_region = Region.objects.get(code='UK')
        tmax_param = WeatherParameter.objects.get(code='Tmax')
        
        sample_data = [
            {'year': 2023, 'month': 1, 'value': 8.5},
            {'year': 2023, 'month': 2, 'value': 9.2},
            {'year': 2023, 'month': 3, 'value': 12.1},
            {'year': 2022, 'month': 12, 'value': 7.8},
        ]
        
        for data in sample_data:
            weather_data, created = WeatherData.objects.get_or_create(
                region=uk_region,
                parameter=tmax_param,
                year=data['year'],
                month=data['month'],
                defaults={
                    'value': data['value'],
                    'source_url': 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt'
                }
            )
            if created:
                self.stdout.write(f'Created data: {data}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample weather data!')
        )
