from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'ahmedabad')  # Default to Ahmedabad if no city is provided

    API_KEY = '2542fd86bb601bb39175e2c2f7d85729'  # Add your OpenWeather API key here
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}

    try:
        data = requests.get(url, params=params).json()

        if data.get('cod') != 200:
            raise KeyError  # Handle cases where the API response is an error

        weather_info = {
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'temp': data['main']['temp'],
            'day': datetime.date.today(),
            'city': city,
            'exception_occurred': False
        }

    except KeyError:
        messages.error(request, 'Entered data is not available to API')
        weather_info = {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'city': 'ahmedabad',
            'exception_occurred': True
        }

    return render(request, 'weatherapp/index.html', weather_info)
