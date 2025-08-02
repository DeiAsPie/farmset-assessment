from django.core.management.base import BaseCommand
from weather_api.models import Region, WeatherParameter
import requests
from datetime import datetime


class Command(BaseCommand):
    help = 'Load initial weather data from UK MetOffice'

    def add_arguments(self, parser):
        parser.add_argument(
            '--region',
            default='UK',
            help='Region code (default: UK)',
        )
        parser.add_argument(
            '--parameter',
            default='Tmax',
            help='Weather parameter (default: Tmax)',
        )

    def handle(self, *args, **options):
        region_code = options['region']
        parameter_code = options['parameter']
        
        self.stdout.write(
            self.style.SUCCESS(f'Loading weather data for {region_code} - {parameter_code}')
        )
        
        # Create initial regions
        regions_data = [
            {'code': 'UK', 'name': 'United Kingdom', 'description': 'United Kingdom'},
            {'code': 'England', 'name': 'England', 'description': 'England'},
            {'code': 'Wales', 'name': 'Wales', 'description': 'Wales'},
            {'code': 'Scotland', 'name': 'Scotland', 'description': 'Scotland'},
            {'code': 'Northern_Ireland', 'name': 'Northern Ireland', 'description': 'Northern Ireland'},
        ]
        
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults={
                    'name': region_data['name'],
                    'description': region_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')
        
        # Create initial weather parameters
        parameters_data = [
            {'code': 'Tmax', 'name': 'Maximum Temperature', 'unit': '°C', 
             'description': 'Mean daily maximum temperature'},
            {'code': 'Tmin', 'name': 'Minimum Temperature', 'unit': '°C', 
             'description': 'Mean daily minimum temperature'},
            {'code': 'Tmean', 'name': 'Mean Temperature', 'unit': '°C', 
             'description': 'Mean temperature'},
            {'code': 'Sunshine', 'name': 'Sunshine Duration', 'unit': 'hours', 
             'description': 'Total sunshine duration'},
            {'code': 'Rainfall', 'name': 'Rainfall', 'unit': 'mm', 
             'description': 'Total rainfall'},
        ]
        
        for param_data in parameters_data:
            param, created = WeatherParameter.objects.get_or_create(
                code=param_data['code'],
                defaults={
                    'name': param_data['name'],
                    'unit': param_data['unit'],
                    'description': param_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created parameter: {param.name}')
        
        # Try to fetch sample data
        try:
            self.fetch_weather_data(region_code, parameter_code)
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not fetch weather data: {str(e)}')
            )
            self.stdout.write(
                'Sample data structure has been created. You can fetch data manually using the API.'
            )

    def fetch_weather_data(self, region_code, parameter_code):
        """Fetch weather data from UK MetOffice."""
        from weather_api.models import WeatherData, DataSource
        
        url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter_code}/date/{region_code}.txt"
        
        self.stdout.write(f'Fetching data from: {url}')
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Get region and parameter objects
        region = Region.objects.get(code=region_code)
        parameter = WeatherParameter.objects.get(code=parameter_code)
        
        # Parse data
        lines = response.text.strip().split('\n')
        created_count = 0
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('Year'):
                parts = line.split()
                if len(parts) >= 13:  # Year + 12 months
                    year = int(parts[0])
                    
                    # Process monthly data (limit to recent years for demo)
                    if year >= 2020:
                        for month, value_str in enumerate(parts[1:13], 1):
                            if value_str != '---':
                                try:
                                    value = float(value_str)
                                    
                                    weather_data, created = WeatherData.objects.get_or_create(
                                        region=region,
                                        parameter=parameter,
                                        year=year,
                                        month=month,
                                        defaults={
                                            'value': value,
                                            'source_url': url,
                                            'data_file': f'{region_code}_{parameter_code}.txt'
                                        }
                                    )
                                    
                                    if created:
                                        created_count += 1
                                        
                                except ValueError:
                                    continue
        
        # Update data source
        DataSource.objects.update_or_create(
            region=region,
            parameter=parameter,
            defaults={
                'name': f'{region_code} {parameter_code}',
                'url': url,
                'last_updated': datetime.now(),
                'is_active': True
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} weather records')
        )
