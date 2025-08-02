# FarmSetu Weather Data API

A Django application that parses UK MetOffice weather data and serves it via REST API with a frontend visualization interface.

## 🌟 Features

- **📊 Data Parsing**: Fetches and parses summarized weather data from UK MetOffice
- **🔌 REST API**: RESTful endpoints for accessing weather data with filtering and pagination
- **📈 Frontend**: HTML/JavaScript visualization dashboard
- **💾 Database**: SQLite/PostgreSQL for data storage with optimized queries
- **🐳 Docker**: Containerized deployment ready
- **☁️ Cloud Ready**: Azure deployment configuration included
- **📱 Responsive**: Mobile-friendly web interface

## 🚀 Quick Start

### Local Development

1. **Clone and Setup**
   ```powershell
   git clone <repository-url>
   cd "farmset assessment"
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_weather_data
   ```

3. **Run Development Server**
   ```powershell
   python manage.py runserver
   ```

4. **Access the Application**
   - **Home Page**: http://localhost:8000/
   - **API**: http://localhost:8000/api/
   - **Admin**: http://localhost:8000/admin/
   - **Frontend Dashboard**: Open `frontend/index.html` in browser

### Docker Deployment

```powershell
docker-compose up --build
```

### Azure Deployment

```powershell
# Using PowerShell (Windows)
.\deploy-azure.ps1

# Using Bash (Linux/Mac)
./deploy-azure.sh
```

## 📚 API Documentation

### Base URL
- Local: `http://localhost:8000/api/`
- Azure: `http://your-app.eastus.azurecontainer.io:8000/api/`

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API overview and documentation |
| `/api/regions/` | GET | List all available regions |
| `/api/parameters/` | GET | List all weather parameters |
| `/api/weather/` | GET | List weather data with filtering |
| `/api/weather/{id}/` | GET | Get specific weather record |
| `/api/weather/by_region/` | GET | Filter by region code |
| `/api/weather/by_parameter/` | GET | Filter by parameter code |
| `/api/weather/statistics/` | GET | Get weather statistics |
| `/api/fetch-weather-data/` | POST | Fetch new data from MetOffice |

### Query Parameters

- `?region=UK` - Filter by region code
- `?parameter=Tmax` - Filter by parameter code  
- `?year_from=2020&year_to=2023` - Filter by year range
- `?page=1` - Pagination

### Example Requests

```powershell
# Get UK maximum temperature data for 2023
curl "http://localhost:8000/api/weather/?region=UK&parameter=Tmax&year_from=2023"

# Get weather statistics
curl "http://localhost:8000/api/weather/statistics/"

# Fetch new data from MetOffice
curl -X POST "http://localhost:8000/api/fetch-weather-data/" \
     -H "Content-Type: application/json" \
     -d '{"region":"UK","parameter":"Tmax"}'
```

## 🏗️ Project Structure

```
farmset assessment/
├── weather_project/          # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── weather_api/             # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # API views and logic
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin interface
│   └── management/          # Custom commands
│       └── commands/
│           └── load_weather_data.py
├── templates/               # HTML templates
│   └── weather_api/
│       └── home.html        # Home page template
├── frontend/                # Frontend dashboard
│   └── index.html           # Single-page application
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container setup
├── deploy-azure.ps1        # Azure deployment (Windows)
├── deploy-azure.sh         # Azure deployment (Linux/Mac)
└── README.md               # This file
```

## 🗄️ Database Models

### Region
- Stores UK regions (UK, England, Wales, Scotland, Northern Ireland)
- Fields: `name`, `code`, `description`

### WeatherParameter  
- Stores weather parameters (Tmax, Tmin, Rainfall, etc.)
- Fields: `name`, `code`, `unit`, `description`

### WeatherData
- Main weather data records
- Fields: `region`, `parameter`, `year`, `month`, `value`, `source_url`
- Indexed for optimal query performance

### DataSource
- Tracks data sources and update times
- Fields: `name`, `url`, `region`, `parameter`, `last_updated`

## 🔧 Configuration

### Environment Variables

