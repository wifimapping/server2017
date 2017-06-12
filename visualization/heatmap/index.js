function median(values) {
    values.sort((a, b) => a - b);
    return (values[(values.length - 1) >> 1] + values[values.length >> 1]) / 2
}

function max(values) {
    return values.sort((a, b) => a - b)[values.length - 1];
}

function mean(values) {
    return (values.reduce((a, b) => a + b, 0) / values.length);
}

function range(values) {
    values.sort((a, b) => a - b);
    return [values[10], values[values.length-10]];
}

var AGGREGATION = {
    median: median,
    max: max,
    mean: mean
};


angular
.module('Heatmap', ['WifiMapping'])
.controller('Ctrl', function($scope, wifiMappingAPI) {
    $scope.params = {
        aggregation: 'median',
        ssid: 'nyu'
    };

    var resultCache = {};

    var baseLayer = L.tileLayer(
      'http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 17
      }
    );

    /*var cfg = {
      "radius": .0001,
      "scaleRadius": true,
      "useLocalExtrema": false,

      latField: 'lat',
      lngField: 'lng',
      valueField: 'level',

      useGradientOpacity: false,
      blur: 0,
      opacity: .5
  };


    var heatmapLayer = new HeatmapOverlay(cfg);*/

    var heatmapLayer;

    var map = new L.Map('map', {
      center: new L.LatLng(40.7295134, -73.9964609),
      zoom: 14,
      maxZoom: 17,
      minZoom: 12,
      layers: [baseLayer]
    });

    /*var previousSSID = "";
    function display(groups) {
        var agg = [];

        var lats = [];
        var lngs = [];

        for (lat in groups) {
            lats.push(parseFloat(lat));
            for (lng in groups[lat]) {
                lngs.push(parseFloat(lng));
                agg.push({
                    lat: lat, lng: lng,
                    level: AGGREGATION[$scope.params.aggregation](groups[lat][lng])
                });

            }
        }

        var data = {
          max: -50,
          min: -90,
          data: agg
        };

        console.log(agg.length);

        heatmapLayer.setData(data);

        //Adjust map when SSID changes
        //map.panTo(new L.LatLng(mean(lats), mean(lngs)));
        if (previousSSID != $scope.params.ssid) {
            latRange = range(lats);
            lngRange = range(lngs);
            map.fitBounds([
                [latRange[1], lngRange[1]],
                [latRange[0], lngRange[0]]
            ]);
        }

        previousSSID = $scope.params.ssid;
    }*/

    /*map.on('zoomstart', function() {
        window.stop();
    });*/

    $scope.execute = function() {
        if (heatmapLayer) {
            map.removeLayer(heatmapLayer);
        } else {
            /*map.on('zoomend', function() {
                $scope.execute();
            });*/
        }

        heatmapLayer = L.tileLayer(
          'http://{s}.maps.wifindproject.com/wifipulling/tile/{z}/{x}/{y}/?ssid={ssid}&agg_function={agg_function}', {
            ssid: $scope.params.ssid,
            agg_function: $scope.params.aggregation,
            maxZoom: 18,
            opacity: .5
          }
        );

        map.addLayer(heatmapLayer);

        /*map.on('zoomend', function() {
            $scope.execute();
        });*/

        /*var params = {
            ssid: $scope.params.ssid, //page_size: 5000,
            columns: ['level', 'lat', 'lng']
        };

        var paramsString = JSON.stringify(params);

        if (resultCache[paramsString]) {
            display(resultCache[paramsString]);
        } else {
            wifiMappingAPI.query(params).then(function(res) {
                console.log(res.length);
                var groups = {};

                var lat, lng;
                for (var i = 0; i < res.length; i++) {
                    lat = res[i].lat.toFixed(4);
                    lng = res[i].lng.toFixed(4);

                    if (!groups[lat]) {
                        groups[lat] = {};
                    }

                    if (!groups[lat][lng]) {
                        groups[lat][lng] = [];
                    }

                    groups[lat][lng].push(res[i].level);
                }

                resultCache[paramsString] = groups;

                display(groups);
            });
        }*/
    };
});
