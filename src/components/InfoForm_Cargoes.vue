<template>
    <div style="opacity: 0.8" class="InfoContainer">
        <h3>Information Form</h3>
        <p>Coordinates: {{ lat.toFixed(2) }}, {{ lng.toFixed(2) }}</p>

        <!-- Name Input -->
        <div class="input-group">
            <label for="Name" style="width: 10cm">Name:</label>
            <input id="Name" v-model="CargoName" placeholder="Enter Name" />
        </div>
        <br />
        <!-- Type Input -->
        <div class="input-group">
            <label for="CargoType" style="width: 10cm">Type:</label>
            <input
                id="CargoType"
                v-model="CargoType"
                list="CargoTypeList"
                placeholder="Select Status"
            />
            <datalist id="CargoTypeList">
                <option>Normal</option>
                <option>Overweight</option>
                <option>Hazardous</option>
                <option>Frozen</option>
            </datalist>
        </div>
        <br />
        <!-- Weight Input -->
        <div class="input-group">
            <label for="CargoWeight" style="width: 10cm">Weight:</label>
            <input
                id="CargoWeight"
                v-model="CargoWeight"
                placeholder="Enter Weight"
            />
        </div>
        <br />
        <!-- Status Input -->
        <div class="input-group">
            <label for="CargoStatus" style="width: 10cm">Status:</label>
            <input
                id="CargoStatus"
                v-model="CargoStatus"
                list="CargoStatusList"
                placeholder="Select Statu"
            />
            <datalist id="CargoStatusList">
                <option>Pending</option>
                <option>In Transit</option>
                <option>Arrive</option>
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
            <button @click="HandleSubmitClick" id="CargoSubmit">Submit</button>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { AddCargoesStatus, UpdateCargoesStatus } from "@/stores/Status.js";

const props = defineProps({
    lat: Number,
    lng: Number,
    ID: Number,
    CargoesStatus: String,
    CargoesInfo: String,
    CargoesName: String,
    CargoesType: String,
    CargoesWeight: [String, Number],
});
const info = ref(props.CargoesInfo);
const CargoName = ref(props.CargoesName);
const CargoType = ref(props.CargoesType);
const CargoStatus = ref(props.CargoesStatus);
const CargoWeight = ref(props.CargoesWeight);

const AddCargoes = AddCargoesStatus();
const UpdateCargoes = UpdateCargoesStatus();

const emit = defineEmits(["AddedCargoes"]);

const HandleSubmitClick = async () => {
    if (AddCargoes.status == true) {
        AddNewCargo();
    }
    if (UpdateCargoes.status == true) {
        AlterCargo();
    }
};
const AlterCargo = async () => {
    console.log(
        `Submitted info: ${info.value} ${CargoName.value} ${CargoType.value} ${CargoStatus.value} ${CargoWeight.value}`
    );

    // Make a POST request to the Flask API to insert data
    try {
        const response = await fetch("http://127.0.0.1:5000/cargo-update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                Info: info.value,
                lat: props.lat,
                lng: props.lng,
                CargoName: CargoName.value,
                CargoType: CargoType.value,
                CargoStatus: CargoStatus.value,
                CargoWeight: CargoWeight.value,
                CargoID: props.ID,
            }), // Send the input value
        });

        const result = await response.json();
        if (response.ok) {
            console.log(result.message); // Handle successful insertion
        } else {
            console.error(result.error); // Handle errors
        }

        emit("AddedCargoes", {
            ID: props.ID,
        });
    } catch (error) {
        console.error("Error:", error);
    }
};
const AddNewCargo = async () => {
    console.log(
        `Submitted info: ${info.value} ${CargoName.value} ${CargoType.value} ${CargoStatus.value} ${CargoWeight.value}`
    );

    // Make a POST request to the Flask API to insert data
    try {
        const response = await fetch("http://127.0.0.1:5000/cargo-insert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                Info: info.value,
                lat: props.lat,
                lng: props.lng,
                CargoName: CargoName.value,
                CargoType: CargoType.value,
                CargoStatus: CargoStatus.value,
                CargoWeight: CargoWeight.value,
            }), // Send the input value
        });

        const result = await response.json();
        if (response.ok) {
            console.log(result.message); // Handle successful insertion
        } else {
            console.error(result.error); // Handle errors
        }

        emit("AddedCargoes", {
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

#CargoSubmit {
    background-color: #349de2;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    font-size: 16px;
}

#CargoSubmit:hover {
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
