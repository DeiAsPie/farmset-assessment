from django.core.management.base import BaseCommand
from weather_api.models import Region, WeatherParameter
import requests


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
            {'code': 'UK', 'name': 'United Kingdom'},
            {'code': 'England', 'name': 'England'},
            {'code': 'Wales', 'name': 'Wales'},
            {'code': 'Scotland', 'name': 'Scotland'},
            {'code': 'Northern_Ireland', 'name': 'Northern Ireland'},
        ]
        
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                code=region_data['code'],
                defaults={
                    'name': region_data['name']
                }
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')
        
        # Create initial weather parameters
        parameters_data = [
            {'code': 'Tmax', 'name': 'Maximum Temperature', 'unit': '°C'},
            {'code': 'Tmin', 'name': 'Minimum Temperature', 'unit': '°C'},
            {'code': 'Tmean', 'name': 'Mean Temperature', 'unit': '°C'},
            {'code': 'Sunshine', 'name': 'Sunshine Duration', 'unit': 'hours'},
            {'code': 'Rainfall', 'name': 'Rainfall', 'unit': 'mm'},
        ]
        
        for param_data in parameters_data:
            param, created = WeatherParameter.objects.get_or_create(
                code=param_data['code'],
                defaults={
                    'name': param_data['name'],
                    'unit': param_data['unit']
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
        from weather_api.models import WeatherData
        
        url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter_code}/date/{region_code}.txt"
        
        self.stdout.write(f'Fetching data from: {url}')
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Get region and parameter objects
        region = Region.objects.get(code=region_code)
        parameter = WeatherParameter.objects.get(code=parameter_code)
        
        # Parse data - simplified to handle annual data
        lines = response.text.strip().split('\n')
        created_count = 0
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('Year') and line != '':
                parts = line.split()
                if len(parts) >= 2:  # Year + at least one value
                    try:
                        year = int(parts[0])
                        # Use annual average (last column) if available, otherwise first data column
                        if len(parts) >= 14:  # Has annual column
                            annual_value = parts[13]
                        else:
                            annual_value = parts[1]  # First month value as fallback
                        
                        if annual_value != '---':
                            value = float(annual_value)
                            
                            weather_data, created = WeatherData.objects.get_or_create(
                                region=region,
                                parameter=parameter,
                                year=year,
                                month=None,  # Annual data
                                defaults={
                                    'value': value,
                                    'source_url': url
                                }
                            )
                            
                            if created:
                                created_count += 1
                                
                    except (ValueError, IndexError):
                        continue
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} weather records')
        )
