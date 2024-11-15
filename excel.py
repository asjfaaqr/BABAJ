import pandas as pd

# read file
df = pd.read_excel("/Users/aya/Downloads/ship_samples_lat_lon.xlsx")

print(df.head())


df["Coordinates"] = df['lat (degrees)'].astype(str) + df['lat (minutes)'].astype(str) + df['lat (seconds)'].astype(str) + "," + df['long (degrees)'].astype(str) + df['long (minutes)'].astype(str) + df['long (seconds)'].astype(str)

print(df.head())


import requests

API_KEY = "6e680f832d420d4f3d161ab7fe2337ef"

# Complete URL for the API call
url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API_KEY}"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Here is the result from the API:")
    print(response.text)
    json_string = response.text
else:
    print("Error: Unable to get data from OpenWeatherMap API! :(")