<template>
  <div>
    <!-- Background -->
    <transition name="fade">
      <div
        id="background"
        v-show="mouseHover"
      />
    </transition>

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
        <div class="side">
          <!-- The visible part when the mouse is not hovering the sidebar -->
          <div class="svg">
            <inline-svg
              :src="require('@/assets/svg/filter.svg')"
              width="18"
              height="18"
              style="margin-right: 3px"
            />
          </div>

          <!-- The opening part when the mouse is hovering the sidebar -->
          <transition name="scale">
            <div
              class="name"
              v-show="mouseHover"
            >
              {{ section.name }}
            </div>
          </transition>
        </div>

        <!-- The opening part when the mouse is hovering the sidebar -->
        <!-- <transition name="fade">
          <div
            class="subsections"
            v-show="mouseHover"
          >
            <div
              class="subSection"
              v-for="subSection in section.menuList"
              :key="subSection.name"
            >
              <div class="subSectionName">{{ subSection.name }}</div>
              <div class="subSectionDescription">{{ subSection.description }}</div>
            </div>
          </div>
        </transition> -->
      </div>
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
    };
  },
};
</script>

<style lang="scss" scoped>
#background {
  width: 100%;
  height: 100%;
  position: fixed;
  top: 62px;
  left: 0px;
  z-index: 0;

  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(1px);
}

#SideBar {
  width: 80px;
  height: 100%;
  position: fixed;
  top: 62px;
  left: 0px;
  z-index: 0;

  background: #e8e8e8;
  border-right: #bab9bf 2px solid;

  transition: all 0.3s;

  .section {
    padding: 10px 10px;
    font-size: 14px;

    .side {
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      gap: 10px;
      height: 40px;

      color: #494949;
    }
  }

  &:hover {
    width: 400px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);

    .section {
      .side {
      }
    }
  }
}
</style>
