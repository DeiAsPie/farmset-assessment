# FarmSetu Weather API - Simplified

A clean, simplified Django REST API for UK MetOffice weather data that fulfills all assessment requirements with minimal complexity.

## ✅ Requirements Fulfilled

- **Project Setup**: Django 5.0.4 project with clean structure
- **Data Parsing**: Weather data fetching capabilities  
- **Data Modeling**: 3 core models (Region, WeatherParameter, WeatherData)
- **API**: RESTful endpoints with filtering
- **Frontend**: Clean dashboard for data visualization
- **Docker**: Single-container deployment
- **Cloud Deployment**: Azure-ready configuration

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Database
python manage.py migrate
python manage.py load_sample_data

# Run
python manage.py runserver
```

Access:
- **Home**: http://localhost:8000/
- **API**: http://localhost:8000/api/
- **Frontend**: http://localhost:8000/frontend/
- **Admin**: http://localhost:8000/admin/

## 🐳 Docker

```bash
docker-compose up --build
```

## 📊 API Endpoints

- `GET /api/regions/` - List all regions
- `GET /api/weather-parameters/` - List all weather parameters  
- `GET /api/weather-data/` - List weather data with filtering
- `GET /api/weather-data/?region=UK&year=2023` - Filter by region and year

## 📱 Frontend Features

- Clean, responsive design
- Region and parameter selection
- Year-based filtering
- Data table display
- Basic statistics

## 📋 Simplifications Made

✅ **Models**: Removed DataSource model, simplified fields  
✅ **Views**: Removed complex statistics and filtering  
✅ **Frontend**: Simplified UI, removed Chart.js dependency  
✅ **Dependencies**: Reduced from 9 to 5 packages  
✅ **Docker**: Single container setup  
✅ **Admin**: Simplified interface  

## 📦 Dependencies

- Django 5.0.4
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- whitenoise 6.6.0
- requests 2.31.0

## 🏗️ Project Structure

```
farmset assessment/
├── weather_project/          # Django settings
├── weather_api/             # Main app
│   ├── models.py            # 3 core models
│   ├── views.py             # Simple ViewSets
│   ├── serializers.py       # 3 serializers
│   └── management/commands/ # Sample data loader
├── frontend/                # Simple dashboard
├── templates/               # Home template
├── requirements.txt         # 5 dependencies
├── Dockerfile              # Container config
└── docker-compose.yml      # Single service
```

This simplified version maintains all core functionality while being much easier to understand, deploy, and maintain.
