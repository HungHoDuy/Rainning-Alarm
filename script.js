const submitButton = document.getElementById("submit-button");
const locationInput = document.getElementById("location");
const weatherInfo = document.querySelector(".weather-info");

submitButton.addEventListener("click", () => {
  const location = locationInput.value;

  // Call the OpenWeatherMap API
  fetch(
    `https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=e71f41462402ed8af85f57e58283926b&units=metric`
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error("Location not found.");
      }
      return response.json();
    })
    .then((data) => {
      const weather = data.list[0].weather[0].main;
      if (weather === "Rain") {
        weatherInfo.textContent = "It's going to rain in the next hour!";
      } else {
        weatherInfo.textContent = "It's not going to rain
