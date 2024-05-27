/*
 * Mapa da desgraça
*/

const mapa = 'mapa';
const porto_alegre_lat = -30.0417169;
const porto_alegre_lng = -51.2211564;
const londres_lat = 51.3026
const londres_lng = -0.739
const tile_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
const tile_attribution = 'Dados de mapas &copy; contribuidora(e)s do <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, ' +
    '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    //~ 'Imagery © <a href="https://thunderforest.com/">Thunderforest</a>, ' +
    //~ 'Dados climáticos obtidos através do <a href="https://notabug.org/velivery/climobike">ClimoBike</a>. ' +
    //~ 'Powered com <a href="http://souvegetariano.com">&hearts;</a> e <a href="https://notabug.org/velivery/velivery_maps">liberdade</a> by <a href="http://velivery.com.br">Velivery</a>';
    ''
;

let map = L.map(mapa).setView([porto_alegre_lat, porto_alegre_lng], 13);
//~ let map = L.map(mapa).setView([londres_lat, londres_lng], 13);

let osm = L.tileLayer(tile_url, {
    maxZoom: 19,
    attribution: tile_attribution
}).addTo(map);

let marcadores = L.layerGroup().addTo(map);

let marcador_1 = L.marker(
    [-30.0417169, -51.2211564],
)
.bindPopup("Marcador 1")
.addTo(marcadores);
let marcador_2 = L.marker(
    [-30.041834, -51.22133],
)
.bindPopup("Marcador 2")
.addTo(marcadores);
let marcador_3 = L.marker(
    [-30.039154, -51.219833],
)
.bindPopup("Marcador 3")
.addTo(marcadores);
let marcador_4 = L.marker(
    [-30.033181, -51.215236],
)
.bindPopup("Marcador 4")
.addTo(marcadores);

let areas = L.layerGroup().addTo(map);

//~ let area_1 = L.polygon([
        //~ [-30.033273, -51.240696],
        //~ [-30.030775, -51.238883],
        //~ [-30.019627, -51.216674],
        //~ [-30.017825, -51.197619],
        //~ [-30.022322, -51.195409],
        //~ [-30.028583, -51.19454],
        //~ [-30.040406, -51.194444],
        //~ [-30.048343, -51.196375],
        //~ [-30.052692, -51.204722],
        //~ [-30.060842, -51.219635],
        //~ [-30.059378, -51.230729],
        //~ [-30.04226, -51.236136],
        //~ [-30.041388, -51.241157],
        //~ [-30.041388, -51.241157]
    //~ ],
    //~ {
        //~ color: 'orange'
    //~ }
//~ )
//~ .addTo(areas)
//~ .bindPopup("Polígono de teste.");

let geos = L.layerGroup().addTo(map);

new L.GeoJSON(dados_teste,
    {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
                radius: 8,
                fillColor: "#8ae234",
                color: "#4e9a06",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            });
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup(
                '<h2>Dados de Teste</h2>'
                + '<ul>'
                + '<li>Vers&atilde;o: '
                + feature.properties.climobike
                + '</li>'
                + '<li>Data de aquisi&ccedil;&atilde;o: '
                + feature.properties.time
                + '</li>'
                + '<li>Coordenadas: '
                + feature.properties.lat
                + ', '
                + feature.properties.long
                + '</li>'
                + '<li>Mon&oacute;xido de carbono: '
                + feature.properties.CO
                + '</li>'
                + '<li>Gases t&oacute;xicos: '
                + feature.properties.NH3
                + '</li>'
                + '<li>Metano: '
                + feature.properties.CH4
                + '</li>'
                + '<li>Temperatura: '
                + feature.properties.temp
                + '</li>'
                + '<li>Umidade relativa do ar: '
                + feature.properties.hum
                + '</li>'
                + '<li>Luminosidade: '
                + feature.properties.ldr
                + '</li>'
                + '</ul>'
            );
        }
    }
)
.addTo(geos);

var baseLayers = {
        "OpenStreetMap": osm
};

var overlays = {
        "Geolocalizações": geos,
        "Marcadores": marcadores,
        "Áreas": areas
};

var controle = L.control.layers(baseLayers, overlays).addTo(map);

var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("Posição: " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);
