import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

let router = new Router({
  routes: [
    {
      name: 'frontPage',
      path: '/',
      component: () => import("../components/debiai/frontpage/FrontPage"),
    },

    // === Project
    {
      name: 'project',
      path: '/dataprovider/:dataProviderId/project/:projectId',
      component: () => import("../components/debiai/project/Project")
    },


    // === Statistics
    {
      path: '/statistics',
      component: () => import("../components/debiai/statistics/Statistics"),
      children: [
        {
          name: 'dataAnalysis',
          path: '/dataAnalysis',
          component: () => import("../components/debiai/statistics/dataAnalysis/DataAnalysis"),
        }
      ]
    },

  ],
})
const DEFAULT_TITLE = "DebiAI"
router.beforeEach((to, from, next) => {
  document.title = to.query.projectId || to.params.projectId || DEFAULT_TITLE;
  next()
});

export default router;