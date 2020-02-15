var monthMapper = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
};

var nightOutMapper = {
    1: "Sun-Mon",
    2: "Mon-Tue",
    3: "Tue-Wed",
    4: "Wed-Thu",
    5: "Thu-Fri",
    6: "Fri-Sat",
    7: "Sat-Sun"
};

var years = ["2009", "2010", "2011", "2012", "2013", "2014", "2015"]
var color_scheme = ["#2f4b7c", "#665191", "#a05195", "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]

default_zoom = 10
nyc_coordinates = [-73.9978, 40.7209]

function readJSONFile(file) {
    var allText;
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function (){
        if(rawFile.readyState === 4){
            if(rawFile.status === 200 || rawFile.status == 0){
                allText = rawFile.responseText;
            }
        }
    }
    rawFile.send(null);
    return(JSON.parse(allText))
} 

mapboxgl.accessToken = "pk.eyJ1Ijoic2pyYWFpam1ha2VycyIsImEiOiJjazB6bjBicjAwMnRuM25ucXY1NDJvaTFtIn0.Q-2s7YaT3lgXaOVis85M4Q";

// Initialize map
var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/dark-v10",
    zoom: default_zoom,
    center: nyc_coordinates
});

// Function to change source of layer
function setLayerSource (layerId, source, sourceLayer) {
    const oldLayers = map.getStyle().layers;
    const layerIndex = oldLayers.findIndex(l => l.id === layerId);
    const layerDef = oldLayers[layerIndex];
    const before = oldLayers[layerIndex + 1] && oldLayers[layerIndex + 1].id;
    layerDef.source = source;
    if (sourceLayer) {
        layerDef['source-layer'] = sourceLayer;
    }
    map.removeLayer(layerId);
    map.addLayer(layerDef, before);
}

