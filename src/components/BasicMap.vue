<template>
  <div id="MapContainer">
    <div class="BasicMap" id="LMap"></div>
  </div>

  <a-row :gutter="16">
    <a-col :span:="12">
      <a-layout-sider class="Sider" :width="256">
        <SiderMenu_Cargoes v-if="CurrentPageIndex === 'Cargoes'" />
        <SiderMenu_Trucks v-if="CurrentPageIndex === 'Trucks'" />
      </a-layout-sider>
    </a-col>
    <a-col :span:="12">
      <div class="RoutePlanningPane" :width="256" v-show="Cargo_AddRoute">
        <RoutePlanning :map="map" :SelectedMarker="SelectedMarker"/>
      </div>
      <div class="ViewRoutePane" :width="256" v-show="Cargo_ViewRoute">
        <ViewRoute :map="map" :SelectedMarker="SelectedMarker"/>
      </div>
      <div class="SelecteCargoPane" :width="256" v-show="TruckSelectCargo">
        <SelectCargo_Truck :map="map" :SelectedMarker="SelectedMarker" :ReachabilityLayer="ReachabilityLayer" @Add-Reachability="AddReachabilityControl" @Remove-Reachability="RemoveReachabilityControl"/>
      </div>
      <div class="Truck_ViewRoutePane" :width="256" v-show="Truck_ViewRoute">
        <ViewRoute_Trucks :map="map" :SelectedMarker="SelectedMarker"/>
      </div>
    </a-col>
  </a-row>
  </br>
  <div class="HeatmapPane" v-show="Heatmap">
    <HeatmapPane :map="map" :CargoMarkers="CargoesMarker" :TruckMarkers="TrucksMarker"/>
  </div>
</template>

<script setup lang="ts">
import { createApp, onMounted, ref, watch } from "vue";
import SiderMenu_Cargoes from "@/components/SiderMenu_Cargoes.vue";
import HeatmapPane from "@/components/HeatmapPane.vue";
import RoutePlanning from "@/components/RoutePlanning.vue";
import ViewRoute from "@/components/ViewRoute_Cargoes.vue";
import SelectCargo_Truck from "@/components/SelectCargo_Truck.vue";
import ViewRoute_Trucks from "@/components/ViewRoute_Trucks.vue";
import CargoesLogo from "@/image/Normal.png";
import SiderMenu_Trucks from "@/components/SiderMenu_Trucks.vue";
import IconShadow from "@/image/marker-shadow.png";
import LefaletMarkerLogo from "@/image/marker-icon.png";
import FrozenLogo from "@/image/frozen.png";
import OverweightLogo from "@/image/Overweight.png";
import HazardousLogo from "@/image/Hazardous.png";
import ScaniaLogo from "@/image/scania.png";
import MANLogo from "@/image/MAN.png";
import BenzLogo from "@/image/Benz.png";
import RenaultLogo from "@/image/Renault.png";
import {
  AddRouteStatus,
  AddCargoesStatus,
  DeleteCargoesStatus,
  PageIndex,
  AddTrucksStatus,
  DeleteTrucksStatus,
  DisplayHeatmap,
  Cargo_AddRouteStatus,
  Cargo_ViewRouteStatus,
  Truck_SelectCargo,
  Truck_ViewRouteStatus,
} from "@/stores/Status.js";
import { storeToRefs } from "pinia";
import InfoForm_Cargoes from "./InfoForm_Cargoes.vue";
import { DesignTokenProvider } from "ant-design-vue/es/theme/internal";
import InfoForm_Trucks from "./InfoForm_Trucks.vue";

import L, { Icon, latLng } from "leaflet";
import "leaflet.heat";
import * as GeoSearch from "leaflet-geosearch";
import "leaflet-routing-machine";
import "leaflet-control-geocoder";
import { icon } from "leaflet";
import "leaflet.markercluster";

import "@/assets/leaflet.reachability.js";