```bash
DEBUG=False                    # Debug mode
SECRET_KEY=your-secret-key    # Django secret key
DATABASE_URL=sqlite:///db.sqlite3  # Database URL
ALLOWED_HOSTS=*               # Allowed hosts
```

### Development Settings

The application uses SQLite for development and supports PostgreSQL for production. All settings are configured in `weather_project/settings.py`.

## 📊 Frontend Dashboard

The frontend provides:
- **Interactive Charts**: Time-series visualization using Chart.js
- **Data Filtering**: By region, parameter, and year range
- **Statistics**: Real-time calculations (avg, min, max)
- **Data Table**: Tabular view of recent records
- **Responsive Design**: Works on desktop and mobile

## 🐳 Docker Support

### Single Container
```powershell
docker build -t farmset-weather .
docker run -p 8000:8000 farmset-weather
```

### Multi-Container with Redis
```powershell
docker-compose up --build
```

The Docker setup includes:
- Django application
- Redis for caching
- SQLite database (persistent volume)
- Health checks
- Non-root user for security

## ☁️ Azure Deployment

### Prerequisites
- Azure CLI installed
- Azure subscription
- Docker installed

### Deployment Steps
1. Run deployment script: `.\deploy-azure.ps1`
2. Create superuser: `az container exec --exec-command "python manage.py createsuperuser"`
3. Load sample data: `az container exec --exec-command "python manage.py load_weather_data"`

### Azure Resources Created
- Resource Group
- Container Registry
- Container Instance
- Public IP with DNS label

## 🧪 Testing

```powershell
# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 Performance Features

- **Database Indexing**: Optimized queries with proper indexes
- **Pagination**: API results are paginated (50 records per page)
- **Caching**: Redis caching for frequently accessed data
- **Query Optimization**: select_related() for efficient database queries
- **Static Files**: WhiteNoise for static file serving

## 🔒 Security Features

- **Environment Variables**: Sensitive data in environment variables
- **CORS**: Configured for frontend access
- **Debug Mode**: Disabled in production
- **Secret Key**: Randomly generated for deployment
- **Admin Protection**: Django admin with authentication

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones
- Different screen orientations

## 🤝 Assessment Completion Checklist

✅ **Project Setup** - Django with proper structure and configuration  
✅ **Data Parsing** - UK MetOffice data fetching and parsing functionality  
✅ **Data Modeling** - Comprehensive Django models with relationships  
✅ **API Development** - RESTful API with filtering, pagination, and statistics  
✅ **Frontend** - Interactive dashboard with charts and data visualization  
✅ **Docker** - Full containerization with docker-compose  
✅ **Deployment** - Azure-ready configuration with automated deployment  
✅ **Git Workflow** - Proper version control structure  
✅ **Cloud Hosting** - Production-ready Azure deployment scripts  
✅ **Documentation** - Comprehensive README and API documentation  

## 🔄 Data Sources

The application fetches data from UK MetOffice climate datasets:
- **Base URL**: `https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/`
- **Format**: `{parameter}/date/{region}.txt`
- **Example**: `Tmax/date/UK.txt` for UK maximum temperature data

### Supported Regions
- UK (United Kingdom)
- England
- Wales  
- Scotland
- Northern_Ireland

### Supported Parameters
- **Tmax**: Maximum Temperature (°C)
- **Tmin**: Minimum Temperature (°C)
- **Tmean**: Mean Temperature (°C)
- **Sunshine**: Sunshine Duration (hours)
- **Rainfall**: Rainfall (mm)

## 🚨 Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure virtual environment is activated
2. **Database errors**: Run `python manage.py migrate`
3. **Permission errors**: Check file permissions and user settings
4. **API errors**: Verify UK MetOffice URLs are accessible
5. **Docker issues**: Ensure Docker daemon is running

### Getting Help

1. Check the Django admin panel for data verification
2. Use the API overview endpoint `/api/` for endpoint testing
3. Check container logs: `docker logs <container-name>`
4. Verify Azure deployment: `az container show --name farmset-weather-api`

## 📄 License

This project is developed as part of the FarmSetu technical assessment.

---

**Developed by**: [Your Name]  
**For**: FarmSetu Technical Assessment  
**Date**: August 2025
