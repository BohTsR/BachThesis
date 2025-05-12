let tempChart, humChart, coGauge, coGaugeText;

const coGaugeOpts = {
    angle: 0,
    lineWidth: 0.3,
    radiusScale: 1,
    pointer: {
    length: 0.6,
    strokeWidth: 0.035,
    color: '#000000'
    },
    limitMax: false,
    limitMin: false,
    colorStart: '#6FADCF',
    colorStop: '#8FC0DA',
    strokeColor: '#E0E0E0',
    generateGradient: true,
    highDpiSupport: true,
    staticZones: [
        { strokeStyle: "#30B32D", min: 0, max: 35 },
        { strokeStyle: "#FFDD00", min: 36, max: 100 },
        { strokeStyle: "#F03E3E", min: 101, max: 300 }
    ],
    staticLabels: {
        font: "12px sans-serif",
        labels: [0, 35, 100, 300],
        color: "#000",
        fractionDigits: 0
    }
};

const coGaugeTarget = document.getElementById('coGauge');
coGauge = new Gauge(coGaugeTarget).setOptions(coGaugeOpts);
coGauge.maxValue = 300;
coGauge.setMinValue(0);
coGauge.animationSpeed = 32;
coGauge.set(0);
coGaugeText = document.getElementById("coLevelText");

async function fetchTodayDataAndUpdateCharts() {
    try {
        const response = await fetch('SmartHome.json');
        if (!response.ok) return;
        const rawData = await response.json();

        const now = new Date();
        const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0);

        const filtered = rawData.filter(entry => {
            const ts = entry.timestamp * 1000;
            return entry.device_id === 'SmartHome' && ts >= startOfDay.getTime() && ts <= now.getTime();
        });

        const temperature = filtered.map(entry => ({ x: entry.timestamp * 1000, y: parseFloat(entry.temperature.toFixed(1)) }));
        const humidity = filtered.map(entry => ({ x: entry.timestamp * 1000, y: parseFloat(entry.humidity.toFixed(1)) }));
        const latestCO = filtered.length ? filtered[filtered.length - 1].co_gas : 0;

        const commonOptions = {
            elements: { line: { tension: 0.4 } },
            scales: {
                x: {
                type: 'time',
                time: { unit: 'hour', displayFormats: { hour: 'HH:mm' } },
                min: startOfDay.getTime(),
                max: now.getTime(),
                title: { display: true, text: 'Time' }
                },
                y: {
                beginAtZero: true,
                title: { display: true, text: 'Measurement' }
            }}
        };

        if (!tempChart) {
            const tempCtx = document.getElementById('temperatureTodayChart').getContext('2d');
            tempChart = new Chart(tempCtx, {
            type: 'line',
            data: { datasets: [{ label: 'Temperature', data: temperature, borderColor: 'rgba(255,99,132,1)', fill: false, pointRadius: 0 }] },
            options: commonOptions
        });
        } else {
            tempChart.options.scales.x.max = now.getTime();
            tempChart.data.datasets[0].data = temperature;
            tempChart.update();
        }

        if (!humChart) {
            const humCtx = document.getElementById('humidityTodayChart').getContext('2d');
            humChart = new Chart(humCtx, {
            type: 'line',
            data: { datasets: [{ label: 'Humidity', data: humidity, borderColor: 'rgba(54,162,235,1)', fill: false, pointRadius: 0 }] },
            options: commonOptions
        });
        } else {
            humChart.options.scales.x.max = now.getTime();
            humChart.data.datasets[0].data = humidity;
            humChart.update();
        }

        coGauge.set(latestCO);
        coGaugeText.textContent = `CO Gas Level: ${latestCO} ppm`;

    } catch (error) {
        console.error("Failed to fetch and update charts:", error);
}}

fetchTodayDataAndUpdateCharts();
setInterval(fetchTodayDataAndUpdateCharts, 1000);
