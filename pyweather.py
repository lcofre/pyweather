#!/usr/bin/env python3
# coding=utf-8

import requests

"""
    This script queries your approximate location from ipinfo.io. It then requests the weather forecast to the wttr.in API
    It will print the extended forecast for the biggest city closer to your location
"""
import sys

def get_weather_data(city):
    """Fetches weather data for a given city from wttr.in."""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        print(f"Error fetching weather data: {e}", file=sys.stderr)
        return None

def main():
    """Main function to get city and print weather data."""
    city = "London"  # Default city
    if len(sys.argv) > 1:
        city = sys.argv[1]

    forecast_data = get_weather_data(city)

    if forecast_data:
        print(forecast_data)

if __name__ == "__main__":
    main()