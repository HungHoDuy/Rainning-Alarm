const apiKey = 'bd4ea33ecf905116d12af172e008dbae'; // Thay your_api_key bằng API key của bạn từ OpenWeatherMap
const baseUrl = 'https://api.openweathermap.org/data/2.5';
const weatherInfoEl = document.getElementById('weather-info');

function getWeatherData(city) {
  const url = `${baseUrl}/weather?q=${city}&appid=${apiKey}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const { coord } = data;
      const weatherUrl = `${baseUrl}/onecall?lat=${coord.lat}&lon=${coord.lon}&exclude=current,minutely,daily,alerts&appid=${apiKey}`;
      fetch(weatherUrl)
        .then(response => response.json())
        .then(data => {
          const { hourly } = data;
          const nextHour = new Date().getHours() + 1;
          const willRain = hourly.find(hour => {
            const hourTime = new Date(hour.dt * 1000).getHours();
            return hourTime === nextHour && hour.weather[0].main === 'Rain';
          });
          if (willRain) {
            weatherInfoEl.innerHTML = `
              <h2>It will rain in ${city} in the next hour</h2>
              <div class="icon"><i class="fas fa-cloud-showers-heavy"></i></div>
            `;
          } else {
            weatherInfoEl.innerHTML = `
              <h2>It will not rain in ${city} in the next hour</h2>
              <div class="icon"><i class="fas fa-sun"></i></div>
            `;
          }
          weatherInfoEl.style.display = 'block';
        })
        .catch(error => console.log(error));
    })
    .catch(error => console.log(error));
}

const formEl = document.querySelector('form');
formEl.addEventListener('submit', event => {
  event.preventDefault();
  const city = document.getElementById('location').value;
  getWeatherData(city);
});
