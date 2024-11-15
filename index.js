let map;

async function initMap() {
  const { Map, Marker, InfoWindow } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 4,
    maxZoom: 10,
    mapTypeId: "satellite",
  });

  map.addListener("click", async function (event) {
    const lat = event.latLng.lat(); // Latitude
    const lon = event.latLng.lng(); // Longitude

    console.log("Map clicked at:", lat, lon); // Check if this logs the coordinates correctly

    // Prompt the user for a title and description
    const title = prompt("Enter your name:");
    const description = prompt("How did the flask collection go today?");

    if (title && description) {
      // Send latitude, longitude, title, and description to the backend
      const response = await fetch('/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lat: lat,
          lon: lon,
          title: title,
          description: description,
        }),
      });

      const weatherData = await response.json();
      console.log("Weather data:", weatherData); // Check the weather data

      // Create the InfoWindow content with weather data
      const infoText = `
          <div>
            <strong>${title}</strong><br>
            ${description}<br>
            Weather: ${weatherData.weather}<br>
            Temperature: ${weatherData.temperature}°C
          </div>
        `;

      // Add a marker at the clicked location
      const marker = new google.maps.Marker({
        position: event.latLng,
        map: map,
      });

      // Create the InfoWindow
      const infoWindow = new google.maps.InfoWindow({
        content: infoText,
      });

      // Add a click event listener to the marker to show the InfoWindow
      marker.addListener("click", () => {
        console.log("Marker clicked");
        infoWindow.open(map, marker);
      });

    } else {
      alert("Both name and description are required to add a marker.");
    }
  });
}

initMap();