const searchControl = new GeoSearch.GeoSearchControl({
  provider: new GeoSearch.OpenStreetMapProvider(),
  style: "bar",
});

const map = ref(null);
const CargoesMarker = ref([]);
const NewCargoesMarker = ref([]);
const TrucksMarker = ref([]);
const NewTrucksMarker = ref([]);
let AddCargoesIndex = 0;
let AddTrucksIndex = 0;
const SelectedMarker = ref(null);

const TrucksMarkerGroup = ref(L.markerClusterGroup());
const CargoesMarkerGroup = ref(L.markerClusterGroup());

const AddCargoesMode = AddCargoesStatus();
const CurrentPage = PageIndex();
const DeleteCargoesMode = DeleteCargoesStatus();
const AddTrucksMode = AddTrucksStatus();
const DeleteTrucksMode = DeleteTrucksStatus();
const HeatmapMode = DisplayHeatmap();
const Cargo_ViewRouteMode = Cargo_ViewRouteStatus();
const Cargo_AddRouteMode = Cargo_AddRouteStatus();
const TruckSelectCargoMode = Truck_SelectCargo();
const Truck_ViewRouteMode = Truck_ViewRouteStatus();
const { status: AddCargoes } = storeToRefs(AddCargoesMode);
const { status: DeleteCargoes } = storeToRefs(DeleteCargoesMode);
const { PageIndex: CurrentPageIndex } = storeToRefs(CurrentPage);
const { status: AddTrucks } = storeToRefs(AddTrucksMode);
const { status: DeleteTrucks } = storeToRefs(DeleteTrucksMode);
const { status: Heatmap } = storeToRefs(HeatmapMode);
const { status: Cargo_AddRoute } = storeToRefs(Cargo_AddRouteMode);
const { status: Cargo_ViewRoute } = storeToRefs(Cargo_ViewRouteMode);
const { status: TruckSelectCargo } = storeToRefs(TruckSelectCargoMode);
const { status: Truck_ViewRoute } = storeToRefs(Truck_ViewRouteMode);

const popupContentRef = ref(null);

