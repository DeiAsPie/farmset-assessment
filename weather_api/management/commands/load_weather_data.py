import requests
from django.core.management.base import BaseCommand

from weather_api.models import Region, WeatherData, WeatherParameter


class Command(BaseCommand):
    help = "Load initial weather data from UK MetOffice"

    def handle(self, *args, **options):
        self.stdout.write("Setting up weather data structure...")

        # Create UK regions
        regions = [
            ("UK", "United Kingdom"),
            ("England", "England"),
            ("Wales", "Wales"),
            ("Scotland", "Scotland"),
            ("Northern_Ireland", "Northern Ireland"),
        ]

        for code, name in regions:
            region, created = Region.objects.get_or_create(code=code, defaults={"name": name})
            if created:
                self.stdout.write(f"✓ Created region: {name}")

        # Create weather parameters
        parameters = [
            ("Tmax", "Maximum Temperature", "°C"),
            ("Tmin", "Minimum Temperature", "°C"),
            ("Tmean", "Mean Temperature", "°C"),
            ("Sunshine", "Sunshine Duration", "hours"),
            ("Rainfall", "Rainfall", "mm"),
        ]

        for code, name, unit in parameters:
            param, created = WeatherParameter.objects.get_or_create(code=code, defaults={"name": name, "unit": unit})
            if created:
                self.stdout.write(f"✓ Created parameter: {name}")

        # Add sample data for demonstration
        self.create_sample_data()

        # Optionally fetch real data from UK MetOffice
        if len(options.get("args", [])) > 0 and options["args"][0] == "--fetch-real":
            self.fetch_real_weather_data()

        self.stdout.write(self.style.SUCCESS("✅ Setup complete! Data structure ready."))

    def create_sample_data(self):
        """Create sample weather data for demonstration."""
        try:
            uk_region = Region.objects.get(code="UK")
            tmax_param = WeatherParameter.objects.get(code="Tmax")

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
                        "value": value,
                        "source_url": "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt",
                    },
                )
                if created:
                    count += 1

            self.stdout.write(f"✓ Created {count} sample weather records")

        except Exception as e:
            self.stdout.write(f"Sample data creation skipped: {str(e)}")

    def fetch_real_weather_data(self):
        """Fetch real weather data from UK MetOffice for demonstration."""
        try:
            self.stdout.write("🌐 Fetching real data from UK MetOffice...")

            # UK MetOffice URL as specified in assignment
            url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt"

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse the data (simple parsing for demonstration)
            lines = response.text.strip().split("\n")
            data_lines = [line for line in lines if line and not line.startswith("#") and not line.startswith("Year")]

            if data_lines:
                # Get models
                uk_region = Region.objects.get(code="UK")
                tmax_param = WeatherParameter.objects.get(code="Tmax")

                # Parse recent years only (for demo)
                recent_data = data_lines[-3:]  # Last 3 years
                count = 0

                for line in recent_data:
                    parts = line.split()
                    if len(parts) >= 13:  # Year + 12 months
                        year = int(parts[0])

                        # Annual average (parts[13] if available)
                        if len(parts) > 13 and parts[13] != "---":
                            try:
                                annual_value = float(parts[13])

                                weather_data, created = WeatherData.objects.get_or_create(
                                    region=uk_region,
                                    parameter=tmax_param,
                                    year=year,
                                    month=None,  # Annual data
                                    defaults={
                                        "value": annual_value,
                                        "source_url": url,
                                    },
                                )

                                if created:
                                    count += 1

                            except ValueError:
                                continue

                self.stdout.write(f"✅ Fetched and stored {count} real weather records from UK MetOffice")
            else:
                self.stdout.write("⚠️  No parseable data found in MetOffice response")

        except requests.RequestException as e:
            self.stdout.write(f"⚠️  Could not fetch real data: {str(e)}")
            self.stdout.write("   Using sample data instead (offline mode)")
        except Exception as e:
            self.stdout.write(f"⚠️  Data parsing error: {str(e)}")
