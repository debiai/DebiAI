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
      component: () => import("../components/debiai/exploration/ExplorationMode"),
    },

    // {
    //   path: "/exploration",
    //   component: () => import("../components/debiai/exploration/ExplorationMode"),
    //   children: [
    //     {
    //       name: "columnSelection",
    //       path: "/columnSelection",
    //       component: () =>
    //         import("../components/debiai/exploration/columnSelection/ColumnSelection"),
    //     },
    //     {
    //       name: "aggregation",
    //       path: "/aggregation",
    //       component: () => import("../components/debiai/exploration/aggregation/Aggregation"),
    //     },
    //     {
    //       name: "filtering",
    //       path: "/filtering",
    //       component: () => import("../components/debiai/exploration/filtering/Filtering"),
    //     },
    //   ],
    // },
  ],
});
const DEFAULT_TITLE = "DebiAI";
router.beforeEach((to, from, next) => {
  document.title = to.query.projectId || to.params.projectId || DEFAULT_TITLE;
  next();
});

export default router;
