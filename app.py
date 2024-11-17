#Import the needed libraries
from flask import Flask, request, jsonify, render_template
import requests
import json
import os

app = Flask(__name__)

# Create variable for api key of weather data
API_KEY = "6e680f832d420d4f3d161ab7fe2337ef"

# Create a JSON file which will store all input data
MARKERS_FILE = 'static/markers.json' 

# Ensure the markers.json file exists
if not os.path.exists(MARKERS_FILE):
    with open(MARKERS_FILE, 'w') as file:
        json.dump([], file)

# Ensure the upload directory exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Opens the homepage
@app.route("/")
def homepage():
    return render_template("maps.html")

# Create a route that sends data to the JSON file
@app.route('/weather', methods=['POST'])
def get_and_store_weather():
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']
    title = data['title']
    description = data['description']
    imageUrl = data.get('imageUrl', '')

    # Make request to OpenWeatherMap API for weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    response = requests.get(url)
    
    # Check that api accessed and get + edit information to preferred format
    if response.status_code == 200:
        weather_data = response.json()
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius as easier to comprehend by most people

        # Create a variable for each new marker that contains all the needed data
        new_marker = {
            'lat': lat,
            'lon': lon,
            'title': title,
            'description': description,
            'weather': weather_description,
            'temperature': round(temperature, 2),
            'imageUrl': imageUrl  
        }

        # Create a variable that calls the function which displays saved markers
        markers = load_markers()
        markers.append(new_marker)
        save_markers(markers)

        # Add to JSON file, the data scraped from the weather API
        return jsonify({
            'weather': weather_description,
            'temperature': round(temperature, 2),
        })
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

# Create a route that retrieves data from the JSON file
@app.route("/markers", methods=["GET"])
def get_markers():
    markers = load_markers()
    return jsonify(markers)

# Create a route that sends image upload to the JSON file
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the image file to the 'uploads' folder created earlier
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    return jsonify({'url': f'/static/uploads/{image.filename}'}) 

# Create a route that shows JSON data on webpage
def load_markers():
    with open(MARKERS_FILE, 'r') as file:
        return json.load(file)

# Create a route that saves new input from user to the JSON file
def save_markers(markers):
    with open(MARKERS_FILE, 'w') as file:
        json.dump(markers, file)

if __name__ == "__main__":
    app.run(debug=True)
