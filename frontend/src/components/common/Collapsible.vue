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
  props: {
    open: {
      type: Boolean,
      default: false,
    },
    headerColor: {
      type: String,
      default: "black",
    },
  },
  data: () => {
    return {
      isOpen: false,
    };
  },
  created() {
    this.isOpen = this.open;
  },
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
        [this.headerColor]: true,
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
      margin: 5px 5px 0 10px;
    }
    &.open:after {
      content: "▲";
      margin: 3px 5px 0 10px;
    }

    // Header color
    &:before {
      width: 20px;
      height: 20px;
      margin: 3px 10px 0 0;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 50px;
      color: white;
      font-size: 0.8em;
    }
    &.green:before {
      content: "✔";
      background-color: var(--success);
    }
    &.blue:before {
      content: "i";
      background-color: var(--success);
    }
    &.red:before {
      content: "✖";
      background-color: var(--danger);
    }
  }
  .body {
    border-bottom: 1px solid #00000027;
    border-radius: 0 0 4px 4px;
  }
}
</style>