// define icon for new cargoes
var NormalCargoesIcon = L.icon({
  iconUrl: CargoesLogo,

  iconSize: [30, 30], // size of the icon
  shadowSize: [50, 64], // size of the shadow
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [0, -20], // point from which the popup should open relative to the iconAnchor
});
var LeafletIcon = L.icon({
  iconUrl: LefaletMarkerLogo,
  shadowUrl: IconShadow,

  iconSize: [38, 95],
  iconAnchor: [22, 94],
  popupAnchor: [-3, -76],
  shadowSize: [68, 95],
  shadowAnchor: [22, 94],
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
var ScaniaIcon = L.icon({
  iconUrl: ScaniaLogo,

  iconSize: [30, 30], // size of the icon
  shadowSize: [50, 64], // size of the shadow
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [0, -30], // point from which the popup should open relative to the iconAnchor
});
var MANIcon = L.icon({
  iconUrl: MANLogo,

  iconSize: [30, 30], // size of the icon
  shadowSize: [50, 64], // size of the shadow
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [0, -30], // point from which the popup should open relative to the iconAnchor
});
var BenzIcon = L.icon({
  iconUrl: BenzLogo,

  iconSize: [30, 30], // size of the icon
  shadowSize: [50, 64], // size of the shadow
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [0, -30], // point from which the popup should open relative to the iconAnchor
});
var RenaultIcon = L.icon({
  iconUrl: RenaultLogo,

  iconSize: [30, 30], // size of the icon
  shadowSize: [50, 64], // size of the shadow
  iconAnchor: [15, 15], // point of the icon which will correspond to marker's location
  shadowAnchor: [4, 62], // the same for the shadow
  popupAnchor: [0, -30], // point from which the popup should open relative to the iconAnchor
});

// watch the page index
watch(CurrentPageIndex, async (value) => {
  console.log("CurrentPageIndex", value);
  if (value == "Cargoes") {
    AddAllCargoes();
  } else {
    DeleteAllCargoes();

    DeleteCargoes.value = false;
    AddCargoes.value = false;
    Cargo_ViewRoute.value = false;
  }

  if (value == "Trucks") {
    AddAllTrucks();
  } else {
    DeleteAllTrucks();

    DeleteTrucks.value = false;
    AddTrucks.value = false;
    Truck_ViewRoute.value = false;
    TruckSelectCargo.value = false;
  }

  Heatmap.value = false;
});

function DeleteAllCargoes() {
   // Remove all the cargoes marker
    if (CargoesMarker.value.length > 0) {
      CargoesMarker.value.forEach((element) => {
        element.off("click");
        element.off("mouseover");
        if (map.value.hasLayer(element)) {
          map.value.removeLayer(element);
          console.log("Remove Cargoes Marker");
        }
        element.remove();
      });
      CargoesMarker.value = [];
    }
    if (NewCargoesMarker.value.length > 0) {
      NewCargoesMarker.value.forEach((element) => {
        element.off("click");
        element.off("mouseover");
        if (map.value.hasLayer(element)) {
          map.value.removeLayer(element);
          console.log("Remove temp Cargoes Marker");
        }
        element.remove();
      });
      NewCargoesMarker.value = [];
      AddCargoesIndex = 0;
    }

    // Remove the Cargoes Marker Group Layer
    if (map.value.hasLayer(CargoesMarkerGroup.value)) {
      map.value.removeLayer(CargoesMarkerGroup.value);
      CargoesMarkerGroup.value.clearLayers();
      console.log("Remove Cargo Marker Group");
    }
}
async function AddAllCargoes() {
  try {
    const PointData = await fetchCargoesData(); 
    if (PointData) {
      AddCargoesMarker(PointData); 
    }
  } catch (error) {
    console.error("Error fetching cargo data:", error); 
  }
}
function DeleteAllTrucks() {
  // Remove all the cargoes marker
  if (TrucksMarker.value.length > 0) {
    TrucksMarker.value.forEach((element) => {
      element.off("click");
      element.off("mouseover");
      if (map.value.hasLayer(element)) {
        map.value.removeLayer(element);
      }
      element.remove();
    });
    console.log("Remove Truck Marker");
    TrucksMarker.value = [];
  }
  if (NewTrucksMarker.value.length > 0) {
    NewTrucksMarker.value.forEach((element) => {
      element.off("click");
      element.off("mouseover");
      if (map.value.hasLayer(element)) {
        map.value.removeLayer(element);
      }
      element.remove();
    });
    console.log("Remove temp Cargoes Marker");
    NewTrucksMarker.value = [];
    AddTrucksIndex = 0;
  }

  // Remove the Trucks Marker Group Layer
  if (map.value.hasLayer(TrucksMarkerGroup.value)) {
    map.value.removeLayer(TrucksMarkerGroup.value);
    TrucksMarkerGroup.value.clearLayers();
    console.log("Remove Truck Marker Group");
  }
}
async function AddAllTrucks() {
  try {
    const PointData = await fetchTrucksData();
    if (PointData) {
      AddTrucksMarker(PointData);
    }
  } catch (error) {
    console.error("Error fetching truck data:", error);
  }
}

// watch the add cargoes mode
watch(AddCargoes, async (value) => {
  console.log("AddCargoesMode", value);
  if (value == false) {
    map.value.off("click", HandleMapClick_AddCargo);
    if (NewCargoesMarker.value.length > 0) {
      NewCargoesMarker.value.forEach((element: L.Marker) => {
        element.off("click");
        element.off("mouseover");
        if (map.value.hasLayer(element)) {
          map.value.removeLayer(element);
          console.log("Remove temp Cargoes Marker");
        }
        element.remove();
      });
      NewCargoesMarker.value = [];
      AddCargoesIndex = 0;
    }

    DeleteAllCargoes();
    AddAllCargoes();
  } else {
    map.value.on("click", HandleMapClick_AddCargo);
  }
});
// wawtch the delete cargoes mode
watch(DeleteCargoes, async (value) => {
  console.log("DeleteCargoesMode", value);
  if (value == true) {
    if (CargoesMarker.value.length > 0) {
      CargoesMarker.value.forEach((element) => {
        element.on("dblclick", function (ev) {
          const CargoesIDs = element.options.ID;
          console.log("Try Delete Cargoes Marker", CargoesIDs);

          deleteCargoes([CargoesIDs]);
        });
      });
    }
  } else {
    if (CargoesMarker.value.length > 0) {
      CargoesMarker.value.forEach((element) => {
        element.off("dbclick");
      });
    }
  }
});
// watch the add trucks mode
watch(AddTrucks, async (value) => {
  console.log("AddTrucksMode", value);
  if (value == false) {
    map.value.off("click", HandleMapClick_AddTruck);
    if (NewTrucksMarker.value.length > 0) {
      NewTrucksMarker.value.forEach((element: L.Marker) => {
        element.off("click");
        element.off("mouseover");
        if (map.value.hasLayer(element)) {
          map.value.removeLayer(element);
          console.log("Remove temp Trucks Marker");
        }
        element.remove();
      });
      NewTrucksMarker.value = [];
      AddTrucksIndex = 0;
    }
  } else {
    map.value.on("click", HandleMapClick_AddTruck);
  }
});
// watch the delete trucks mode
watch(DeleteTrucks, async (value) => {
  console.log("DeleteCargoesMode", value);
  if (value == true) {
    if (TrucksMarker.value.length > 0) {
      TrucksMarker.value.forEach((element) => {
        element.on("dblclick", function (ev) {
          const TrucksID = element.options.ID;
          console.log("Try Delete Trucks Marker", TrucksID);

          deleteTrucks([TrucksID]);
        });
      });
    }
  } else {
    if (TrucksMarker.value.length > 0) {
      TrucksMarker.value.forEach((element) => {
        element.off("dbclick");
      });
    }
  }
});

// Get all cargoes from database
const fetchCargoesData = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/cargo-get-data");
    if (!response.ok) {
      throw new Error("Failed to fetch route data");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching route data:", error);
    return null;
  }
};
// Get all trucks from database
const fetchTrucksData = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/truck-get-data");
    if (!response.ok) {
      throw new Error("Failed to fetch truck data");
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching turck data:", error);
    return null;
  }
};

