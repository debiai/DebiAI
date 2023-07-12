<template>
  <div id="ExplorationMode">
    <div id="header">
      <!-- DebiAI title to go to the main menu -->
      <h1>
        <router-link
          id="debiaiMenuLogo"
          :to="
            '/dataprovider/' +
            $store.state.ProjectPage.dataProviderId +
            '/project/' +
            $store.state.ProjectPage.projectId
          "
          >&#8592;
          <img
            src="../../../../src/assets/images/DebiAI.png"
            alt="DebiAI"
            height="48"
          />
        </router-link>
      </h1>
      <div style="flex: 1"></div>
      <h1 id="title2">Statistics</h1>
      <div style="flex: 1"></div>

      <!-- IRT Logo -->
      <img
        id="title3"
        src="../../../../src/assets/images/SystemX.png"
        alt="SystemX"
        height="38"
      />
    </div>
    <div id="content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style></style>
