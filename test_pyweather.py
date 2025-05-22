import unittest
from unittest.mock import patch, mock_open
import sys
import io # Required for StringIO

# Add the parent directory to sys.path to allow importing pyweather
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pyweather # Now pyweather can be imported

class TestWeatherData(unittest.TestCase):

    @patch('pyweather.requests.get')
    def test_get_weather_data_success(self, mock_get):
        # Configure the mock to return a successful response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": "10 C", "weather": "Sunny"}
        
        city = "TestCity"
        expected_url = f"https://wttr.in/{city}?format=j1"
        
        data = pyweather.get_weather_data(city)
        
        mock_get.assert_called_once_with(expected_url)
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(data, {"temperature": "10 C", "weather": "Sunny"})

    @patch('pyweather.requests.get')
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    def test_get_weather_data_request_exception(self, mock_stderr, mock_get):
        # Configure the mock to raise RequestException
        mock_get.side_effect = pyweather.requests.exceptions.RequestException("Test network error")
        
        city = "TestCity"
        data = pyweather.get_weather_data(city)
        
        self.assertIsNone(data)
        self.assertIn("Error fetching weather data: Test network error", mock_stderr.getvalue())

    @patch('pyweather.requests.get')
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr
    def test_get_weather_data_http_error(self, mock_stderr, mock_get):
        # Configure the mock response for an HTTP error
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = pyweather.requests.exceptions.HTTPError("404 Client Error")
        
        city = "TestCityNotFound"
        data = pyweather.get_weather_data(city)
        
        self.assertIsNone(data)
        # Check that raise_for_status was called, leading to the HTTPError
        mock_response.raise_for_status.assert_called_once()
        self.assertIn("Error fetching weather data: 404 Client Error", mock_stderr.getvalue())


class TestMainExecution(unittest.TestCase):

    @patch('pyweather.get_weather_data')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_city_argument(self, mock_stdout, mock_get_weather_data):
        # Mock get_weather_data to return specific data
        mock_get_weather_data.return_value = {"current_condition": [{"temp_C": "15"}]}
        
        # Patch sys.argv to simulate command line arguments
        with patch.object(sys, 'argv', ['pyweather.py', 'Paris']):
            pyweather.main()
            
        mock_get_weather_data.assert_called_once_with('Paris')
        self.assertEqual(mock_stdout.getvalue().strip(), "{'current_condition': [{'temp_C': '15'}]}")

    @patch('pyweather.get_weather_data')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_without_city_argument_uses_default(self, mock_stdout, mock_get_weather_data):
        # Mock get_weather_data
        mock_get_weather_data.return_value = {"current_condition": [{"temp_C": "10"}]}
        
        # Patch sys.argv for default city
        with patch.object(sys, 'argv', ['pyweather.py']):
            pyweather.main()
            
        mock_get_weather_data.assert_called_once_with('London') # Default city
        self.assertEqual(mock_stdout.getvalue().strip(), "{'current_condition': [{'temp_C': '10'}]}")

if __name__ == '__main__':
    unittest.main()
