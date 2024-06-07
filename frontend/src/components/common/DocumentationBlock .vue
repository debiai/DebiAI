<template>
  <div id="DocumentationBlock">
    <div id="questionMark">
      <b
        id="i"
        ref="i"
        @mouseover="showTooltip"
        @mouseleave="hideTooltip"
        >i</b
      >
    </div>
    <transition name="fade">
      <p
        id="docBlock"
        ref="docBlock"
        @mouseover="showTooltip"
        @mouseleave="hideTooltip"
        v-show="show"
      >
        <slot />
      </p>
    </transition>
  </div>
</template>

<script>
export default {
  name: "DocumentationBlock",
  data() {
    return {
      show: false,
    };
  },
  methods: {
    showTooltip() {
      this.show = true;
      this.$nextTick(this.adjustDockBlockPosition);
      if (this.offTimeout) clearTimeout(this.offTimeout);
    },
    hideTooltip() {
      if (this.offTimeout) clearTimeout(this.offTimeout);

      this.offTimeout = setTimeout(() => {
        this.show = false;
      }, 100);
    },
    adjustDockBlockPosition(previousPosition) {
      if (!this.show) return;

      const docBlock = this.$refs.docBlock;
      const docBlockRect = docBlock.getBoundingClientRect();
      const i = this.$refs.i;
      const iRect = i.getBoundingClientRect();
      let top = iRect.top + iRect.height;
      let left = iRect.left;

      // Check if the tooltip is out of the screen
      if (left + docBlockRect.width > window.innerWidth) {
        left = iRect.right - docBlockRect.width;
      }

      if (top + docBlockRect.height > window.innerHeight) {
        top = iRect.top - docBlockRect.height;
      }

      // Offset by the scroll position
      top += window.scrollY;
      left += window.scrollX;

      // Set the position
      docBlock.style.top = `${top}px`;
      docBlock.style.left = `${left}px`;

      // Recursively call the function until the position is stable
      if (!previousPosition || previousPosition.top !== top || previousPosition.left !== left) {
        this.$nextTick(() => this.adjustDockBlockPosition({ top, left }));
      }
    },
  },
};
</script>

<style scoped>
#questionMark #i {
  margin: 0 7px 0 7px;
  cursor: pointer;
  border: solid 1px var(--blueDark);
  color: var(--blueDark);
  background-color: rgb(245, 254, 255);
  border-radius: 100%;
  width: 18px;
  height: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 3px;
  text-decoration: none;
  font-size: initial;
}

#docBlock {
  position: absolute;
  padding: 20px;
  margin: 0px;
  border: solid 1px var(--blueDark);
  border-radius: 3px;
  color: var(--blueDark);
  background-color: rgb(213, 251, 255);
  text-align: left;
  z-index: 1000;
  font-size: initial;
  text-decoration: none;
  align-self: flex-start;
  font-weight: normal;
  box-shadow: 0px 0px 25px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  max-height: 500px;
  overflow-y: auto;
}
</style>

<style>
/* Style for the slot */
#docBlock * {
  border-color: var(--blueDark);
}
</style>
