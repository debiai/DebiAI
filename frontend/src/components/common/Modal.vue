<template>
  <div
    id="modal"
    @click.stop="outsideClick"
  >
    <div id="Panel">
      <slot />
    </div>

    <div id="errors">
      <!-- Errors -->
      <div
        v-for="(error, index) in errorMessages"
        :key="index"
      >
        <transition name="fade">
          <div
            class="error"
            v-if="error"
          >
            {{ error }}
          </div>
        </transition>
      </div>

      <!-- Warnings -->
      <div
        v-for="(warning, index) in warningMessages"
        :key="index + warningMessages.length"
      >
        <transition name="fade">
          <div
            class="error warning"
            v-if="warning"
          >
            {{ warning }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Modal",
  props: {
    errorMessages: { type: Array, default: () => [] },
    warningMessages: { type: Array, default: () => [] },
    preventBodyScroll: { type: Boolean, default: true },
  },
  mounted() {
    // When the modal is opened, we want to disable scrolling on the body
    const bodyOverflowStyle = document.body.style.overflow;
    if (bodyOverflowStyle !== "hidden" && this.preventBodyScroll) {
      document.body.style.overflow = "hidden";
      this.preventBodyScroll = true;
      // The preventBodyScroll variable is used in the beforeDestroy hook
      // Useful in case of recursive modals
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

<style lang="scss" scoped>
#modal {
  z-index: 5;
  position: fixed;
  height: 100vh;
  width: 100vw;
  left: 0%;
  top: 0%;
  background-color: rgba(0, 0, 0, 0.4);

  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  backdrop-filter: blur(1px);

  animation: fadeIn 0.1s;

  &:hover {
    cursor: pointer;
  }
}

#Panel {
  max-height: 90vh;
  max-width: 90vw;
  padding: 30px;
  background-color: white;
  border-radius: 4px;
  overflow: auto;

  &:hover {
    cursor: default;
  }
}

#errors {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .error {
    font-weight: bold;
    border-radius: 10px;
    padding: 5px;
    margin: 10px;
  }

  .warning {
    background-color: var(--warning);
    color: black;
  }
}
</style>
