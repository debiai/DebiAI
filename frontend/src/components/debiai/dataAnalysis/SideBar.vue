<template>
  <div id="SideBar">
    <div
      class="section"
      v-for="section in menuList"
      :key="section.name"
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
};
</script>

<style lang="scss" scoped>
#SideBar {
  width: 100px;
  height: 100%;
  position: fixed;
  top: 62px;
  left: 0px;
  z-index: 1;

  background: #e8e8e8;
  border-right: #bab9bf 2px solid;

  transition: width 0.3s;

  &:hover {
    width: 400px;
  }
}
</style>
