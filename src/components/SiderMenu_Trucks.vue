<template>
    <a-menu id="dddddd" v-model:openKeys="openKeys" v-model:selectedKeys="selectedKeys"
        :style="{ width: '256px', opacity: 0.7 }" mode="inline" :items="items" @click="handleClick"
        style="opacity: 0.7; background-color: white"></a-menu>
</template>
<script setup>
import { reactive, ref, watch, h } from "vue";
import { AddTrucksStatus, DeleteTrucksStatus, UpdateTrucksStatus, DisplayHeatmap, Truck_SelectCargo, Truck_ViewRouteStatus } from "@/stores/Status.js";
import {
    AimOutlined,
    AppstoreOutlined,
    SettingOutlined,
    HeatMapOutlined,
    AppstoreAddOutlined,
    DeleteOutlined,
    UploadOutlined,
    SelectOutlined,
} from "@ant-design/icons-vue";
const selectedKeys = ref(["DeleteTrucks"]);
const openKeys = ref(["sub1"]);
function getItem(label, key, icon, children, type) {
    return {
        key,
        icon,
        children,
        label,
        type,
    };
}
const items = reactive([
    getItem("Navigation One", "sub1", () => h(AimOutlined), [
        getItem(
            "Item 1",
            "g1",
            null,
            [getItem("Add Trucks", "Add-Trucks", ()=> h(AppstoreAddOutlined)), getItem("Delete Trucks", "Delete-Trucks", ()=> h(DeleteOutlined)), getItem("Update Trucks", "Update-Trucks", ()=> h(UploadOutlined))],   
            "group"
        ),
        getItem(
            "Item 2",
            "g2",
            null,
            [getItem("Heatmap", "Heatmap", ()=>h(HeatMapOutlined))],
            "group"
        ),
    ]),
    getItem("Navigation Two", "sub2", () => h(AppstoreOutlined), [
        getItem("Select Cargo", "Select Cargo", ()=> h(SelectOutlined)),
        getItem("View Route", "View Route"),
    ]),
]);
const handleClick = (e) => {
    console.log("click side menu", e.key);

    const AddTrucksMode = AddTrucksStatus();
    const DeleteTrucksMode = DeleteTrucksStatus();
    const UpdatesTruckMode = UpdateTrucksStatus();
    const HeatmapMode = DisplayHeatmap();
    const SelectCargoMode = Truck_SelectCargo();
    const ViewRouteMode = Truck_ViewRouteStatus();
    if (e.key == "Add-Trucks") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            AddTrucksMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            AddTrucksMode.updateStatus(true);
        }
    } else {
        AddTrucksMode.updateStatus(false);
    }
    if (e.key == "Delete-Trucks") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            DeleteTrucksMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            DeleteTrucksMode.updateStatus(true);
        }
    } else {
        DeleteTrucksMode.updateStatus(false);
    }
    if (e.key == "Update-Trucks") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            UpdatesTruckMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            UpdatesTruckMode.updateStatus(true);
        }
    } else {
        UpdatesTruckMode.updateStatus(false);
    }

    //handel click heatmap
    if (e.key == "Heatmap") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            HeatmapMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            HeatmapMode.updateStatus(true);
        }
    } else {
        HeatmapMode.updateStatus(false);
    }

    //handel click SelectCargo
    if (e.key == "Select Cargo") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            SelectCargoMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            SelectCargoMode.updateStatus(true);
        }
    } else {
        SelectCargoMode.updateStatus(false);
    }

    //handel click ViewRoute
    if (e.key == "View Route") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            ViewRouteMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            ViewRouteMode.updateStatus(true);
        }
    } else {
        ViewRouteMode.updateStatus(false);
    }
};
watch(openKeys, (val) => {
    console.log("openKeys", val);
});
</script>