map.on("load", function() {  
    // Add geocoder (search function) 
    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        zoom: 15,
        placeholder: "Search for geohash...",
        localGeocoder: forwardGeocoder,
        localGeocoderOnly: true,
        mapboxgl: mapboxgl
    });

    // On init
    var e = document.getElementById("year");
    var currentYear = e.options[e.selectedIndex].value;
    updateTop(5)

    // Get top n of current year and write to top_html
    function updateTop(n){
        var trip_data = readJSONFile("data/trips/night-hot-spots-" + currentYear + ".geojson");
        var top = (trip_data.features).sort(function (a, b) {
            return b.properties.score - a.properties.score;
        }).slice(0, n);
    
        html_string = "<ol>"

        top.forEach(function(value) {
            html_string = html_string.concat("<li class='list-group-item'>" + value.properties.geoHash + "<br />(" + value.properties.score + ")</li>")
        })

        html_string = html_string.concat("</ol>")
        document.getElementById("top_html").innerHTML = html_string;
    }  

    // Forward geocoder for local data of current year  
    function forwardGeocoder(query) {
        var trip_data = readJSONFile("data/trips/night-hot-spots-" + currentYear + ".geojson");
        var matchingFeatures = [];
        for (var i = 0; i < trip_data.features.length; i++) {
            var feature = trip_data.features[i];
            if (feature.properties.geoHash.toLowerCase().search(query.toLowerCase()) !== -1) {
                feature['place_name'] = feature.properties.geoHash;
                feature['center'] = feature.geometry.coordinates;
                matchingFeatures.push(feature);
            }
        }
        return matchingFeatures;
    }

    // For each year, create layer according to data/
    years.forEach(function(value) {
        map.addSource("trips" + value, {
            type: "geojson",
            data: "data/trips/night-hot-spots-" + value + ".geojson"
        });
    });
        
    map.addSource("boroughs", {
        type: "geojson",
        data: "data/borough_boundaries.geojson"
    })

    // Bars data: https://www.kaggle.com/somesnm/heatmap-of-pubs-and-bars-of-new-york-city
    map.addSource("bars", {
        type: "geojson",
        data: "data/nyc_bars.geojson"
    });    
    
    // Heatmap, density based on "score"
    map.addLayer({
        "id": "heatmap",
        "type": "heatmap",
        "source": "trips" + currentYear,
        "paint": {
            "heatmap-weight": [
                "interpolate",
                ["linear"],
                ["get", "score"],
                0, 0,
                10, 1
            ],
            "heatmap-intensity": [
                "interpolate",
                ["linear"],
                ["zoom"],
                0, 1,
                9, 3
            ],
            "heatmap-color": [
                "interpolate",
                ["linear"],
                ["heatmap-density"],
                0, "rgba(33,102,172,0)",
                0.2, "rgb(103,169,207)",
                0.4, "rgb(209,229,240)",
                0.6, "rgb(253,219,199)",
                0.8, "rgb(239,138,98)",
                1, "rgb(178,24,43)"
            ],
            "heatmap-radius": [
                "interpolate",
                ["linear"],
                ["zoom"],
                0, 2,
                9, 20
            ],
            "heatmap-opacity": [
                "interpolate",
                ["linear"],
                ["zoom"],
                10, 1,
                18, 0
            ],
        }
    });

    // Bars, visualized by "glass"
    map.loadImage("bar_icon.png", function(error, image) {
        if (error) throw error;
        map.addImage("bar", image);
        map.addLayer({
            id: "bars",
            type: "symbol",
            source: "bars",
            layout: {
                "icon-image": "bar",
                "icon-size": 0.05
            },
            minzoom: 12
        });
    })

    // Trips circles layer
    map.addLayer({
        id: "trips",
        type: "circle",
        source: "trips" + currentYear,
        minzoom: 14,
        paint: {
            "circle-radius":
            [
                "interpolate",
                ["linear"],
                ["number", ["get", "score"]],
                0, 1,
                10, 20
            ],
            "circle-color":
            [
                "interpolate",
                ["linear"],
                ["number", ["get", "score"]],
                0, "#2DC4B2",
                2, "#3BB3C3",
                4, "#669EC4",
                6, "#8B88B6",
                8, "#A2719B",
                10, "#AA5E79"
            ]
        }
    });

    // Borough layer
    map.addLayer({
        id: "boroughs",
        type: "fill",
        source: "boroughs",
        paint: {
            'fill-opacity': 0.1,
            'fill-color': [
                'match',
                ['get', 'boro_name'],
                'Bronx', '#e41a1c',
                'Staten Island', '#984ea3',
                'Brooklyn', '#ffff33',
                'Queens', '#ff7f00',
                'Manhattan', '#4daf4a',
                /* other */ '#ccc']
        }
    })

    // Create 2d lineplot for plot_data
    function linePlot2D(eid, plot_labels, plot_data, title){
        var yearsArray = []

        plot_data.forEach(function(value, index) {
            var tmpYear = {
                label: years[index],
                borderColor: color_scheme[index],
                backgroundColor: color_scheme[index],
                data: value,
                fill: false
            }
            yearsArray.push(tmpYear)
        });

        var chart = new Chart(eid, {
            type: 'line',
            data: {
                labels: plot_labels,
                datasets: yearsArray
            },
            options: {
                title: {
                    display: true,
                    text: title
                }
            },
        })
        return chart
    }

    // Create barplot (1d) for plot_data
    function barPlot(eid, plot_labels, plot_data, title){
        var chart = new Chart(eid, {
            type: 'bar',
            data: {
                labels: plot_labels,
                datasets: [{
                    label: 'Number of night trips',
                    backgroundColor: color_scheme,
                    data: plot_data
                }]
            },
            options: {
                legend: {
                    display: false,
                },
                title: {
                    display: true,
                    text: title
                }
            },
        })
        return chart
    }

    // On click of cluster point
    map.on("click", "trips", function (e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var score = e.features[0].properties.score;

        var geohash =  e.features[0].properties.geoHash

        var hourStats = JSON.parse(e.features[0].properties.hourStats);
        var nightOfWeekStats = JSON.parse(e.features[0].properties.nightOfWeekStats);
        var monthStats = JSON.parse(e.features[0].properties.monthStats);
        var yearStats = JSON.parse(e.features[0].properties.yearStats);

        var numberOfNightTrips =  e.features[0].properties.numberOfNightTrips
        var numberOfDayTrips =  e.features[0].properties.numberOfDayTrips
        var nightLifeLocations =  e.features[0].properties.nightLifeLocationsInNeighbourhood

        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Create info table
        var infoStats = '\
                <table class="table"> \
                    <tbody> \
                        <tr> \
                            <td>Coordinates</td> \
                            <td>' + coordinates + ' (' + geohash + ')</td> \
                        </tr> \
                    <tr> \
                    <td>Number of night trips (clustersize):</td> \
                    <td>' + numberOfNightTrips + '</td> \
                        </tr> \
                    <tr> \
                        <td>Number of day trips:</td> \
                        <td>' + numberOfDayTrips + '</td> \
                        </tr> \
                    <tr> \
                    <td>Night life locations nearby (< 50 meter):</td> \
                    <td>' + nightLifeLocations + '</td> \
                        </tr> \
                    <tr> \
                        <td>Score in ' + currentYear + '</td> \
                        <td>' + score + '</td> \
                    </tr> \
                    <tr> \
                        <td>Google Maps</td> \
                        <td><a href="https://www.google.com/maps/place/' + coordinates[1] + ',' + coordinates[0] + '" target="blank">Link</a></td> \
                    </tr> \
                    </tbody> \
                </table> '

        // Popup body (contain infoStats)        
        var body =' \
                <ul class="nav nav-pills mb-3" id="pills-tab" role="tablist"> \
                    <li class="nav-item"> \
                        <a class="nav-link active" id="pills-info-tab" data-toggle="pill" href="#pills-info" role="tab" aria-controls="pills-info" aria-selected="true">Info</a> \
                    </li> \
                    <li class="nav-item"> \
                        <a class="nav-link" id="pills-hour-tab" data-toggle="pill" href="#pills-hour" role="tab" aria-controls="pills-hour" aria-selected="false">Hour timeseries</a> \
                    </li> \
                    <li class="nav-item"> \
                        <a class="nav-link" id="pills-day-tab" data-toggle="pill" href="#pills-day" role="tab" aria-controls="pills-day" aria-selected="false">Nightout timeseries</a> \
                    </li> \
                    <li class="nav-item"> \
                        <a class="nav-link" id="pills-month-tab" data-toggle="pill" href="#pills-month" role="tab" aria-controls="pills-month" aria-selected="false">Monthly timeseries</a> \
                    </li> \
                    <li class="nav-item"> \
                        <a class="nav-link" id="pills-year-tab" data-toggle="pill" href="#pills-year" role="tab" aria-controls="pills-year" aria-selected="false">Yearly timeseries</a> \
                    </li> \
                </ul> \
                <div class="tab-content" id="pills-tabContent"> \
                    <div class="tab-pane fade show active" id="pills-info" role="tabpanel" aria-labelledby="pills-info-tab">' + infoStats + '</div> \
                    <div class="tab-pane fade" id="pills-hour" role="tabpanel" aria-labelledby="pills-hour-tab"><canvas id="hour_graph-' + geohash + '"></canvas></div> \
                    <div class="tab-pane fade" id="pills-day" role="tabpanel" aria-labelledby="pills-day-tab"><canvas id="day_graph-' + geohash + '"></canvas></div> \
                    <div class="tab-pane fade" id="pills-month" role="tabpanel" aria-labelledby="pills-month-tab"><canvas id="month_graph-' + geohash + '"></canvas></div> \
                    <div class="tab-pane fade" id="pills-year" role="tabpanel" aria-labelledby="pills-year-tab"><canvas id="year_graph-' + geohash + '"></canvas></div> \
                </div>'

        // Create popup
        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(body)
            .addTo(map);
        map.flyTo({center: e.features[0].geometry.coordinates, zoom: 18});

        var hourToString = hourStats["2009"].hour.slice(0, 8).map(function (e){
            return e + ":00"
        });

        var nightOutToString = nightOfWeekStats["2009"].nightOfWeek.slice(0, 7).map(function (e){
            return nightOutMapper[e];
        });

        var monthToString = [1,2,3,4,5,6,7,8,9,10,11,12].map(function (e){
            return monthMapper[e]
        });

        // Transform geojson data to valid chart.js format
        var hourTimeseries = []
        var NOTimeseries = []
        var monthTimeseries = []

        years.forEach(function(value) {
            hourTimeseries.push(hourStats[value].numberOfTrips);
            NOTimeseries.push(nightOfWeekStats[value].numberOfTrips);
            monthTimeseries.push(monthStats[value].numberOfTrips);
        })

        // Visualize plots (add to corresponding element)
        var hour_graph = document.getElementById('hour_graph-' + geohash).getContext('2d');
        linePlot2D(hour_graph, hourToString, hourTimeseries, "Number of trips per hour (" + geohash + ")");

        var day_graph = document.getElementById('day_graph-' + geohash).getContext('2d');
        linePlot2D(day_graph, nightOutToString, NOTimeseries, "Number of trips per night out (" + geohash + ")");

        var month_graph = document.getElementById('month_graph-' + geohash).getContext('2d');
        linePlot2D(month_graph, monthToString, monthTimeseries, "Number of trips per month (" + geohash + ")");

        var year_graph = document.getElementById('year_graph-' + geohash).getContext('2d');
        barPlot(year_graph, yearStats.year, yearStats.numberOfTrips, "Number of trips per year (" + geohash + ")");
    });

    // Pointer styles
    map.on("mouseenter", "trips", function () {
        map.getCanvas().style.cursor = "pointer";
    });

    map.on("mouseleave", "trips", function () {
        map.getCanvas().style.cursor = "";
    });

    // Add geocoder to #search_map
    document.getElementById("search_map").appendChild(geocoder.onAdd(map));

    // Reset view to original zoom
    document.getElementById("reset_view").addEventListener("click", function(e) {
        map.flyTo({center: nyc_coordinates, zoom: default_zoom});
    });

    // Year filter
    document.getElementById("year").addEventListener("click", function(e) {
        currentYear = parseInt(e.target.value);
        setLayerSource("trips", "trips" + currentYear)
        setLayerSource("heatmap", "trips" + currentYear)
        updateTop(5)
    });    
});


