// 1. Define API URL and API key
const API_URL = "https://api.openweathermap.org/data/3.0/onecall";
const API_KEY = "e71f41462402ed8af85f57e58283926b";

// 2. Get user's location (latitude and longitude)
// You can use the Geolocation API to get the user's location
// or ask the user to enter their location manually
if ("geolocation" in navigator) {
  // Geolocation is supported
  navigator.geolocation.getCurrentPosition(position => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    // Use the latitude and longitude values to make an API request

    // 3. Make an API call to OpenWeatherMap to get the current weather data
    // Use the "exclude" parameter to exclude all weather data except hourly forecast
    // Use the "units" parameter to specify units (e.g. metric or imperial)
   const url = `${API_URL}?lat=${latitude}&lon=${longitude}&exclude=current,minutely,daily,alerts&units=metric&appid=${API_KEY}`;
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(data => {
        const hourlyData = data.hourly;

        // 5. Check if there is a high chance of rain in the next hour
   const willRain = hourlyData[0].pop > 0.5;

        // 6. Alert the user if there is a high chance of rain
   if (willRain) {
          alert("There is a high chance of rain in the next hour!");
        }
      })
      .catch(error => {
        console.error("Error fetching weather data:", error);
      });
  });
} else {
  // Geolocation is not supported
  console.error("Geolocation is not supported by this browser");
}

