// MapTiler API Key
const key = 'wKra4Nb3f8CdrZdI9xb3';

 // Initialiseer de OpenLayers kaart (en gebruik OpenStreetMap)
const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM(), // Gebruik OpenStreetMap als basemap
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([0, 0]), // Beginpunt van de kaart
    zoom: 3
  })
});

// StormGlass API Key
const stormglassKey = '54c7076c-a2dc-11ef-9159-0242ac130003-54c707c6-a2dc-11ef-9159-0242ac130003';

// Functie om weerdata op te halen van de StormGlass API
async function getWeatherData(lat, lon) {
  const url = `https://api.stormglass.io/v2/weather/point?lat=${lat}&lng=${lon}&params=airTemperature,precipitation,windSpeed&source=sg`;

  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': stormglassKey
      }
    });

    if (!response.ok) {
      alert('Failed to retrieve weather data');
      return;
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching weather data:', error);
    alert('Error fetching weather data.');
  }
}

// Functie om weerdata weer te geven in een popup op de kaart
function displayWeatherPopup(lat, lon, data) {
  // Haal de eerste weerdata (uit de 'hours' array)
  const temperature = data.hours[0].airTemperature.value || 'N/A';
  const precipitation = data.hours[0].precipitation.value || 'N/A';
  const windSpeed = data.hours[0].windSpeed.value || 'N/A';

  const weatherInfo = `
    <div>
      <h3>Weather Information</h3>
      <p><strong>Temperature:</strong> ${temperature}°C</p>
      <p><strong>Precipitation:</strong> ${precipitation} mm</p>
      <p><strong>Wind Speed:</strong> ${windSpeed} m/s</p>
    </div>
  `;

  // Maak een popup om de weerdata weer te geven
  const popup = new ol.Overlay({
    element: document.createElement('div'),
    positioning: 'bottom-center',  // Popup onderaan het midden van de kaart
  });

  // Zet de HTML van de popup
  popup.getElement().innerHTML = weatherInfo;

  // Zet de popup positie op de kaart
  popup.setPosition(ol.proj.fromLonLat([lon, lat]));

  // Voeg de popup toe aan de kaart
  map.addOverlay(popup);

  // Zoom naar de locatie
  map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
  map.getView().setZoom(10); // Verander zoomniveau naar 10
}

// Handleer de gebruikersinvoer voor coördinaten
const inputButton = document.getElementById('getCoordinates');
inputButton.addEventListener('click', async function() {
  const latInput = document.getElementById('lat').value;  // Let op de ID 'lat'
  const lonInput = document.getElementById('lon').value;  // Let op de ID 'lon'

  if (latInput && lonInput) {
    const lat = parseFloat(latInput);
    const lon = parseFloat(lonInput);

    const weatherData = await getWeatherData(lat, lon);
    if (weatherData) {
      displayWeatherPopup(lat, lon, weatherData);
    }
  } else {
    alert('Please enter both latitude and longitude');
  }
}); 