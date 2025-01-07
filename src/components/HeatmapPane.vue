<template>
  <div class="container">
    <div class="disabled-section">
      <span>Radius:</span>
      <a-switch v-model:checked="radius_disabled" size="small" class="switch" />
    </div>
    <a-slider
      id="test"
      v-model:value="HeatmapRadius"
      :disabled="disabled"
      class="slider"
    />
    <div class="disabled-section">
      <span>Blur:</span>
      <a-switch v-model:checked="blur_disabled" size="small" class="switch" />
    </div>
    <a-slider
      id="test"
      v-model:value="HeatmapBlur"
      :disabled="disabled"
      class="slider"
    />
  </div>
</template>

<script setup>
import { reactive, ref, watch, h, defineProps, onMounted } from "vue";
import { DisplayHeatmap, PageIndex } from "@/stores/Status.js";
import { storeToRefs } from "pinia";
import L from "leaflet";
import "leaflet.heat";

const radius_disabled = ref(false);
const blur_disabled = ref(false);

const Props = defineProps({
  map: Object,
  TruckMarkers: Array,
  CargoMarkers: Array,
});

const HeatmapBlur = ref(50);
const HeatmapRadius = ref(50);
var heat = ref(
  L.heatLayer([], { radius: HeatmapBlur.value, blur: HeatmapRadius.value })
);

const HeatmapMode = DisplayHeatmap();
const CurrentPageIndex = PageIndex();
const { status: Heatmap } = storeToRefs(HeatmapMode);
const { PageIndex: CurrentPage } = storeToRefs(CurrentPageIndex);

watch(
  () => Props.map,
  (Newmap) => {
    Newmap.createPane("heatmapPane"); // Custom pane
    Newmap.getPane("heatmapPane").style.zIndex = 650;
    heat.value.pane = "heatmapPane";
    Newmap.addLayer(heat.value);
  }
);

watch(Heatmap, (NewHeatmap) => {
  let Markers = [];
  if (CurrentPage.value == "Trucks") {
    Markers = Props.TruckMarkers;
  } else if (CurrentPage.value == "Cargoes") {
    Markers = Props.CargoMarkers;
  }
  if (NewHeatmap && Props.map && Markers.length > 0) {
    let HeatpointData = [];
    for (let i = 0; i < Markers.length; i++) {
      const latLng = Markers[i].getLatLng();
      HeatpointData.push([latLng.lat, latLng.lng, 20.0]);
    }
    heat.value.setLatLngs(HeatpointData);
  } else {
    heat.value.setLatLngs([]);
  }
});

watch(
  [HeatmapBlur, HeatmapRadius],
  ([newBlur, newRadius]) => {
    if (heat.value) {
      heat.value.setOptions({
        radius: newRadius,
        blur: newBlur,
      });
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.code-box-demo .ant-slider {
  margin-bottom: 16px;
}

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
}

.switch {
  margin-left: 10px;
}

.slider {
  width: 100%;
  margin-bottom: 10px; /* Add space between sliders */
}
</style>
