function fethDataFrompOpenWeather() {

    const lat = 50.126825;
    const lon = 14.464630;
    const appid = "e89b9eec0a2a2f4138996a47e5e03c4e";
    baseUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${appid}&units=metric`;

    fetch(baseUrl)
        .then(response => {
            if (!response.ok) throw new Error('Network error');
                return response.json();
        })
        .then(data => {
            console.log('Weather data:', data);
            document.getElementById('weatherBox').textContent = `🌤️ ${data.main.temp}°C in ${data.name}`;
        })
        .catch(error => {
            console.error('Fetch error:', error);
    });
}

setInterval(fethDataFrompOpenWeather, 1000*60*5);
