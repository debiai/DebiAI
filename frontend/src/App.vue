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
import "./assets/css/main.css";
import "./assets/css/imported.css";
import Messenger from "./components/utils/Messenger.vue";
import Loading from "./components/utils/Loading";

export default {
  name: "App",
  components: {
    Messenger,
    Loading,
  }
};
</script>

<style>
#app {
  height: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#content {
  height: 100%;
}
</style>
