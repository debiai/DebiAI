import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

// Common Components
import commonComponents from "./components/common";
commonComponents.forEach((component) => {
  Vue.component(component.name, component);
});

// Common Services
import backendDialog from "./services/backendDialog";
import explorationDialog from "./services/exploration/explorationDialog";
import services from "./services/services";
Vue.prototype.$backendDialog = backendDialog;
Vue.prototype.$explorationDialog = explorationDialog;
Vue.prototype.$services = services;

// Common Data
import config from "../config";
Vue.prototype.$API_URL = config.API_URL;

// Custom directive
Vue.directive("focus", { inserted: (el) => el.focus() });

// New Vue
new Vue({
  el: "#app",
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
