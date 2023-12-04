<template>
  <div
    id="menu"
    :style="{
      inset: offset.y + 'px ' + offset.x + 'px auto auto',
    }"
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
          />
        </div>
        <div class="name">
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
    closeMenu(e) {
      this.$emit("close");
    },
  },

  computed: {
    availableMenuItems() {
      return this.menu.filter((item) => item.available !== false);
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
  z-index: 1;
  // inset: 0px 0px auto auto; This property is changed dynamically

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
      .name {
        opacity: 0.5;
      }
    }

    &:hover {
      background-color: var(--grey);
    }

    display: flex;
    align-items: center;
    gap: 10px;

    .name {
      white-space: nowrap;
      user-select: none;
    }
  }

  .separator {
    height: 1px;
    background: var(--grey);
    margin: 5px 0;
  }
}
</style>
