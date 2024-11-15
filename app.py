from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# OpenWeatherMap API Key
API_KEY = "6e680f832d420d4f3d161ab7fe2337ef"

@app.route("/")
def homepage():
    return render_template("maps.html")

@app.route('/weather', methods=['POST'])
def get_weather():
    # Get data from the frontend
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']
    title = data['title']
    description = data['description']

    # Make request to OpenWeatherMap API for weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()

        # Extracting the current weather and temperature
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius

        # Send weather data back to the frontend
        return jsonify({
            'weather': weather_description,
            'temperature': round(temperature, 2),  # Round the temperature to 2 decimal places
        })
    else:
        # Log the error for debugging
        print(f"Error: {response.status_code}, {response.text}")
        return jsonify({'error': 'Unable to fetch weather data'}), 500
