<template>
  <div
    id="menu"
    :style="getStyles"
    :class="{ flipVertically: flipVertically }"
  >
    <!-- Dropdown menu -->
    <div
      v-for="(item, index) in availableMenuItems"
      :key="index"
      @click="!item.disabled && item.action ? item.action() : ''"
    >
      <div
        v-if="item.name !== 'separator'"
        :class="'menu-item' + (item.disabled ? ' disabled' : '')"
      >
        <div
          class="icon"
          v-if="item.icon"
        >
          <inline-svg
            :src="require('@/assets/svg/' + item.icon + '.svg')"
            width="14"
            height="14"
            fill="var(--fontColor))"
            stroke="var(--fontColor)"
          />
        </div>
        <div class="dropdownMenuName">
          {{ item.name }}
        </div>
      </div>
      <div
        v-else
        class="separator"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MenuBtn",
  props: {
    menu: {
      type: Array,
      required: true,
    },
    offset: {
      type: Object,
      default: () => {
        return {
          x: 0,
          y: 0,
        };
      },
    },
    position: {
      type: Object,
      default: () => {
        return {
          x: null,
          y: null,
        };
      },
    },
    flipVertically: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {};
  },
  mounted() {
    setTimeout(() => {
      // Close dropdown menu when clicked outside
      window.addEventListener("click", this.closeMenu);
    }, 100);
  },

  methods: {
    closeMenu() {
      this.$emit("close");
    },
  },

  computed: {
    availableMenuItems() {
      return this.menu.filter((item) => item.available !== false);
    },
    getStyles() {
      if (this.position.x === null || this.position.y === null) {
        return {
          inset: `${this.offset.y}px ${this.offset.x}px auto auto`,
        };
      } else {
        return {
          left: `${this.position.x}px`,
          top: `${this.position.y}px`,
        };
      }
    },
  },

  beforeDestroy() {
    window.removeEventListener("click", this.closeMenu);
  },
};
</script>

<style lang="scss" scoped>
#menu {
  position: absolute;
  min-width: 150px;
  z-index: 10000000;

  &.flipVertically {
    // Flip vertically
    transform: translateY(-100%);
  }

  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  background-color: #fff;
  border-radius: 5px;

  .menu-item {
    padding: 10px 18px;
    cursor: pointer;
    transition: background-color 0.1s ease-in-out;
    text-align: left;

    &.disabled {
      cursor: not-allowed;

      .icon,
      .dropdownMenuName {
        opacity: 0.5;
      }
    }

    &:hover {
      background-color: var(--grey);
    }

    display: flex;
    align-items: center;
    gap: 10px;

    .dropdownMenuName {
      white-space: nowrap;
      user-select: none;
    }
  }

  .separator {
    height: 1.3px;
    background: var(--grey);
    margin: 0px 0;
  }
}
</style>
