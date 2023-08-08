<template>
  <!-- SideBar -->
  <div
    id="SideBar"
    @mouseover="mouseHover = true"
    @mouseleave="mouseHover = false"
  >
    <div
      class="section"
      v-for="section in menuList"
      :key="section.name"
    >
      <div
        :class="'head' + (openedSection === section.name ? ' open' : '')"
        @click="
          openedSection == section.name ? (openedSection = null) : (openedSection = section.name)
        "
      >
        <!-- The visible part when the mouse is not hovering the sidebar -->
        <div class="icon">
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="18"
            height="18"
            style="margin-right: 3px"
          />
        </div>

        <!-- The opening part when the mouse is hovering the sidebar -->
        <transition name="fade">
          <div
            v-show="mouseHover"
            class="side"
          >
            <div class="name">
              {{ section.name }}
            </div>

            <div class="arrow">
              <inline-svg
                id="arrow"
                :src="require('@/assets/svg/arrowRight.svg')"
                width="10"
                height="10"
              />
            </div>
          </div>
        </transition>
      </div>

      <!-- The opening part when you select a section -->
      <transition name="scale">
        <div
          class="subsections"
          v-show="openedSection === section.name"
        >
          <div
            class="subSection"
            v-for="subSection in section.menuList"
            :key="subSection.name"
          >
            <div class="name">{{ subSection.name }}</div>
            <!-- <div class="subSectionDescription">{{ subSection.description }}</div> -->
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    menuList: {
      type: Array,
      default: () => [],
      // {
      //     name: "selections",
      //     icon: "loop",
      //     menuList: [
      //         {
      //             name: "Open a selection",
      //             description: "Open a new analysis with another selection",
      //             callback: () => {}
      //         },
      //         ...
      //     ]
      // }
    },
  },

  data() {
    return {
      mouseHover: false,

      openedSection: null,
    };
  },

  watch: {
    mouseHover() {
      if (!this.mouseHover) {
        this.openedSection = null;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#SideBar {
  width: 80px;
  height: 100%;
  position: fixed;
  top: 60px;
  left: 0px;
  z-index: 0;

  background: #e8e8e8;
  border-right: #bab9bf 2px solid;

  transition: all 0.3s;
  overflow: hidden;

  .section {
    font-size: 14px;

    .head {
      padding: 10px 10px 10px 30px;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      gap: 10px;
      height: 40px;

      padding-right: 20px;
      color: #494949;
      transition: padding 0.3s ease-out;
      cursor: pointer;

      &:hover {
        background: #d8d8d8;
      }

      .side {
        flex: 1;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        height: 40px;

        .name {
          white-space: nowrap;
          font-weight: 700;
        }

        .arrow {
          transition: transform 0.1s ease-out;
          transform: rotate(90deg);
        }
      }

      &.open {
        .arrow {
          transform: rotate(-90deg);
        }
      }
    }

    .subsections {
      display: flex;
      flex-direction: column;

      .subSection {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
        height: 20px;

        padding: 10px 10px 10px 50px;
        cursor: pointer;

        &:hover {
          background: #d8d8d8;
          .name {
            color: black;
            text-decoration: underline;
          }
        }

        .name {
          white-space: nowrap;
        }
      }
    }
  }

  &:hover {
    // Open the sidebar
    width: 300px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);

    .section {
      .head {
        padding-left: 20px;
      }
    }
  }
}
</style>
