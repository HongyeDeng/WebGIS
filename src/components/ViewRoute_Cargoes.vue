<template>
    <div class="container">
        <div class="disabled-section">
            <p>Cargo Type</p>
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
            <p>Start Location</p>
            <a-select
                v-model:value="StartLocationFilter"
                mode="tags"
                style="width: 200px"
                placeholder="Tags Mode"
                :options="StartLocationoptions"
                @change="handleChange"
            ></a-select>
        </div>
        <div class="disabled-section">
            <p>End Location</p>
            <a-select
                v-model:value="EndLocationFilter"
                mode="tags"
                style="width: 200px"
                placeholder="Tags Mode"
                :options="EndLocationoptions"
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
import { Cargo_ViewRouteStatus } from "@/stores/Status.js";
import CargoRoutePopup from "@/components/InfoForm_CargoRoute.vue";
import DestinationLogo from "@/image/destination.png";
import { storeToRefs } from "pinia";
import L, { map } from "leaflet";
import "leaflet-routing-machine";
import Antd from "ant-design-vue";
import $ from "jquery";

const leafletPip = require("leaflet-pip");
// Class to store route information
class CargoRoute {
    constructor(cargo_id, cargotype, routeLayer, StartCountry, EndCountry) {
        this.cargo_id = cargo_id;
        this.cargotype = cargotype;
        this.routeLayer = routeLayer; // This is the L.geoJSON layer
        this.DestinationMarker;
        this.StartCountry = StartCountry;
        this.EndCountry = EndCountry;
    }
}
const CargoRouteStyle = {
    color: "blue",
    weight: 5,
    opacity: 0.2,
};
const CargoRouteStyle_Highlight = {
    color: "yellow",
    weight: 8,
    opacity: 0.8,
};

const EUPolygonStyle = {
    fillColor: "yellow", // Fill color of the polygon
    fillOpacity: 0.0, // Opacity of the fill (0.0 - 1.0)
    color: "red", // Stroke/border color
    weight: 0.1, // Stroke/border width in pixels
    opacity: 1, // Stroke/border opacity (0.0 - 1.0)
    dashArray: "1, 1",
};
const EU_PolygonLayer = ref(null);
loadWFS_Polygon("ne:countries", "EPSG:4326", EU_PolygonLayer);

// Destination Icon
var DestinationIcon = L.icon({
    iconUrl: DestinationLogo,

    iconSize: [30, 30], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});

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

// Set the StartLocation Filter
const StartLocationFilter = ref([]);
const StartLocationoptions = ref([]);
// Set the EndLocation Filter
const EndLocationFilter = ref([]);
const EndLocationoptions = ref([]);

const cargoRoutes = ref([]);

const Props = defineProps({
    map: Object,
    SelectedMarker: Object,
});

const ViewRouteMode = Cargo_ViewRouteStatus();
const { status: ViewRoute } = storeToRefs(ViewRouteMode);

watch(ViewRoute, async (val) => {
    console.log("ViewRoute", val);
    if (val) {
        // Load all cargo routes
        try {
            const response = await fetch(
                "http://127.0.0.1:5000/getallroutes-cargo",
                {
                    method: "GET",
                }
            );
            if (!response.ok) {
                throw new Error("Failed to fetch truck data");
            }
            const data = await response.json();
            for (const item of data.data) {
                var StartCountry = "", EndCountry = "";
                const geoJsonLayer = L.geoJSON(JSON.parse(item.route), {
                    onEachFeature: (feature, layer) => {
                        layer.cargo_id = item.cargo_id;
                        layer.cargotype = item.cargotype;

                        layer.on("click", () => {
                            console.log("Clicked Cargo ID:", layer.cargo_id);
                        });
                        layer.setStyle(CargoRouteStyle);

                        // Highlight the route when mouseover
                        layer.on("mouseover", function (e) {
                            this.setStyle(CargoRouteStyle_Highlight);
                        });
                        layer.on("mouseout", function (e) {
                            this.setStyle(CargoRouteStyle);
                        });

                        // query the route coordiantes
                        const StartPoint = feature.coordinates[0];
                        const EndPoint =
                            feature.coordinates[feature.coordinates.length - 1];
                        StartCountry = queryPointInPolygon(
                            StartPoint,
                            "Start"
                        );
                        EndCountry = queryPointInPolygon(
                            EndPoint,
                            "End"
                        );

                        // Add the popup to the route
                        const popupContent = document.createElement("div"); // Create a container for the Vue component
                        const app = createApp(CargoRoutePopup, {
                            cargoId: item.cargo_id,
                            cargoType: item.cargotype,
                            StartCountry: StartCountry,
                            EndCountry: EndCountry,
                        });
                        app.use(Antd).mount(popupContent); // Mount the Vue component
                        layer.bindPopup(popupContent);
                    },
                });

                // Add the route to the map
                const CurrentRoute = new CargoRoute(
                    item.cargo_id,
                    item.cargotype,
                    geoJsonLayer,
                    StartCountry,
                    EndCountry
                );
                const CoordinatesLength = JSON.parse(item.route).coordinates
                    .length;
                const Coordinates = JSON.parse(item.route).coordinates[
                    CoordinatesLength - 1
                ];
                CurrentRoute.DestinationMarker = L.marker(
                    [Coordinates[1], Coordinates[0]],
                    {
                        icon: DestinationIcon,
                    }
                ).addTo(Props.map);
                geoJsonLayer.addTo(Props.map);
                cargoRoutes.value.push(CurrentRoute);
            }
        } catch (error) {
            console.error("Error:", error);
        }
    } else {
        for (const route of cargoRoutes.value) {
            route.routeLayer.remove();
            route.DestinationMarker.remove();
        }
        cargoRoutes.value = [];

        if (
            EU_PolygonLayer.value &&
            Props.map.hasLayer(EU_PolygonLayer.value)
        ) {
            Props.map.removeLayer(EU_PolygonLayer.value);
        }
    }
});

