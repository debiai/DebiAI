<template>
  <div id="app">
    <div id="content">
      <Messenger />
      <Loading />
      <router-view />
    </div>
  </div>
</template>

<script>
import "./assets/css/main.scss";
import "./assets/css/imported.scss";
import Messenger from "./components/utils/Messenger.vue";
import Loading from "./components/utils/Loading";

export default {
  name: "App",
  components: {
    Messenger,
    Loading,
  },
};
</script>

<style>
#app {
  height: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--fontColor);
}
#content {
  height: 100%;
}
</style>
