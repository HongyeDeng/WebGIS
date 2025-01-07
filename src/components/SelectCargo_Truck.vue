<template>
    <div class="container">
        <a-button type="primary" @click="HandleConfirm">Confirm</a-button>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps, watch } from "vue";
import L from "leaflet";
import $ from "jquery";
import { storeToRefs } from "pinia";
import { Truck_SelectCargo } from "@/stores/Status.js";

import CargoesLogo from "@/image/Normal.png";
import FrozenLogo from "@/image/frozen.png";
import OverweightLogo from "@/image/Overweight.png";
import HazardousLogo from "@/image/Hazardous.png";
import { Select } from "ant-design-vue";
var NormalCargoesIcon = L.icon({
    iconUrl: CargoesLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});
var FrozenCargoesIcon = L.icon({
    iconUrl: FrozenLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});
var OverweightCargoesIcon = L.icon({
    iconUrl: OverweightLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});
var HazardousCargoesIcon = L.icon({
    iconUrl: HazardousLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});

const Props = defineProps({
    map: Object,
    SelectedMarker: Object,
});

const Truck_SelectCargoMode = Truck_SelectCargo();
const { status: SelectCargo } = storeToRefs(Truck_SelectCargoMode);

var RouteOriginStyle = {
    color: "blue",
    weight: 3,
    opacity: 0.8,
};
const CargoRouteLayer = ref(null);

// handle the selected marker
const SelectedCargoID = ref(null);
const SelectedTruckID = ref(null);
const SelectedCargoRoute = ref(null);
let SelectedCargoMarker;

// Initial Routing machine
const Routing = ref(null);
const waypoints = ref([]);
const coords = ref([]);
Routing.value = L.Routing.control({
    waypoints: waypoints.value,
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim(),
    showAlternatives: false,
});
Routing.value.on("routesfound", function (e) {
    coords.value = e.routes[0].coordinates;
    console.log("Route Found");
});

// handle the selected marker(Truck)
watch(
    () => Props.SelectedMarker,
    (NewSelectedMarker) => {
        if (NewSelectedMarker && NewSelectedMarker.options.MarkerType) {
            if (NewSelectedMarker.options.MarkerType.includes("Truck")) {
                SelectedTruckID.value = NewSelectedMarker.options.ID;
                waypoints.value[0] = NewSelectedMarker.getLatLng();
            }
        }
    }
);

watch(
    [SelectedCargoID, SelectedTruckID],
    ([newCargoID, newTruckID], [oldCargo, oldTruck]) => {
        if (newCargoID && newTruckID && SelectCargo.value) {
            console.log("Selected Cargo:", newCargoID);
            console.log("Selected Truck:", newTruckID);
            Routing.value.setWaypoints(waypoints.value);
            Routing.value.addTo(Props.map);
        }
    }
);

watch(SelectCargo, async (NewValue) => {
    if (NewValue) {
        console.log("SelectCargo", NewValue);
        loadWFS("pgLayer:cargo", "EPSG:3857");
    } else {
        if (
            CargoRouteLayer.value &&
            Props.map.hasLayer(CargoRouteLayer.value)
        ) {
            Props.map.removeLayer(CargoRouteLayer.value);
            if (Routing.value) {
                Routing.value.remove();
            }
        }
    }
});
function loadWFS(layerName, epsg) {
    var urlString = "http://localhost:8083/geoserver/pgLayer/ows";
    var param = {
        service: "WFS",
        version: "1.0.0", // Use 1.0.0 to match your URL
        request: "GetFeature",
        typeName: layerName, // 'pgLayer:cargo' in your case
        outputFormat: "application/json",
        maxFeatures: 50, // Limit to 50 features
        srsName: epsg, // You still need to provide the EPSG code
    };
    var u = urlString + L.Util.getParamString(param, urlString);
    console.log(u);
    $.ajax({
        url: u,
        dataType: "json",
        success: loadWfsHandler,
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error loading WFS data:", textStatus, errorThrown);
            // Handle the error appropriately
        },
    });
    function loadWfsHandler(data) {
        console.log("Load cargo data", data);
        CargoRouteLayer.value = L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                // Create a custom icon for the point markers
                if (feature.properties.cargotype == "Normal") {
                    layer.setIcon(NormalCargoesIcon);
                } else if (feature.properties.cargotype == "Frozen") {
                    layer.setIcon(FrozenCargoesIcon);
                } else if (feature.properties.cargotype == "Overweight") {
                    layer.setIcon(OverweightCargoesIcon);
                } else if (feature.properties.cargotype == "Hazardous") {
                    layer.setIcon(HazardousCargoesIcon);
                }
                layer.setOpacity(0.5);
                // Bind a popup to the marker
                layer.bindPopup("Cargo ID: " + feature.id);

                // handle the mouseover/out events
                layer.on("mouseover", function (e) {
                    let GetIcon = e.target.options.icon;
                    GetIcon.options.iconSize = [50, 50];
                    GetIcon.options.iconAnchor = [25, 25];
                    layer.setIcon(GetIcon);
                });
                layer.on("mouseover", function (e) {
                    SelectedCargoRoute.value = L.geoJSON(
                        {
                            type: "Feature",
                            geometry: layer.feature.properties.cargo_route, // Pass the LineString geometry here
                            properties: {}, // Optionally add properties if needed
                        },
                        {
                            style: {
                                color: "blue", // Line color
                                weight: 3, // Line weight
                                opacity: 0.6, // Line opacity
                            },
                        }
                    );
                    SelectedCargoRoute.value.addTo(Props.map);
                });
                layer.on("mouseout", function (e) {
                    let GetIcon = e.target.options.icon;
                    GetIcon.options.iconSize = [30, 30];
                    GetIcon.options.iconAnchor = [15, 15];
                    layer.setIcon(GetIcon);

                    if (Props.map.hasLayer(SelectedCargoRoute.value)) {
                        Props.map.removeLayer(SelectedCargoRoute.value);
                    }
                });

                layer.on("click", function (e) {
                    const coordinates = layer.getLatLng(); // Get LatLng object
                    waypoints.value[1] = coordinates;
                    const CargoID = layer.feature.id;
                    SelectedCargoID.value = CargoID.split(".")[1];
                });
            },
        });

        Props.map.addLayer(CargoRouteLayer.value);
    }
}

const HandleConfirm = async () => {
    const wktCoords = coords.value
        .map((coord) => `${coord.lng} ${coord.lat}`)
        .join(",");
    const wktLineString = `LINESTRING(${wktCoords})`;
    try {
        const response = await fetch("http://127.0.0.1:5000/truck-add-route", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                TruckID: SelectedTruckID.value,
                CargoID: SelectedCargoID.value,
                polyline: wktLineString,
            }), // Send the input value
        });

        const result = await response.json();
        if (response.ok) {
            console.log(result.message); // Handle successful insertion
        } else {
            console.error(result.error); // Handle errors
        }
    } catch (error) {
        console.error("Error:", error);
    }
};
</script>

<style scoped>
.container {
    width: 200px;
    height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
</style>