const DoFilter = () => {
    console.log("CargoType Filter:", CargoTypeFilter.value);
    console.log("StartLocation Filter:", StartLocationFilter.value);
    if (Props.map) {
        // Filter the Cargo Type
        for (const route of cargoRoutes.value) {
            if (CargoTypeFilter.value.includes(route.cargotype)) {
                route.routeLayer.addTo(Props.map);
                route.DestinationMarker.addTo(Props.map);
            } else {
                route.routeLayer.remove();
                route.DestinationMarker.remove();
            }
        }

        // Filter the Start/End Location
        for (const route of cargoRoutes.value) {
            if (StartLocationFilter.value.includes(route.StartCountry)) {
                route.routeLayer.addTo(Props.map);
                route.DestinationMarker.addTo(Props.map);
            } else {
                route.routeLayer.remove();
                route.DestinationMarker.remove();
            }
        }
        for (const route of cargoRoutes.value) {
            if (EndLocationFilter.value.includes(route.EndCountry)) {
                route.routeLayer.addTo(Props.map);
                route.DestinationMarker.addTo(Props.map);
            } else {
                route.routeLayer.remove();
                route.DestinationMarker.remove();
            }
        }

        if (StartLocationFilter.value.length == 0 && CargoTypeFilter.value.length == 0 && EndLocationFilter.value.length == 0) {

            for (const route of cargoRoutes.value) {
                route.routeLayer.addTo(Props.map);
                route.DestinationMarker.addTo(Props.map);
            }
        }
    }
};

function loadWFS_Polygon(layerName, epsg, TargetLayer) {
    var urlString = "http://localhost:8083/geoserver/ne/ows";
    var param = {
        service: "WFS",
        version: "1.0.0", // Use 1.0.0 to match your URL
        request: "GetFeature",
        typeName: layerName, // 'pgLayer:cargo' in your case
        outputFormat: "application/json",
        maxFeatures: 5000, // Limit to 50 features
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
        TargetLayer.value = L.geoJSON(data, {
            onEachFeature: function (feature, layer) {
                layer.setStyle(EUPolygonStyle);
            },
        });

        Props.map.addLayer(TargetLayer.value);
    }
}

function queryPointInPolygon(point, QueryType) {
    if (EU_PolygonLayer && EU_PolygonLayer.value) {
        const results = leafletPip.pointInLayer(point, EU_PolygonLayer.value);
        if (results.length > 0) {
            var StartCountry = results[0].feature.properties.NAME_EN;

            if (StartCountry && !StartLocationoptions.value.some(option => option.value === StartCountry) && QueryType == "Start") {
                StartLocationoptions.value.push({
                    label: StartCountry,
                    value: StartCountry,
                });
            }
            if (StartCountry && !EndLocationoptions.value.some(option => option.value === StartCountry) && QueryType == "End") {
                EndLocationoptions.value.push({
                    label: StartCountry,
                    value: StartCountry,
                });
            }

            return StartCountry;
        }
    }
}
</script>

<style scoped>
.container {
    width: 250px;
    height: 500px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 15px;
}

.disabled-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 10px; /* Adjust the space between text and switch */
    line-height: 30px;
}
</style>
