#!/usr/bin/env python
"""
Simple test script for FarmSetu Weather API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    """Test the main API endpoints."""
    print("🧪 Testing FarmSetu Weather API")
    print("=" * 50)
    
    endpoints = [
        ("Home", "/"),
        ("Regions", "/api/regions/"),
        ("Weather Parameters", "/api/weather-parameters/"),
        ("Weather Data", "/api/weather-data/"),
    ]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"{name}: {status}")
            if endpoint == "/" and response.status_code == 200:
                data = response.json()
                print(f"   Available endpoints: {len(data.get('endpoints', {}))}")
        except requests.RequestException as e:
            print(f"{name}: ❌ FAIL (Connection error)")

if __name__ == "__main__":
    print("Make sure Django server is running at http://127.0.0.1:8000")
    print("Run: python manage.py runserver")
    print()
    test_endpoints()
    print("\n✨ Test completed!")
