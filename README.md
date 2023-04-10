# Rainning-Alarm
An app that's warn the user if there will be a high chance of raining in the next hour
// 1. Define API URL and API key
const API_URL = "https://api.openweathermap.org/data/3.0/onecall";
const API_KEY = "YOUR_API_KEY_HERE";

// 2. Get user's location (latitude and longitude)
// You can use the Geolocation API to get the user's location
// or ask the user to enter their location manually

// 3. Make an API call to OpenWeatherMap to get the current weather data
// Use the "exclude" parameter to exclude all weather data except hourly forecast
// Use the "units" parameter to specify units (e.g. metric or imperial)
const url = `${API_URL}?lat=${LATITUDE}&lon=${LONGITUDE}&exclude=current,minutely,daily,alerts&units=metric&appid=${API_KEY}`;

// 4. Parse the API response to get the hourly forecast data
fetch(url)
  .then(response => response.json())
  .then(data => {
    const hourlyData = data.hourly;

    // 5. Check if there is a high chance of rain in the next hour
    const willRain = hourlyData[0].pop > 0.5;

    // 6. Alert the user if there is a high chance of rain
    if (willRain) {
      alert("There is a high chance of rain in the next hour!");
    }
  })
  .catch(error => console.error(error));
