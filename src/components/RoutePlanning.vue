<template>
    <div class="container">
        <div class="disabled-section">
            <span>Select Destination:</span>
            <a-switch
                v-model:checked="SelectDestination"
                size="small"
                class="switch"
            />
        </div>
        <div class="disabled-section">
            <span>Add Waypoints:</span>
            <a-switch
                v-model:checked="AddWaypoints"
                size="small"
                class="switch"
            />
        </div>
        <a-button type="primary" @click="HandleConfirm">Confirm</a-button>
    </div>
</template>

<script setup>
import { ref, onMounted, defineProps, watch } from "vue";
import { Cargo_AddRouteStatus } from "@/stores/Status.js";
import { storeToRefs } from "pinia";
import L, { map } from "leaflet";
import "leaflet-routing-machine";

const Props = defineProps({
    map: Object,
    SelectedMarker: Object,
});

const Cargo_AddRouteMode = Cargo_AddRouteStatus();
const { status: Cargo_AddRoute } = storeToRefs(Cargo_AddRouteMode);

const SelectDestination = ref(false);
const AddWaypoints = ref(false);

const Routing = ref(null);
const waypoints = ref([]);
const coords = ref([]);
watch(
    () => Props.map,
    (Newmap) => {
        Routing.value = L.Routing.control({
            waypoints: waypoints.value,
            routeWhileDragging: true,
            geocoder: L.Control.Geocoder.nominatim(),
            showAlternatives: false,
        });

        Routing.value.on("routesfound", function (e) {
            coords.value = e.routes[0].coordinates;
        });
    }
);

watch(
    () => Props.SelectedMarker,
    (NewSelectedMarker) => {
        if (
            NewSelectedMarker &&
            Props.map &&
            Routing.value &&
            Cargo_AddRoute.value
        ) {
            console.log(
                "AddRouteMode",
                Cargo_AddRoute.value,
                "SelectMarker:",
                NewSelectedMarker.options.ID
            );
            waypoints.value[0] = NewSelectedMarker.getLatLng();
            Routing.value.setWaypoints(waypoints.value);
        }
    }
);

watch(Cargo_AddRoute, (val) => {
    console.log("Cargo_AddRoute");
    if (val && Routing.value && Props.map) {
        Routing.value.addTo(Props.map);
    } else {
        Props.map.off("click", ChangeDestination);
        Routing.value.remove();
    }
});

watch(SelectDestination, (val) => {
    if (val && Routing.value && Props.map) {
        Props.map.on("click", ChangeDestination);
    } else {
        Props.map.off("click", ChangeDestination);
    }
});

function ChangeDestination(e) {
    let NewDestination = e.latlng;
    if (Props.map && Routing.value) {
        if (waypoints.value.length < 2) {
            waypoints.value[waypoints.value.length] = NewDestination;
        } else {
            waypoints.value[waypoints.value.length - 1] = NewDestination;
        }
        Routing.value.setWaypoints(waypoints.value);
        console.log("New Waypoints", NewDestination);
    }
}

const HandleConfirm = async () => {
    const wktCoords = coords.value
        .map((coord) => `${coord.lng} ${coord.lat}`)
        .join(",");
    const wktLineString = `LINESTRING(${wktCoords})`;
    console.log(Props.SelectedMarker.ID);
    try {
        const response = await fetch("http://127.0.0.1:5000/cargo-add-route", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                CargoID: Props.SelectedMarker.options.ID,
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

.disabled-section {
    display: flex;
    align-items: center;
    margin-bottom: 10px; /* Adjust the space between text and switch */
    line-height: 30px;
    color: darkgrey;
}

.switch {
    margin-left: 10px;
}
</style>
