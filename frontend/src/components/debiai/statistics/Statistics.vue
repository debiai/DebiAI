<template>
  <div id="statistics">
    <div id="header">
      <!-- DebiAI title to go to the main menu -->
      <h1>
        <router-link id="debiaiMenuLogo" :to="'/project/' + $store.state.ProjectPage.projectId">&#8592;
          <img src="../../../../src/assets/images/DebiAI.png" alt="DebiAI" height="48" />
        </router-link>
      </h1>
      <div style="flex: 1"></div>
      <h1 id="title2">Statistics</h1>
      <div style="flex: 1"></div>

      <!-- IRT Logo -->
      <img id="title3" src="../../../../src/assets/images/SystemX.png" alt="SystemX" height="38" />
    </div>
    <div id="content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: "Statistics",
  components: {},
  data: () => {
    return {};
  },
  mounted() { },
  methods: {},
  computed: {},
};
</script>

<style scoped>
#statistics {
  height: 100%;
  display: flex;
  flex-direction: column;
}


#header {
  display: flex;
  align-items: center;
  color: white;
  padding: 2px;
  background-color: var(--primary);
}

#debiaiMenuLogo {
  display: flex;
  justify-content: center;
  align-items: center;
  background: red;
  color: #fff;
  text-decoration: none;
  background: none;
}

#title2 {
  align-self: center;
}

#title3 {
  align-self: center;
  padding-top: 9px;
}

#content {
  flex: 1;
  height: 100%;
}
</style>