function AddCargoesMarker(data: any) {
  console.log("CargoesData\n", data);
  data.data.forEach((element: any) => {
    const latlng = { lat: element.lat, lng: element.lng };
    const PopupApp = createApp(InfoForm_Cargoes, {
      lat: parseFloat(element.lat),
      lng: parseFloat(element.lng),
      ID: element.cargo_id,
      CargoesInfo: element.Info,
      CargoesName: element.cargoname,
      CargoesType: element.cargotype,
      CargoesStatus: element.cargostatus,
      CargoesWeight: element.cargoweight,
    });

    const marker = L.marker([element.lat, element.lng], {
      draggable: false,
      ID: element.cargo_id,
      MarkerType: "Cargo",
      riseOnHover: true,
      opacity: 1.0,
    });
    if (element.cargotype == "Frozen") {
      marker.setIcon(FrozenCargoesIcon);
    }
    if (element.cargotype == "Overweight") {
      marker.setIcon(OverweightCargoesIcon);
    }
    if (element.cargotype == "Hazardous") {
      marker.setIcon(HazardousCargoesIcon);
    }
    if (element.cargotype == "Normal") {
      marker.setIcon(NormalCargoesIcon);
    }

    // Create a popup for the cargoes marker
    const div = document.createElement("div");
    popupContentRef.value = div;
    PopupApp.mount(div);
    var Popup = L.popup({
      autoClose: true,
      closeOnClick: true,
      closeButton: true,
    }).setContent(popupContentRef.value);
    marker.bindPopup(Popup);
    marker.closePopup();
    // set the event for the marker
    marker.on("click", function (ev) {
      ev.target.openPopup();
      SelectedMarker.value = ev.target;
    });
    marker.on("mouseover", function (ev) {
      var GetIcon = ev.target.options.icon;
      GetIcon.options.iconSize = [50, 50];
      GetIcon.options.iconAnchor = [25, 25];
      ev.target.setIcon(GetIcon);
    });
    marker.on("mouseout", function (ev) {
      var GetIcon = ev.target.options.icon;
      GetIcon.options.iconSize = [30, 30];
      GetIcon.options.iconAnchor = [15, 15];
      ev.target.setIcon(GetIcon);
    });

    // Add to the Marker Array
    CargoesMarker.value.push(marker);

    CargoesMarkerGroup.value.addLayer(marker);
  });
  map.value.addLayer(CargoesMarkerGroup.value);
}
// Handle Add Cargoes Event
function HandleMapClick_AddCargo(e) {
  console.log("Map Clicked");

  if (AddCargoes.value == true) {
    const latlng = e.latlng;
    var marker = L.marker(latlng, {
      draggable: true,
      TempID: AddCargoesIndex,
    }).addTo(map.value);

    // Create a popup for the new cargoes marker
    const div = document.createElement("div");
    popupContentRef.value = div;
    const PopupApp = createApp(InfoForm_Cargoes, {
      lat: parseFloat(latlng.lat),
      lng: parseFloat(latlng.lng),
      ID: AddCargoesIndex,
    });
    PopupApp.mount(div);
    marker.bindPopup(popupContentRef.value).openPopup();

    // Create Event for the Marker
    // mouseover open popup
    marker.on("mouseover", function (ev) {
      ev.target.openPopup();
    });
    // double click remove marker
    marker.on("dblclick", function (ev) {
      for (let i = 0; i < NewCargoesMarker.value.length; i++) {
        if (
          NewCargoesMarker.value[i].options.TempID == ev.target.options.TempID
        ) {
          if (map.value.hasLayer(NewCargoesMarker.value[i])) {
            map.value.removeLayer(NewCargoesMarker.value[i]);
          }
          NewCargoesMarker.value.splice(i, 1);
        }
      }
      marker.remove();
      console.log("Remove New Cargoes Marker", NewCargoesMarker.value.length);
    });

    // Add to the New Marker Array
    NewCargoesMarker.value.push(marker);
    AddCargoesIndex++;
    console.log("Add New Cargoes Marker");
  }
}
// Handle Delete Cargoes Event
const deleteCargoes = async (CargoesIDs) => {
  try {
    console.log("Delete Cargoes Marker Request", CargoesIDs);
    const response = await fetch("http://127.0.0.1:5000/delete-cargoes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ids: CargoesIDs }),
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message);
      // Remove markers from the map
      CargoesIDs.forEach((id) => {
        const markerIndex = CargoesMarker.value.findIndex(
          (m) => m.options.ID === id
        );
        if (markerIndex !== -1) {
          // Remove from map
          CargoesMarker.value[markerIndex].remove();
          // Remove from array
          CargoesMarker.value.splice(markerIndex, 1);
        }
      });
    } else {
      console.error("Error:", result.error);
    }
  } catch (err) {
    console.error("Error:", err);
  }
};

