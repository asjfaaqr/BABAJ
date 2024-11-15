import requests

# Your OpenWeatherMap API key
API_KEY = "277fad684e1a0edac56dff6200adffb8"  # Replace with your actual API key

def get_current_weather(lat, lon):
    """
    Get current weather data for a specific location using OpenWeatherMap API.
    
    :param lat: Latitude of the location
    :param lon: Longitude of the location
    :return: Weather data including temperature, humidity, and wind speed
    """
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"  # Get the temperature in Celsius, change to 'imperial' for Fahrenheit
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Extract relevant weather data
        temperature = data.get('main', {}).get('temp', None)
        humidity = data.get('main', {}).get('humidity', None)
        wind_speed = data.get('wind', {}).get('speed', None)
        return temperature, humidity, wind_speed
    else:
        print(f"Error fetching weather data: {response.status_code} - {response.text}")
        return None, None, None
