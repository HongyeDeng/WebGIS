<template>
    <a-menu
        id="dddddd"
        v-model:openKeys="openKeys"
        v-model:selectedKeys="selectedKeys"
        :style="{ width: '256px', opacity: 0.7 }"
        mode="inline"
        :items="items"
        @click="handleClick"
        style="opacity: 0.7; background-color: white"
    ></a-menu>
</template>
<script setup>
import { reactive, ref, watch, h } from "vue";
import {
    AddCargoesStatus,
    DeleteCargoesStatus,
    UpdateCargoesStatus,
    DisplayHeatmap,
    Cargo_AddRouteStatus,
    Cargo_ViewRouteStatus,
} from "@/stores/Status.js";
import {
    AimOutlined,
    AppstoreOutlined,
    SettingOutlined,
    HeatMapOutlined,
    AppstoreAddOutlined,
    DeleteOutlined,
    UploadOutlined,
    ArrowRightOutlined,
} from "@ant-design/icons-vue";
const selectedKeys = ref(["2"]);
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
            [
                getItem("Add Cargo", "Add Cargo", () => h(AppstoreAddOutlined)),
                getItem("Delete Cargo", "Delete Cargo", () =>
                    h(DeleteOutlined)
                ),
                getItem("Edit Cargo", "Edit Cargo", () => h(UploadOutlined)),
            ],
            "group"
        ),
        getItem(
            "Item 2",
            "g2",
            null,
            [
                getItem("Heatmap", "Heatmap", () => h(HeatMapOutlined)),
            ],
            "group"
        ),
    ]),
    getItem("Navigation Two", "sub2", () => h(AppstoreOutlined), [
        getItem("Add Route", "Add Route", () => h(AppstoreAddOutlined)),
        getItem("View Route", "View Route", () => h(ArrowRightOutlined)),
    ]),

]);
const handleClick = (e) => {
    console.log("click side menu", e.key);

    const AddCargoesMode = AddCargoesStatus();
    const DeleteCargoesMode = DeleteCargoesStatus();
    const UpdateCargoesMode = UpdateCargoesStatus();
    const HeatmapMode = DisplayHeatmap();
    const AddRouteMode = Cargo_AddRouteStatus();
    const ViewRouteMode = Cargo_ViewRouteStatus();

    if (e.key == "Add Cargo") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            AddCargoesMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            AddCargoesMode.updateStatus(true);
        }
    } else {
        AddCargoesMode.updateStatus(false);
    }

    if (e.key == "Delete Cargo") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            DeleteCargoesMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            DeleteCargoesMode.updateStatus(true);
        }
    } else {
        DeleteCargoesMode.updateStatus(false);
    }

    if (e.key == "Edit Cargo") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            UpdateCargoesMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            UpdateCargoesMode.updateStatus(true);
            console.log("Edit Cargo Mode", UpdateCargoesMode.status);
        }
    } else {
        UpdateCargoesMode.updateStatus(false);
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

    //handle click add route
    if (e.key == "Add Route") {
        if (selectedKeys.value.includes(e.key)) {
            selectedKeys.value = [];
            AddRouteMode.updateStatus(false);
        } else {
            selectedKeys.value = [e.key];
            AddRouteMode.updateStatus(true);
        }
    } else {
        AddRouteMode.updateStatus(false);
    }

    //handle click view route
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
