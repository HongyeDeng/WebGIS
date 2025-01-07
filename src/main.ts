import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Antd from "ant-design-vue";
import { createPinia } from "pinia";
import "ant-design-vue/dist/reset.css";

const piana = createPinia();
createApp(App).use(piana).use(Antd).use(router).mount("#app");