// Hndle Add Trucks Event
function AddTrucksMarker(data: any) {
  console.log("CargoesData\n", data);
  data.data.forEach((element: any) => {
    const latlng = { lat: element.lat, lng: element.lng };
    const PopupApp = createApp(InfoForm_Trucks, {
      lat: parseFloat(element.lat),
      lng: parseFloat(element.lng),
      ID: element.truck_id,
      TruckInfo: element.Info,
      TruckName: element.truckname,
      TruckType: element.trucktype,
      TruckStatus: element.truckstatus,
      TruckWeight: element.truckweight,
    });

    const marker = L.marker([element.lat, element.lng], {
      draggable: false,
      ID: element.truck_id,
      MarkerType: "Truck",
      riseOnHover: true,
      opacity: 1.0,
    });
    if (element.truckname.includes("Scania")) {
      marker.setIcon(ScaniaIcon);
    }
    if (element.truckname.includes("MAN")) {
      marker.setIcon(MANIcon);
    }
    if (element.truckname.includes("Benz")) {
      marker.setIcon(BenzIcon);
    }
    if (element.truckname.includes("Renault")) {
      marker.setIcon(RenaultIcon);
    }

    // Create a popup for the cargoes marker
    const div = document.createElement("div");
    popupContentRef.value = div;
    PopupApp.mount(div);
    var Popup = L.popup({
      autoClose: true,
      closeOnClick: true,
      closeButton: true,
    }).setContent(popupContentRef.value);
    marker.bindPopup(Popup);
    marker.closePopup();
    // set the event for the marker
    marker.on("click", function (ev) {
      ev.target.openPopup();
      SelectedMarker.value = ev.target;
    });
    marker.on("mouseover", function (ev) {
      var GetIcon = ev.target.options.icon;
      GetIcon.options.iconSize = [50, 50];
      GetIcon.options.iconAnchor = [25, 25];
      ev.target.setIcon(GetIcon);
    });
    marker.on("mouseout", function (ev) {
      var GetIcon = ev.target.options.icon;
      GetIcon.options.iconSize = [30, 30];
      GetIcon.options.iconAnchor = [15, 15];
      ev.target.setIcon(GetIcon);
    });

    // Add to the Marker Array
    TrucksMarker.value.push(marker);

    TrucksMarkerGroup.value.addLayer(marker);
  });
  map.value.addLayer(TrucksMarkerGroup.value);
}
// Handle Add New Trucks Event
function HandleMapClick_AddTruck(e) {
  console.log("Map Clicked");

  if (AddTrucks.value == true) {
    const latlng = e.latlng;
    var marker = L.marker(latlng, {
      draggable: true,
      TempID: AddTrucksIndex,
    }).addTo(map.value);

    // Create a popup for the new cargoes marker
    const div = document.createElement("div");
    popupContentRef.value = div;
    const PopupApp = createApp(InfoForm_Trucks, {
      lat: parseFloat(latlng.lat),
      lng: parseFloat(latlng.lng),
      ID: AddTrucksIndex,
    });
    PopupApp.mount(div);
    marker.bindPopup(popupContentRef.value).openPopup();

    // Create Event for the Marker
    // mouseover open popup
    marker.on("mouseover", function (ev) {
      ev.target.openPopup();
    });
    // double click remove marker
    marker.on("dblclick", function (ev) {
      for (let i = 0; i < NewTrucksMarker.value.length; i++) {
        if (
          NewTrucksMarker.value[i].options.TempID == ev.target.options.TempID
        ) {
          if (map.value.hasLayer(NewTrucksMarker.value[i])) {
            map.value.removeLayer(NewTrucksMarker.value[i]);
          }
          NewTrucksMarker.value.splice(i, 1);
        }
      }
      marker.remove();
      console.log("Remove New Truck Marker", NewTrucksMarker.value.length);
    });

    // Add to the New Marker Array
    NewTrucksMarker.value.push(marker);
    AddTrucksIndex++;
    console.log("Add New Truck Marker");
  }
}
// Handle Delete Trucks Event
const deleteTrucks = async (TruckIDs) => {
  try {
    console.log("Delete Trucks Marker Request", TruckIDs);
    const response = await fetch("http://127.0.0.1:5000/delete-trucks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ids: TruckIDs }),
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message);
      // Remove markers from the map
      TruckIDs.forEach((id) => {
        const markerIndex = TrucksMarker.value.findIndex(
          (m) => m.options.ID === id
        );
        if (markerIndex !== -1) {
          // Remove from map
          TrucksMarker.value[markerIndex].remove();
          // Remove from array
          TrucksMarker.value.splice(markerIndex, 1);
        }
      });
    } else {
      console.error("Error:", result.error);
    }
  } catch (err) {
    console.error("Error:", err);
  }
};

