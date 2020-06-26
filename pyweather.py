#!/usr/bin/env python3
# coding=utf-8

import requests

"""
    This script queries your approximate location from ipinfo.io. It then requests the weather forecast to the metaweather.com API
    It will print the extended forecast for the biggest city closer to your location
"""

my_info = requests.get('https://ipinfo.io').json()
cities_around = requests.get('https://www.metaweather.com/api/location/search/?lattlong=' + my_info['loc'])
closer_city = cities_around.json()[0]

forecast = requests.get('https://www.metaweather.com/api/location/' + str(closer_city['woeid'])).json()

print('Extended forecast for ' + forecast['title'] + ' ' + forecast['location_type'])
print('=' * 75)
print('Date             Forecast   Wind Speed (mph) Min (°C) Max (°C)   Humid (%)')
print('=' * 75)
for day in forecast['consolidated_weather']:
    properties = [
        day['applicable_date'],
        day['weather_state_name'],
        day['wind_direction_compass'],
        day['wind_speed'],
        day['min_temp'],
        day['max_temp'],
        day['humidity']
    ]
    print('{:<10s}{:>15s}{:>7s}{:>12.1f}{:>9.1f}{:>9.1f}{:>12.1f}'.format(*properties))