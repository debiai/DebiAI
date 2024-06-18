<template>
  <div :class="collapsibleClass">
    <!-- Header -->
    <div
      :class="headerClass"
      @click="isOpen = !isOpen"
      :title="headerTitle"
    >
      <inline-svg
        id="arrow"
        :src="require('@/assets/svg/arrowRight.svg')"
        width="10"
        height="10"
      />

      <div
        :class="colorTagClass"
        v-if="headerColor"
      >
        <span v-if="headerColor === 'green'">✔</span>
        <span v-if="headerColor === 'blue'">i</span>
        <span v-if="headerColor === 'red'">✖</span>
      </div>
      <slot name="header"></slot>
    </div>

    <!-- Content -->
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
      default: null,
    },
    headerTitle: {
      type: String,
      default: "",
    },
    simple: {
      // Made to place a column in the header
      type: Boolean,
      default: false,
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
        simple: this.simple,
      };
    },
    headerClass() {
      return {
        header: true,
        open: this.isOpen,
      };
    },
    colorTagClass() {
      return {
        colorTag: true,
        [this.headerColor]: true,
      };
    },
  },
  watch: {
    isOpen() {
      // Scroll to the bottom of the collapsible when it is opened
      if (this.isOpen && !this.open) {
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
  border: 1px solid var(--greyDark);

  .header {
    padding: 9px 12px;
    min-height: 20px;
    border-bottom: 1px solid var(--greyDark);

    cursor: pointer;
    background-color: var(--greyLight);
    color: var(--fontColorLight);
    display: flex;
    align-items: center;
    gap: 10px;

    * {
      display: flex;
      align-items: center;
      margin: 0;
    }

    #arrow {
      transform: rotate(0deg);
      transform: translateY(-2px);
      transition: transform 0.2s ease-out;
    }

    &.open {
      #arrow {
        transform: rotate(90deg);
      }
    }

    // Header color
    .colorTag {
      width: 20px;
      height: 19px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 50px;
      color: white;
      font-size: 0.8em;
      transition: background-color 0.2s;
      &.green {
        background-color: var(--success);
      }
      &.blue {
        background-color: var(--success);
      }
      &.red {
        background-color: var(--danger);
      }
    }
  }

  &.simple {
    border: none;

    .header {
      padding: 0 0 0 10px;
      background-color: white;
      border: none;
      gap: 0;
    }
    .body {
      padding-left: 20px;
      border: none;
    }
  }
}
</style>