const Reachability = ref(null);
const ReachabilityLayer = ref(null);
onMounted(() => {

  map.value = L.map("LMap").setView([57.03, 16.02], 3);
  console.log("Map Created");
  L.Marker.prototype._animateZoom = function (opt) {
    if (!this._map) {
      return;
    }
    const pos = this._map
      ._latLngToNewLayerPoint(this._latlng, opt.zoom, opt.center)
      .round();
    this._setPos(pos);
  };
  L.Popup.prototype._animateZoom = function (e) {
    if (!this._map) {
      return;
    }
    var pos = this._map._latLngToNewLayerPoint(this._latlng, e.zoom, e.center),
      anchor = this._getAnchor();
    L.DomUtil.setPosition(this._container, pos.add(anchor));
  };
  L.tileLayer("http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map.value);

  // Initialize  Reachability Control
  Reachability.value = L.control.reachability({
    apiKey: '5b3ce3597851110001cf62481af82f4307eb44569644ca66b47188a3',
    showOriginMarker: false,
    position: 'topright',
  });

  //Routing.addTo(map.value);
  map.value.addControl(searchControl);

});

// Add Reachability control

function AddReachabilityControl() {
  if (map.value) {
    map.value.addControl(Reachability.value);
    map.value.on("reachability:displayed", function (e) {
      console.log("Reachability Displayed");
      ReachabilityLayer.value = Reachability.value.latestIsolines;
    });
  }
}
function RemoveReachabilityControl() {
  if (map.value) {
    map.value.removeControl(Reachability.value);
    map.value.off("reachability:displayed");
    ReachabilityLayer.value = null;
  }
}

</script>

<style scoped>
@import "../assets/leaflet.reachability.css";
@import "../assets/MarkerCluster.css";
@import "../assets/MarkerCluster.Default.css";
#MapContainer {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 1;
}
#LMap {
  width: 100%;
  height: 100%;
  position: absolute;
  /* Set a height for the map */
}

