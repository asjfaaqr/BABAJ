let map;
let markers = [];

async function initMap() {
  const { Map, Marker, InfoWindow, Circle } = await google.maps.importLibrary("maps");

  // Initialize the map with a default center
  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 4,
    mapTypeId: "satellite",
  });

  // Get and center the map to the user's location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      map.setCenter({ lat, lng: lon });
      map.setZoom(15);

      // Show user's location with a blue circle to make it easier for them to add the marker on their location
      const userLocationCircle = new Circle({
        center: { lat, lng: lon },
        radius: 50,
        fillColor: 'blue',
        fillOpacity: 0.35,
        strokeColor: 'blue',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        clickable: false,
        map: map
      });
    }, () => {
      alert("Geolocation is not supported by your browser.");
    });
  }

  // Call the function to show saved markers from the JSON file
  loadMarkers();

  // Create an Event listener to add new marker
  map.addListener("click", async function (event) {
    const lat = event.latLng.lat();
    const lon = event.latLng.lng();

    // Create prompts to get the needed input from user
    const title = prompt("Enter your name:");
    const description = prompt("How did the flask collection go today?");

    // Guide user to upload image by a popup alert
    alert("Please upload an image file."); 

    // Create prompts to get the image input from user
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.click();

    fileInput.addEventListener("change", async function (e) {
      const file = e.target.files[0];
      if (file) {
        const formData = new FormData();
        formData.append("image", file);

        // Call the route to save images in the backend
        const imageResponse = await fetch("/upload", {
          method: 'POST',
          body: formData,
        });

        // Get the image URL from the JSON file
        const imageData = await imageResponse.json();
        const imageUrl = imageData.url; 


         //  Call the route to save the data in the backend
        if (title && description) {
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
              imageUrl: imageUrl 
            }),
          });

          //  Create an infowindow that displays all the needed data
          const weatherData = await response.json();
          const infoWindowContent = `
            <div>
              <strong>${title}</strong><br>
              ${description}<br>
              Weather: ${weatherData.weather}<br>
              Temperature: ${weatherData.temperature}°C<br>
              <img src="${imageUrl}" alt="Uploaded Image" style="max-width: 200px;" />
            </div>
          `;

           //  Add a new marker on the maps 
          const newMarker = new google.maps.Marker({
            position: { lat, lng: lon },
            map: map,
          });

          //  Add the infowindow to the html page
          const infoWindow = new google.maps.InfoWindow({
            content: infoWindowContent,
          });

          // Display the infowindow when marker clicked
          newMarker.addListener("click", () => {
            infoWindow.open(map, newMarker);
          });

          // Save the new marker in the JSON file
          saveMarker(lat, lon, title, description, imageUrl);
        }
      }
    });
  });
}

//  Call the route to display the data from JSON file
async function loadMarkers() {
  const response = await fetch("/markers");
  const markerData = await response.json();

  markerData.forEach(marker => {
    const { lat, lon, title, description, weather, temperature, imageUrl } = marker;
    //  Display information in infowindow 
    const infoWindowContent = `
      <div>
        <strong>${title}</strong><br>
        ${description}<br>
        Weather: ${weather}<br>
        Temperature: ${temperature}°C<br>
        <img src="${imageUrl}" alt="Uploaded Image" style="max-width: 200px;" />
      </div>
    `;

    //  Display a new marker on the maps 
    const newMarker = new google.maps.Marker({
      position: { lat, lng: lon },
      map: map,
    });

    const infoWindow = new google.maps.InfoWindow({
      content: infoWindowContent,
    });

   // Display infowindow when marker clicked
    newMarker.addListener("click", () => {
      infoWindow.open(map, newMarker);
    });
  });
}


 // Save new marker informartion to JSON file
async function saveMarker(lat, lon, title, description, imageUrl) {
  await fetch('/weather', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      lat: lat,
      lon: lon,
      title: title,
      description: description,
      imageUrl: imageUrl 
    }),
  });
}

initMap();
