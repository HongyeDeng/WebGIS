<template>
  <div id="HeaderGlobal">
    <a-menu
      v-model:selectedKeys="current"
      mode="horizontal"
      :items="items"
      id="MenuGlobal"
    />
  </div>
</template>
<script lang="ts" setup>
import { h, ref, watch } from "vue";
import {
  SettingOutlined,
  DropboxOutlined,
  CarOutlined,
  FormOutlined,
  GithubOutlined,
} from "@ant-design/icons-vue";
import { MenuProps } from "ant-design-vue";
import { Button } from "ant-design-vue";
import { PageIndex } from "@/stores/Status.js";
import { storeToRefs } from "pinia";

const current = ref<string[]>(["Orders"]);
const items = ref<MenuProps["items"]>([
  {
    key: "Cargoes",
    icon: () => h(DropboxOutlined),
    label: "Cargoes",
    title: "Cargoes",
  },
  {
    key: "Trucks",
    icon: () => h(CarOutlined),
    label: "Trucks",
    title: "Trucks",
  },
  {
    key: "Orders",
    icon: () => h(FormOutlined),
    label: "Orders",
    title: "Oresers",
  },
  {
    key: "Order",
    icon: () => h(GithubOutlined),
    label: h(
      'a',
      {
        href: 'https://github.com/HongyeDeng',
        target: '_blank',
      },
      'GitHubLink',
    ),
    title: "GitHubLink",
  },
]);

watch(current, (val) => {
  const Page = PageIndex();
  Page.updateIndex(current.value[0]);
  console.log("Change the add Page To:", current.value[0]);
});
</script>

<style scoped>
#HeaderGlobal {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 64px;
  left: 0px;
  right: 0px;
  width: 100%;
}

#MenuGlobal {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 64px;
  left: 0px;
  right: 0px;
  background-color: #7dbcea;
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  padding: 0px 50px;
  width: 100%;
  justify-content: space-evenly;
}
</style>
