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
  props: {},
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
};
</script>

<style lang="scss" scoped>
.collapsible {
  border: 1px solid #00000027;
  border-radius: 4px;

  .header {
    padding: 10px;
    border-bottom: 1px solid #00000027;
    cursor: pointer;
    background-color: #0000000d;
    color: #0000008a;
    display: flex;
    justify-content: space-between;

    // Harrow at the right of the header
    &:after {
      content: "▼";
    }
    &.open:after {
      content: "▲";
    }
  }
  .body {
    padding: 5px;
    border-bottom: 1px solid #00000027;
    border-radius: 0 0 4px 4px;
  }
}
</style>
