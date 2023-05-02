<template>
  <div id="layoutViewer">
    <!-- Display a layout in a graphical way -->
    <!-- {{ layout }} -->
    <div
      class="component"
      v-for="component in layout"
      :key="component.id"
      :style="{
        gridColumn: component.x + 1,
        gridRow: component.y + 1,
        width: component.width * 100 + '%',
        height: component.height * 100 + '%',
      }"
    />
      <!-- {{ component.key }} -->
      <!-- {{ component.layout.x }} -->
      <!-- {{ component.layout.y }} -->
      <!-- {{ component.layout.width }} -->
      <!-- {{ component.layout.height }} -->
    <!-- </div> -->
  </div>
</template>

<script>
export default {
  name: "Layouts",
  components: {},
  props: {
    layout: { type: Array, required: true },
  },
  data: () => {
    return {
      analysisMaxX: 12,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>
#layoutViewer {
  /* text-align: left; */
  padding: 5px;
  margin: 5px;
  border: 1px solid black;
  border-radius: 3px;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  grid-template-rows: repeat(12, 1fr);
  gap: 0.5px 0.5px;
  width: 100px;
  height: 100px;
}
.component {
  background-color: rgb(190, 250, 250);
  border: 1px solid black;
  border-radius: 3px;
}
</style>
