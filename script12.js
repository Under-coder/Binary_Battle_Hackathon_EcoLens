let map, marker, myChart;

const cityData = {
mumbai:{lat:19.0760,lng:72.8777,cover:'18% (9,253 Ha)',loss:'65% (17,479 Ha)',cause:'Urban Growth',time:'5-6 Years',current:18,peak:65},
bhopal:{lat:23.2599,lng:77.4126,cover:'15% (7,950 Ha)',loss:'76% (27,050 Ha)',cause:'Urban Expansion',time:'5-7 Years',current:15,peak:76},
delhi:{lat:28.6139,lng:77.2090,cover:'21% (13,000 Ha)',loss:'49% (12,400 Ha)',cause:'Urbanization',time:'4-6 Years',current:21,peak:49},
bangalore:{lat:12.9716,lng:77.5946,cover:'12% (8,500 Ha)',loss:'82% (35,200 Ha)',cause:'Tech Growth',time:'6-8 Years',current:12,peak:82},
chennai:{lat:13.0827,lng:80.2707,cover:'14% (6,800 Ha)',loss:'71% (22,100 Ha)',cause:'Industrial',time:'5-7 Years',current:14,peak:71}
};

let currentData = cityData["mumbai"];

document.addEventListener("DOMContentLoaded",function(){

initMap();
setupEventListeners();
createGraph();
analyzeLocation();

});

function initMap(){

const satelliteLayer=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
const streetLayer=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

map=L.map("map",{
center:[19.0760,72.8777],
zoom:11,
layers:[satelliteLayer]
});

L.control.layers({
"Satellite":satelliteLayer,
"Street":streetLayer
}).addTo(map);

}

function setupEventListeners(){

document.getElementById("analyzeBtn").addEventListener("click",analyzeLocation);

document.getElementById("cityInput").addEventListener("keypress",function(e){
if(e.key==="Enter"){
analyzeLocation();
}
});

}

function analyzeLocation(){

const input=document.getElementById("cityInput").value.toLowerCase().trim();

if(cityData[input]){
currentData=cityData[input];
}else{
currentData=cityData["mumbai"];
}

updateDashboard();
updateMap();
updateGraph();

}

function updateMap(){

const coords=[currentData.lat,currentData.lng];

map.flyTo(coords,12);

if(marker){
map.removeLayer(marker);
}

marker=L.marker(coords).addTo(map);

}

function updateDashboard(){

document.getElementById("Cover").textContent=currentData.cover;
document.getElementById("Loss").textContent=currentData.loss;
document.getElementById("cause").textContent=currentData.cause;
document.getElementById("time").textContent=currentData.time;

const chartCurrent=document.getElementById("chartCurrent");
const chartLoss=document.getElementById("chartLoss");

if(chartCurrent) chartCurrent.textContent=currentData.cover;
if(chartLoss) chartLoss.textContent=currentData.loss;

}

function createGraph(){

const ctx=document.getElementById("vegetationChart").getContext("2d");

myChart=new Chart(ctx,{
type:"bar",

data:{
labels:["2010","2012","2014","2016","2018","2020","2023"],

datasets:[
{
label:"Current Green Cover",
data:[55,50,45,35,28,20,currentData.current],
backgroundColor:"#10b981"
},

{
label:"Cover Green Area",
data:[60,55,50,40,30,25,currentData.current+5],
backgroundColor:"#22c55e"
},

{
label:"Loss Green Area",
data:[10,15,25,35,45,55,currentData.peak],
backgroundColor:"#ef4444"
}

]

},

options:{
responsive:true,
maintainAspectRatio:false,

plugins:{
legend:{
position:"top"
}
},

scales:{
y:{
beginAtZero:true,
max:100,
ticks:{
callback:function(value){
return value+"%";
}
}
}
}

}

});

}

function updateGraph(){

myChart.data.datasets[0].data=[55,50,45,35,28,20,currentData.current];
myChart.data.datasets[1].data=[60,55,50,40,30,25,currentData.current+5];
myChart.data.datasets[2].data=[10,15,25,35,45,55,currentData.peak];

myChart.update();

}