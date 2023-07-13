<template>
  <div :class="collapsibleClass">
    <div
      :class="headerClass"
      @click="isOpen = !isOpen"
    >
      <slot name="header"></slot>
    </div>
    <transition name="fade">
      <div
        class="body"
        v-show="isOpen"
      >
        <slot name="body"></slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "Collapsible",
  components: {},
  data: () => {
    return {
      isOpen: false,
    };
  },
  created() {},
  methods: {},
  computed: {
    collapsibleClass() {
      return {
        collapsible: true,
        open: this.isOpen,
      };
    },
    headerClass() {
      return {
        header: true,
        open: this.isOpen,
      };
    },
  },
  watch: {
    isOpen() {
      // Scroll to the bottom of the collapsible when it is opened
      if (this.isOpen) {
        this.$nextTick(() => {
          this.$el.scrollIntoView({ behavior: "smooth", block: "center" });
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.collapsible {
  border: 1px solid #00000027;
  border-radius: 4px;

  .header {
    padding: 9px 12px;
    min-height: 20px;
    border-bottom: 1px solid #00000027;
    cursor: pointer;
    background-color: #0000000d;
    color: #0000008a;
    display: flex;
    justify-content: space-between;

    * {
      display: flex;
      align-items: center;
      margin: 0;
      gap: 10px;
    }

    // Harrow at the right of the header
    &:after {
      content: "▼";
    }
    &.open:after {
      content: "▲";
    }
  }
  .body {
    border-bottom: 1px solid #00000027;
    border-radius: 0 0 4px 4px;
  }
}
</style>
