import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

let router = new Router({
  routes: [
    {
      name: "frontPage",
      path: "/",
      component: () => import("../components/debiai/frontpage/FrontPage"),
    },
    {
      name: "legal",
      path: "/legal",
      component: () => import("../components/debiai/frontpage/legal/Legal"),
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
  ],
});
const DEFAULT_TITLE = "DebiAI";
router.beforeEach((to, from, next) => {
  document.title = to.query.projectId || to.params.projectId || DEFAULT_TITLE;
  next();
});

export default router;
