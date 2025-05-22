#!/usr/bin/env python3
# coding=utf-8

import requests

"""
    This script queries your approximate location from ipinfo.io. It then requests the weather forecast to the wttr.in API
    It will print the extended forecast for the biggest city closer to your location
"""
import sys

city = "London" # Default city
if len(sys.argv) > 1:
    city = sys.argv[1]

# wttr.in can fetch weather directly using city name, and adding ?format=j1 gives json output
url = f"https://wttr.in/{city}?format=j1"
forecast_data = requests.get(url).json()

# For now, just print the raw json to see its structure
# Later we can parse this to print a formatted forecast
print(forecast_data)

# The old printing logic is commented out as it's specific to metaweather.com
# print('Extended forecast for ' + forecast['title'] + ' ' + forecast['location_type'])
# print('=' * 75)
# print('Date             Forecast   Wind Speed (mph) Min (°C) Max (°C)   Humid (%)')
# print('=' * 75)
# for day in forecast['consolidated_weather']:
#     properties = [
#         day['applicable_date'],
#         day['weather_state_name'],
#         day['wind_direction_compass'],
#         day['wind_speed'],
#         day['min_temp'],
#         day['max_temp'],
#         day['humidity']
#     ]
#     print('{:<10s}{:>15s}{:>7s}{:>12.1f}{:>9.1f}{:>9.1f}{:>12.1f}'.format(*properties))