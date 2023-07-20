<template>
  <div
    id="LoadingAnimation"
    :class="classObject"
  >
    <div id="text">
      <slot />
    </div>
    <div id="animation"><span></span><span></span><span></span></div>
  </div>
</template>

<script>
export default {
  name: "LoadingAnimation",
  props: {
    center: { type: Boolean, default: false },
  },
  computed: {
    classObject() {
      return {
        center: this.center,
      };
    },
  },
};
</script>

<style lang="scss" scoped>
#LoadingAnimation {
  margin-left: 5px;

  #animation {
    text-align: center;
    span {
      animation-name: blink;
      animation-duration: 1.4s;
      animation-iteration-count: infinite;
      animation-fill-mode: both;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      background-color: cadetblue;
      display: inline-block;
      margin-right: 2.5px;
      margin-left: 2.5px;

      &:nth-child(2) {
        animation-delay: 0.2s;
      }

      &:nth-child(3) {
        animation-delay: 0.4s;
      }
    }
  }

  #text {
    color: cadetblue;
    text-align: center;
    font-weight: bold;
  }

  &.center {
    position: absolute;
    top: 25%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

/* Loading Anim */
@keyframes blink {
  0% {
    opacity: 0.2;
  }

  20% {
    opacity: 1;
  }

  100% {
    opacity: 0.2;
  }
}
</style>
