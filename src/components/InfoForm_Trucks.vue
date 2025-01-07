<template>
  <div style="opacity: 0.8" class="InfoContainer">
    <h3>Information Form</h3>
    <p>Coordinates: {{ lat.toFixed(2) }}, {{ lng.toFixed(2) }}</p>

    <!-- Name Input -->
    <div class="input-group">
      <label for="Name" style="width: 10cm">Name:</label>
      <input id="Name" v-model="TruckName" placeholder="Enter Name" />
    </div>
    <br />
    <!-- Type Input -->
    <div class="input-group">
      <label for="TruckType" style="width: 10cm">Type:</label>
      <input
        id="TruckType"
        v-model="TruckType"
        list="TruckTypeList"
        placeholder="Select Type"
      />
      <datalist id="TruckTypeList">
        <option>Normal</option>
        <option>Overweight</option>
        <option>Hazardous</option>
        <option>Frozen</option>
      </datalist>
    </div>
    <br />
    <!-- Weight Input -->
    <div class="input-group">
      <label for="MaximumWeight" style="width: 10cm">Weight:</label>
      <input id="MaximumWeight" v-model="TruckWeight" placeholder="Enter MaximumWeight" />
    </div>
    <br />
    <!-- Status Input -->
    <div class="input-group">
      <label for="TruckStatus" style="width: 10cm">Status:</label>
      <input
        id="TruckStatus"
        v-model="TruckStatus"
        list="TruckStatusList"
        placeholder="Select Status"
      />
      <datalist id="TruckStatusList">
        <option>Await</option>
        <option>In Transit</option>
        <option>Resting</option>
      </datalist>
    </div>
    <br />
    <!-- Info Input -->
    <textarea
      id="Info"
      v-model="info"
      placeholder="Enter additional information here"
      rows="4"
      cols="50"
      style="resize: vertical; width: 100%"
    ></textarea>
    <br />
    <!-- Submit Button -->
    <div class="input-group">
      <button @click="HandleSubmitClick" id="TruckSubmit">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { AddTrucksStatus, UpdateTrucksStatus } from "@/stores/Status.js";

const props = defineProps({
  lat: Number,
  lng: Number,
  ID: Number,
  TruckStatus: String,
  TruckInfo: String,
  TruckName: String,
  TruckType: String,
  TruckWeight: [String, Number],
});
const info = ref(props.TruckInfo);
const TruckName = ref(props.TruckName);
const TruckType = ref(props.TruckType);
const TruckStatus = ref(props.TruckStatus);
const TruckWeight = ref(props.TruckWeight);

const AddTrucks = AddTrucksStatus();
const UpdateTrucks = UpdateTrucksStatus();

const emit = defineEmits(["AddedTruck"]);

const HandleSubmitClick = async () => {
  if (AddTrucks.status == true) {
    AddNewTruck();
  } 
  if (UpdateTrucks.status == true) {
    AlterTruck();
  }
};
const AlterTruck = async () => {
  console.log(`Submitted info: ${info.value} ${TruckName.value} ${TruckType.value} ${TruckStatus.value} ${TruckWeight.value}`);

  // Make a POST request to the Flask API to insert data
  try {
    const response = await fetch("http://127.0.0.1:5000/truck-update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Info: info.value,
        lat: props.lat,
        lng: props.lng,
        TruckName: TruckName.value,
        TruckType: TruckType.value,
        TruckStatus: TruckStatus.value,
        TruckWeight: TruckWeight.value,
        TruckID: props.ID,
      }), // Send the input value
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message); // Handle successful insertion
    } else {
      console.error(result.error); // Handle errors
    }

    emit("AddedTruck", {
      ID: props.ID,
    });
  } catch (error) {
    console.error("Error:", error);
  }
};
const AddNewTruck = async () => {
  console.log(`Submitted info: ${info.value} ${TruckName.value} ${TruckType.value} ${TruckStatus.value} ${TruckWeight.value}`);

  // Make a POST request to the Flask API to insert data
  try {
    const response = await fetch("http://127.0.0.1:5000/truck-insert", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Info: info.value,
        lat: props.lat,
        lng: props.lng,
        TruckName: TruckName.value,
        TruckType: TruckType.value,
        TruckStatus: TruckStatus.value,
        TruckWeight: TruckWeight.value,
      }), // Send the input value
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message); // Handle successful insertion
    } else {
      console.error(result.error); // Handle errors
    }

    emit("AddedTrucks", {
      ID: props.ID,
    });
  } catch (error) {
    console.error("Error:", error);
  }
};
</script>

<style scoped>
h3 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #333;
}

#TruckSubmit {
  background-color: #349de2;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}

#TruckSubmit:hover {
  background-color: #62c8f0;
}

.InfoContainer {
  background-color: #ffffff;
  border-radius: 8px;
  /* box-shadow: 0 4px 8px rgba(72, 22, 250, 0.1); */
  text-align: center;
}

.input-group {
  display: flex;
  justify-content: center;
  align-items: center;
  right: 40px;
}
</style>
