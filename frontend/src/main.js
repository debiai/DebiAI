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
Vue.prototype.$API_DEBIAI_URL = config.API_DEBIAI_URL;
Vue.prototype.$API_DATA_URL = config.API_DATA_URL;
Vue.prototype.$API_ALGO_URL = config.API_ALGO_URL;

// Custom directive
Vue.directive("focus", { inserted: (el) => el.focus() });

// New Vue
new Vue({
  el: "#app",
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
