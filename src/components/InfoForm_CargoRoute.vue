<template>
    <div>
        <p>Cargo ID: {{ Props.cargoId }}</p>
        <p>Type: {{ Props.cargoType }}</p>
        <p>StartCountry {{ Props.StartCountry }}</p>
        <p>EndCountry {{ Props.EndCountry }}</p>
        <a-button type="primary" @click="HandleDeleteRoute(Props.cargoId)">Delete Route</a-button>
    </div>
</template>

<script setup>
import { ref, defineProps, watch } from "vue";

const Props = defineProps({
    cargoId: String,
    cargoType: String,
    StartCountry: String,
    EndCountry: String,
});

async function HandleDeleteRoute(cargoId) {
  try {
    console.log("Delete Cargo Route Request", cargoId);

    const response = await fetch("http://127.0.0.1:5000/cargo-delete-route", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ CargoID: cargoId }), // Send CargoID in the body
    });

    const result = await response.json();

    if (response.ok) {
      console.log(result.message); // "Cargo route deleted successfully!"

      // Emit event or update frontend after successful deletion
      //emitDeleteRouteSuccess(cargoId);

    } else {
      console.error("Error deleting cargo route:", result.error);
      // Handle the error appropriately (e.g., display an error message to the user)
      // ...
    }
  } catch (err) {
    console.error("Error during cargo route deletion:", err);
    // Handle network or other errors
    // ...
  }
}
</script>
