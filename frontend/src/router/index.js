import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

let router = new Router({
  routes: [
    // === Home
    {
      name: "frontPage",
      path: "/",
      component: () => import("../components/debiai/frontpage/FrontPage"),
    },
    // === Project
    {
      name: "project",
      path: "/dataprovider/:dataProviderId/project/:projectId",
      component: () => import("../components/debiai/project/Project"),
    },
    // === Data analysis
    {
      name: "dataAnalysis",
      path: "/dataAnalysis",
      component: () => import("../components/debiai/dataAnalysis/DataAnalysis"),
    },
    // === Exploration
    {
      name: "exploration",
      path: "/dataprovider/:dataProviderId/project/:projectId/exploration",
      component: () => import("../components/debiai/exploration/Explorations"),
    },
  ],
});

export default router;
