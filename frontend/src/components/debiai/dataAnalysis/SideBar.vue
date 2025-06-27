<template>
  <!-- SideBar -->
  <div
    id="SideBar"
    @mouseover="mouseHover = true"
    @mouseleave="mouseHover = false"
  >
    <div
      class="section"
      v-for="section in menuSectionsWithoutEmptySubsections"
      :key="section.name"
    >
      <!-- Section icon and name -->
      <div
        :class="'head' + (openedSections[section.name] ? ' open' : '')"
        @click="selectSection(section.name)"
      >
        <!-- The visible part when the mouse is not hovering the sidebar -->
        <div class="icon">
          <inline-svg
            :src="require('@/assets/svg/' + section.icon + '.svg')"
            width="22"
            height="22"
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

      <!-- Subsections, the opening part when you select a section -->
      <transition name="scale">
        <div
          class="subsections"
          v-show="openedSections[section.name] && mouseHover"
        >
          <div
            class="subSection"
            v-for="subSection in section.menuList"
            :key="subSection.name"
            @click="subSection.callback()"
          >
            <div class="name">{{ subSection.name }}</div>
            <div class="description">{{ subSection.description }}</div>
          </div>
        </div>
      </transition>
    </div>

    <div
      class="section"
      id="documentation"
    >
      <!-- Section icon and name -->
      <div
        class="head"
        @click="openDocumentation()"
      >
        <!-- The visible part when the mouse is not hovering the sidebar -->
        <div class="icon">
          <img
            src="@/assets/images/Question.png"
            alt="Documentation"
            height="30"
          />
        </div>
        <!-- The opening part when the mouse is hovering the sidebar -->
        <transition name="fade">
          <div
            v-show="mouseHover"
            class="side"
          >
            <div class="name">Documentation</div>
          </div>
        </transition>
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
      //             callback: () => {},
      //             modes: ["analysis", "exploration", ...],
      //         },
      //         ...
      //     ]
      // }
    },
    data: {
      type: Object,
      default: () => ({}),
      // {
      //     mode: "...",
      //     ...
      // }
    },
  },

  data() {
    return {
      mouseHover: false,

      openedSections: {}, // { sectionName: true/false }
    };
  },

  created() {
    // Add a menu section property to track when opened
    this.menuList.forEach((section) => {
      this.openedSections[section.name] = false;
    });

    // Filter the subsections based on the current mode
    this.menuList.forEach((section) => {
      for (const subSection of section.menuList) {
        if (subSection.modes) {
          // Check if the current mode is in the allowed modes
          if (!subSection.modes.includes(this.data.mode)) {
            section.menuList = section.menuList.filter((item) => item.name !== subSection.name);
          }
        }
      }
    });
  },

  methods: {
    selectSection(sectionName) {
      this.openedSections[sectionName] = !this.openedSections[sectionName];
      this.$forceUpdate();
    },
    openDocumentation() {
      window.open("https://debiai.irt-systemx.fr/dashboard/#analysis-page", "_blank");
    },
  },
  computed: {
    menuSectionsWithoutEmptySubsections() {
      return this.menuList.filter((section) => {
        // Filter out sections with no subsections
        return section.menuList && section.menuList.length > 0;
      });
    },
  },

  watch: {
    mouseHover() {
      if (!this.mouseHover) {
        // Close all sections
        this.menuList.forEach((section) => {
          this.openedSections[section.name] = false;
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#SideBar {
  width: 60px;
  height: calc(100vh - 80px);
  position: fixed;
  top: 60px;
  left: 0px;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;

  background: var(--grey);
  border-right: var(--greyDark) 2px solid;
  padding-top: 20px;

  transition: all 0.3s;
  overflow-x: hidden;

  .section {
    font-size: 14px;

    .head {
      padding: 10px 10px 10px 20px;
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
      gap: 10px;
      height: 40px;

      color: var(--fontColor);
      transition: all 0.1s ease-out;
      cursor: pointer;

      &:hover {
        background: var(--grey);
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
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;

        padding: 10px 10px 10px 50px;
        cursor: pointer;

        &:hover {
          background: var(--grey);
        }

        .name {
          white-space: nowrap;
        }

        .description {
          text-align: left;
          font-size: 0.9em;
          color: var(--fontColorLight);
          width: 200px;
        }
      }
    }
  }

  #documentation {
    margin-top: auto;

    .head {
      padding-left: 14px;
    }
  }

  &:hover {
    // Open the sidebar
    width: 300px;
    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
    background: var(--greyLight);
  }
}
</style>
