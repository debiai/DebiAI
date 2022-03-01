<template>
  <div id="modal">
    <div id="pannel">
      <slot/>
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
  data() {
    return {};
  }
};
</script>

<style>
#modal {
  z-index: 5;
  position: fixed;
  height: 100vh;
  width: 100vw;
  left: 0%;
  top: 0%;
  background-color: rgba(0, 0, 0, 0.5);

  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

#pannel {
  max-height: 90vh;
  max-width: 90vw;
  padding: 3vh;
  background-color: rgb(250, 250, 250);
  border: solid#f8f9fa;
  border-radius: 1vh;
  overflow: auto;
}
</style>