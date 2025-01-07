import { defineStore } from "pinia";

export const AddRouteStatus = defineStore("Add-Route-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const AddCargoesStatus = defineStore("Add-Cargoes-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const UpdateCargoesStatus = defineStore("Update-Cargoes-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const DeleteCargoesStatus = defineStore("Delete-Cargoes-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const PageIndex = defineStore("Page-Index", {
  state: () => ({
    PageIndex: "Orders",
  }),
  actions: {
    updateIndex(NewIndex) {
      this.PageIndex = NewIndex;
    },
  },
});

export const AddTrucksStatus = defineStore("Add-Trucks-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const UpdateTrucksStatus = defineStore("Update-Trucks-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const DeleteTrucksStatus = defineStore("Delete-Trucks-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const DisplayHeatmap = defineStore("DisplayHeatmap", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const Cargo_AddRouteStatus = defineStore("Cargo-AddRoute-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const Cargo_ViewRouteStatus = defineStore("Cargo-ViewRoute-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const Truck_SelectCargo = defineStore("Truck-SelectCargo", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});

export const Truck_ViewRouteStatus = defineStore("Truck-ViewRoute-Status", {
  state: () => ({
    status: false,
  }),
  actions: {
    updateStatus(status) {
      this.status = status;
    },
    toggleStatus() {
      this.status = !this.status;
    },
  },
});