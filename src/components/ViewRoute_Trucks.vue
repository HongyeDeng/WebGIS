<template>
    <div class="container">
        <div class="disabled-section">
            <a-select
                v-model:value="CargoTypeFilter"
                mode="tags"
                style="width: 200px"
                placeholder="Tags Mode"
                :options="CargoTypeoptions"
                @change="handleChange"
            ></a-select>
        </div>
        <div class="disabled-section">
            <a-button type="primary" @click="DoFilter">Confirm</a-button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps, watch, createApp } from "vue";
import { Truck_ViewRouteStatus } from "@/stores/Status.js";
import CargoRoutePopup from "@/components/InfoForm_CargoRoute.vue";
import DestinationLogo from "@/image/destination.png";
import { storeToRefs } from "pinia";
import L, { map } from "leaflet";
import "leaflet.markercluster";
import "leaflet-routing-machine";
import Antd from "ant-design-vue";
import $ from "jquery";

// RouteLayer
const Truck_RouteLayer = ref(null);
const Cargo_RouteLayer = ref(null);
const Truck_Route_Style = {
    color: "green",
    weight: 5,
    opacity: 0.2,
};
const Cargo_Route_Style = {
    color: "blue",
    weight: 5,
    opacity: 0.2,
};
const Truck_Route_Style_HighLight = {
    color: "green",
    weight: 5,
    opacity: 0.8,
};
const Cargo_Route_Style_HighLight = {
    color: "blue",
    weight: 5,
    opacity: 0.8,
};

// Destination Icon
var DestinationIcon = L.icon({
    iconUrl: DestinationLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});
const DestinationMarkerGroutp = ref(L.markerClusterGroup());

// Canvas renderer to draw the route
const canvasRenderer = L.canvas({
    tolerance: 2,
});

// Set the CargoType Filter
const CargoTypeFilter = ref([]);
const CargoTypeoptions = ref([]);
CargoTypeoptions.value = [
    { label: "Normal", value: "Normal" },
    { label: "Overweight", value: "Overweight" },
    { label: "Hazardous", value: "Hazardous" },
    { label: "Frozen", value: "Frozen" },
];

const Props = defineProps({
    map: Object,
    SelectedMarker: Object,
});

const ViewRouteMode = Truck_ViewRouteStatus();
const { status: ViewRoute } = storeToRefs(ViewRouteMode);

watch(ViewRoute, async (val) => {
    console.log("ViewRoute", val);
    if (val) {
        loadWFS_Route("pgLayer:truck_route", "EPSG:3857", Truck_RouteLayer);
        loadWFS_Route("pgLayer:cargo_route", "EPSG:3857", Cargo_RouteLayer);
    } else {
        if (
            Truck_RouteLayer.value &&
            Props.map.hasLayer(Truck_RouteLayer.value)
        ) {
            Props.map.removeLayer(Truck_RouteLayer.value);
        }
        if (
            Cargo_RouteLayer.value &&
            Props.map.hasLayer(Cargo_RouteLayer.value)
        ) {
            Props.map.removeLayer(Cargo_RouteLayer.value);
        }

        if (DestinationMarkerGroutp.value && Props.map.hasLayer(DestinationMarkerGroutp.value)) {
            Props.map.removeLayer(DestinationMarkerGroutp.value);
        }
    }
});

const DoFilter = () => {
    console.log("Filter:", CargoTypeFilter.value);
    if (Props.map) {
        Cargo_RouteLayer.value.eachLayer(function (layer) {
            if (layer.feature) {
                if (CargoTypeFilter.value.includes(layer.feature.properties.cargotype && layer.feature.properties.associated_truck_id != null)) {
                    layer.setStyle({ opacity: 0.2 });
                } else {
                    layer.setStyle({ opacity: 0 });
                }
            }
        });
        Truck_RouteLayer.value.eachLayer(function (layer) {
            if (layer.feature) {
                if (CargoTypeFilter.value.includes(layer.feature.properties.trucktype) && layer.feature.properties.cargo_id != null) {
                    layer.setStyle({ opacity: 0.2 });
                } else {
                    layer.setStyle({ opacity: 0 });
                }
            }
        });
        if (CargoTypeFilter.value.length == 0) {
            Cargo_RouteLayer.value.eachLayer(function (layer) {
                layer.setStyle({ opacity: 0.2 });
            });
            Truck_RouteLayer.value.eachLayer(function (layer) {
                layer.setStyle({ opacity: 0.2 });
            });
        }
    }
};

function loadWFS_Route(layerName, epsg, TargetLayer) {
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
        console.log("Load route data", data);
        TargetLayer.value = L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                // Bind a popup to the marker
                layer.bindPopup("CargoName: " + feature.properties.cargoname);

                // Set the style of the route
                if (layerName.includes("truck")) {
                    layer.setStyle(Truck_Route_Style);
                    layer.on("mouseover", function (e) {
                        layer.setStyle(Truck_Route_Style_HighLight);
                    });
                    layer.on("mouseout", function (e) {
                        layer.setStyle(Truck_Route_Style);
                    });
                } else if (layerName.includes("cargo")) {
                    layer.setStyle(Cargo_Route_Style);
                    layer.on("mouseover", function (e) {
                        layer.setStyle(Cargo_Route_Style_HighLight);
                    });
                    layer.on("mouseout", function (e) {
                        layer.setStyle(Cargo_Route_Style);
                    });
                }

                if (layerName.includes("cargo")) {
                    if (feature.properties.associated_truck_id == null) {
                        layer.setStyle({ opacity: 0 });
                    }
                }

                if (layerName.includes("truck")) {
                    const LastPoint = feature.geometry.coordinates[feature.geometry.coordinates.length - 1];    
                    const marker = L.marker(L.GeoJSON.coordsToLatLng(LastPoint), {
                        icon: DestinationIcon,
                    });
                    DestinationMarkerGroutp.value.addLayer(marker);
                }
            },
        });

        Props.map.addLayer(TargetLayer.value);
        Props.map.addLayer(DestinationMarkerGroutp.value);
    }
}
</script>

<style scoped>
.container {
    width: 250px;
    height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 30px;
}

.disabled-section {
    display: flex;
    align-items: center;
    margin-bottom: 10px; /* Adjust the space between text and switch */
    line-height: 30px;
}
</style>
