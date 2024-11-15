import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from weather import get_current_weather  # Import the function for current weather

# Load the dataset
file_path = '/Users/biankasledzinska/Downloads/uva/year 2/python/scraping 2/weather_map/data/ship_samples_lat_lon.xlsx'  # Replace with your actual file path
data = pd.read_excel(file_path)

# Helper function to convert degrees, minutes, seconds to decimal degrees
def dms_to_decimal(degrees, minutes, seconds):
    return abs(degrees) + minutes / 60 + seconds / 3600

# Convert latitude and longitude to decimal degrees with hemisphere correction
def convert_dms(row):
    lat = dms_to_decimal(row['lat (degrees)'], row['lat (minutes)'], row['lat (seconds)'])
    lon = dms_to_decimal(row['long (degrees)'], row['long (minutes)'], row['long (seconds)'])
    
    # Adjust latitude and longitude based on hemisphere
    if row['lat (degrees)'] < 0:
        lat = -lat
    if row['long (degrees)'] < 0:
        lon = -lon
    
    return pd.Series({'latitude': lat, 'longitude': lon})

# Apply conversion to the dataset
data[['latitude', 'longitude']] = data.apply(convert_dms, axis=1)

# Convert the 'date' column to datetime format for sorting
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date')  # Sort by date to show routes in order

# Define color for each flag type
data['flag_description'] = data['flag (1 = contaminated; 2 = low pressure)'].map({
    1: 'Contaminated',
    2: 'Low Pressure'
}).fillna('Normal')

# Prepare the figure for plotting
fig = go.Figure()

# Plot each point and add line segments to connect them sequentially
for index, row in data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    
    # Fetch current weather for each point
    temperature, humidity, wind_speed = get_current_weather(lat, lon)
    
    # Display the weather data as part of the hovertext
    hovertext = f"Source: {row['Source']}<br>Date: {row['date'].date()}<br>Flag: {row['flag_description']}"
    
    if temperature is not None:
        hovertext += f"<br>Temperature: {temperature}°C"
    if humidity is not None:
        hovertext += f"<br>Humidity: {humidity}%"
    if wind_speed is not None:
        hovertext += f"<br>Wind Speed: {wind_speed} m/s"
    
    # Add point to the map
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lat=[lat],
        lon=[lon],
        marker=dict(size=8, color='green'),
        name=row['flag_description'],
        hoverinfo='text',
        hovertext=hovertext,
        visible=True  # Set visibility to True so points show up
    ))

# Create frames for the timeline animation
frames = []
for i in range(len(data)):
    frames.append(
        go.Frame(
            data=[go.Scattermapbox(
                mode="markers",
                lat=[data['latitude'].iloc[i]],
                lon=[data['longitude'].iloc[i]],
                marker=dict(size=8, color='green'),
                hoverinfo='text',
                hovertext=f"Source: {data['Source'].iloc[i]}<br>Date: {data['date'].iloc[i].date()}<br>Flag: {data['flag_description'].iloc[i]}"
            )],
            name=f'show_{i}'  # Naming frames to link to the slider steps
        )
    )

# Layout customizations for aesthetics and clarity
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        center=dict(lat=data['latitude'].mean(), lon=data['longitude'].mean()),
        zoom=2
    ),
    title="Ship Air Sample Collection Data",
    title_x=0.5,
    showlegend=False,  # Hide the legend to minimize clutter
    margin={"r":0, "t":50, "l":0, "b":0},  # Adjust margins for a cleaner look
    updatemenus=[{
        'buttons': [{
            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
            'label': '▶️ Play',
            'method': 'animate'
        }, {
            'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
            'label': '⏸️ Pause',
            'method': 'animate'
        }],
        'direction': 'left',
        'pad': {'r': 10, 't': 10},  # Adjust the padding to keep buttons compact
        'showactive': False,
        'type': 'buttons',
        'x': 0.5,
        'xanchor': 'center',
        'y': -0.2,  # Positioning play button below the slider
        'yanchor': 'top',
        'font': {'size': 20},  # Slightly larger button font
        'bgcolor': 'rgba(255, 255, 255, 0.7)'  # Add background color to buttons
    }],
    sliders=[{
        'active': 0,
        'yanchor': 'top',
        'y': 0.85,  # Position the slider just below the title
        'xanchor': 'center',
        'x': 0.5,
        'currentvalue': {
            'font': {'size': 20},
            'visible': True,
            'xanchor': 'center'
        },
        'len': 0.8,  # Slightly narrower slider for cleaner appearance
        'steps': [
            {
                'args': [
                    [f'show_{i}'],
                    {'frame': {'duration': 500, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 500}}
                ],
                'label': data['date'].iloc[i].strftime('%Y-%m-%d %H:%M'),
                'method': 'animate'
            }
            for i in range(len(data))
        ]
    }]
)

# Show map
fig.show()
