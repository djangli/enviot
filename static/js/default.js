var lat = 40.5853;
var lon = -105.0844;
var siteLayer;
var interpolationLayer;

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([lon, lat]),
        zoom: 9
    })
});

addSiteLayerToMap();


function createInterpolationMap() {
    $.ajax('/interpolate-map/').done(function (result) {
        $('#result-link').remove();
        $('#result').html(result);
    });
}


function publishWebMapService() {
    $.ajax('/publish-wms/').done(function (service_layer){
        alert('WMS publishing success!');
    }).fail(function (){
        alert('WMS publishing failed!!!')
    });
}


function addInterpolationLayerToMap() {

    if (interpolationLayer) {
        map.removeLayer(interpolationLayer);
    }

    $.ajax('/show-map/').done(function (service_layer) {     
        console.log(service_layer);
        var remote_endpoint = 'http://ec2-18-232-162-21.compute-1.amazonaws.com:8080/geoserver/wms';
        var local_endpoint = 'https://localhost:8080/geoserver/wms';
        interpolationLayer = new ol.layer.Image({
            source: new ol.source.ImageWMS({
                url: remote_endpoint,
                params: {'LAYERS': service_layer},
                ratio: 1,
                serverType: 'geoserver'
            }),
            opacity: 0.5
        });
        
        map.addLayer(interpolationLayer);
    });
};

function addSiteLayerToMap() {
    $.ajax({url: "api/site-list/"}).done(function (sites){
        // point feature
        var markers = [];
        for (i = 0; i < sites.length; i++) {
            // parse site information
            var site = sites[i];
            var sensor = site['sensors'][0];
            var parameter = sensor['parameters'][0];
            var value = parameter['value'];
            // create site marker with ol
            var marker = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([site.lon, site.lat]))
            })
            marker.setStyle(new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 10,
                    fill: new ol.style.Fill({color: 'rgba(255, 0, 0, 0.1)'}),
                    stroke: new ol.style.Stroke({color: 'red', width: 1})
                }),
                text: new ol.style.Text({
                    text: value.toString()
                })
            }));
            markers.push(marker);
        }
        
        if (siteLayer) {
            map.removeLayer(siteLayer);
        }

        // vector layer
        siteLayer = new ol.layer.Vector({
            source: new ol.source.Vector({features: markers})
        });
        
        map.addLayer(siteLayer); 
    });
}
