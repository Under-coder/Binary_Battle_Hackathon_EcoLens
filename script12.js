let map, marker, myChart;

document.addEventListener("DOMContentLoaded", function() {
    initMap();
    setupEventListeners();
    createGraph();
    // Initial load with default city
    analyzeLocation();
});

function initMap() {
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

    map = L.map("map", {
        center: [23.2599, 77.4126], // Default to Bhopal
        zoom: 11,
        layers: [satelliteLayer]
    });

    L.control.layers({
        "Satellite": satelliteLayer,
        "Street": streetLayer
    }).addTo(map);
}

function setupEventListeners() {
    document.getElementById("analyzeBtn").addEventListener("click", analyzeLocation);
    document.getElementById("cityInput").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            analyzeLocation();
        }
    });
}

async function analyzeLocation() {
    const cityInput = document.getElementById("cityInput").value.trim();
    const city = cityInput || "Bhopal"; // Default to Bhopal if empty

    try {
        const response = await fetch(`http://127.0.0.1:8000/ecosystem-analysis?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        updateDashboard(data);
        updateMap(data.coordinates.latitude, data.coordinates.longitude);
        updateGraph(data);
    } catch (error) {
        console.error("API call failed:", error);
        alert("Failed to fetch data. Ensure backend is running.");
    }
}

function updateMap(lat, lng) {
    const coords = [lat, lng];
    map.flyTo(coords, 12);

    if (marker) {
        map.removeLayer(marker);
    }

    marker = L.marker(coords).addTo(map);
}

function updateDashboard(data) {
    document.getElementById("Cover").textContent = `${(data.ndvi_analysis.average_ndvi * 100).toFixed(1)}%`;
    document.getElementById("Loss").textContent = `${(data.ndvi_analysis.ndvi_change * 100).toFixed(1)}%`;
    document.getElementById("cause").textContent = data.predicted_cause;
    document.getElementById("time").textContent = data.recovery_estimate;

    // Update chart stats
    document.getElementById("chartCurrent").textContent = `${(data.ndvi_analysis.average_ndvi * 100).toFixed(1)}%`;
    document.getElementById("chartLoss").textContent = `${(data.ndvi_analysis.ndvi_change * 100).toFixed(1)}%`;
}

function createGraph() {
    const ctx = document.getElementById("vegetationChart").getContext("2d");
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Current NDVI (%)', 'NDVI Change (%)'],
            datasets: [{
                label: 'Vegetation Index',
                data: [0, 0],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function updateGraph(data) {
    if (myChart) {
        myChart.data.datasets[0].data = [data.ndvi_analysis.average_ndvi * 100, data.ndvi_analysis.ndvi_change * 100];
        myChart.update();
    }
}