.Sider {
  top: 100px;
  left: 10px;
  right: 10px;
  width: 256px;
  z-index: 10;
  opacity: 0.9;
  background-color: white;
  border-radius: 25px;
  overflow: hidden;
}

.HeatmapPane {
  position: relative;
  top: 110px;
  left: 10px;
  width: 256px;
  height: 150px;
  z-index: 100; /* Ensure this is above other elements */
  background-color: white;
  opacity: 0.9;
  border-radius: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.RoutePlanningPane {
  position: relative;
  top: 110px;
  left: 10px;
  width: 256px;
  height: 150px;
  z-index: 100; /* Ensure this is above other elements */
  background-color: white;
  opacity: 0.9;
  border-radius: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.ViewRoutePane {
  position: relative;
  top: 110px;
  left: 10px;
  width: 256px;
  height: 300px;
  z-index: 100; /* Ensure this is above other elements */
  background-color: white;
  opacity: 0.9;
  border-radius: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.SelecteCargoPane {
  position: relative;
  top: 110px;
  left: 10px;
  width: 256px;
  height: 150px;
  z-index: 100; /* Ensure this is above other elements */
  background-color: white;
  opacity: 0.9;
  border-radius: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}

.Truck_ViewRoutePane {
  position: relative;
  top: 110px;
  left: 10px;
  width: 256px;
  height: 150px;
  z-index: 100; /* Ensure this is above other elements */
  background-color: white;
  opacity: 0.9;
  border-radius: 25px;

  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
