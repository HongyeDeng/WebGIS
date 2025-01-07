<template>
  <div id="BasicLayout">
    <a-layout>
      <a-layout-header class="Header">
        <Header_Navigator />
      </a-layout-header>
      <a-layout>
        <!-- <a-layout-sider :style="siderStyle">
          Sider
        </a-layout-sider> -->
        <a-layout-content :style="contentStyle">
          <BasicMap />
        </a-layout-content>
      </a-layout>
      <a-layout-footer :style="footerStyle">Footer</a-layout-footer>
    </a-layout>
  </div>
</template>

<script lang="ts" setup>
import HelloWorld from "@/components/HelloWorld.vue";
import { ref } from "vue";
import BasicMap from "@/components/BasicMap.vue";
import SiderMenu from "@/components/SiderMenu.vue";
import Header_Navigator from "@/components/Header_Navigator.vue";
import type { CSSProperties } from "vue";
const headerStyle: CSSProperties = {
  textAlign: "center",
  color: "#fff",
  height: 64,
  paddingInline: 50,
  lineHeight: "64px",
  backgroundColor: "#7dbcea",
};

const contentStyle: CSSProperties = {
  textAlign: "center",
  minHeight: 120,
  lineHeight: "120px",
  color: "black",
  backgroundColor: "#108ee9",
  width: "100%",
  height: "100vh",
  overflow: "auto",
};

const siderStyle: CSSProperties = {
  textAlign: "center",
  lineHeight: "120px",
  color: "#fff",
  backgroundColor: "#3ba0e9",
  position: "relative",
  "padding-top": "64px",
};

const footerStyle: CSSProperties = {
  textAlign: "center",
  color: "#fff",
  backgroundColor: "#7dbcea",
  position: "relative",
};
</script>

<style scoped>
#BasicLayout {
  height: 100vh;
}
</style>
