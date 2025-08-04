from django.core.management.base import BaseCommand
from weather_api.models import Region, WeatherParameter, WeatherData


class Command(BaseCommand):
    help = 'Load initial weather data from UK MetOffice'

    def handle(self, *args, **options):
        self.stdout.write('Setting up weather data structure...')
        
        # Create UK regions
        regions = [
            ('UK', 'United Kingdom'),
            ('England', 'England'),
            ('Wales', 'Wales'),
            ('Scotland', 'Scotland'),
            ('Northern_Ireland', 'Northern Ireland'),
        ]
        
        for code, name in regions:
            region, created = Region.objects.get_or_create(code=code, defaults={'name': name})
            if created:
                self.stdout.write(f'✓ Created region: {name}')
        
        # Create weather parameters
        parameters = [
            ('Tmax', 'Maximum Temperature', '°C'),
            ('Tmin', 'Minimum Temperature', '°C'),
            ('Tmean', 'Mean Temperature', '°C'),
            ('Sunshine', 'Sunshine Duration', 'hours'),
            ('Rainfall', 'Rainfall', 'mm'),
        ]
        
        for code, name, unit in parameters:
            param, created = WeatherParameter.objects.get_or_create(
                code=code, defaults={'name': name, 'unit': unit}
            )
            if created:
                self.stdout.write(f'✓ Created parameter: {name}')
        
        # Add sample data for demonstration
        self.create_sample_data()
        
        self.stdout.write(self.style.SUCCESS('✅ Setup complete! Data structure ready.'))

    def create_sample_data(self):
        """Create sample weather data for demonstration."""
        try:
            uk_region = Region.objects.get(code='UK')
            tmax_param = WeatherParameter.objects.get(code='Tmax')
            
            # Sample data for recent years
            sample_data = [
                (2023, None, 14.8),  # Annual average
                (2022, None, 13.9),
                (2021, None, 13.2),
                (2020, None, 13.5),
            ]
            
            count = 0
            for year, month, value in sample_data:
                weather_data, created = WeatherData.objects.get_or_create(
                    region=uk_region,
                    parameter=tmax_param,
                    year=year,
                    month=month,
                    defaults={
                        'value': value,
                        'source_url': 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt'
                    }
                )
                if created:
                    count += 1
                    
            self.stdout.write(f'✓ Created {count} sample weather records')
            
        except Exception as e:
            self.stdout.write(f'Sample data creation skipped: {str(e)}')
