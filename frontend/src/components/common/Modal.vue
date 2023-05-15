<template>
  <div
    id="modal"
    @click.stop="outsideClick"
  >
    <div id="pannel">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
  data() {
    return {};
  },
  mounted() {
    // When the modal is opened, we want to disable scrolling on the body
    const bodyOverflowStyle = document.body.style.overflow;
    if (bodyOverflowStyle !== "hidden") {
      document.body.style.overflow = "hidden";
      this.preventBodyScroll = true;
      // The preventBodyScroll variable is used in the beforeDestroy hook
      // Usefull in case of recursive modals
      // (the beforeDestroy would be called before the last modal is closed)
    }
  },
  methods: {
    outsideClick(e) {
      if (e.target.id === "modal") this.$emit("close");
    },
  },
  beforeDestroy() {
    // When the modal is closed, we want to enable scrolling on the body
    if (this.preventBodyScroll) document.body.style.overflow = "auto";
  },
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
  backdrop-filter: blur(1px);

  animation: fadeIn 0.1s;
}
#modal:hover {
  cursor: pointer;
}

#pannel {
  max-height: 90vh;
  max-width: 90vw;
  padding: 3vh;
  background-color: rgb(250, 250, 250);
  border-radius: 1vh;
  overflow: auto;
}

#pannel:hover {
  cursor: default;
}
</style>
