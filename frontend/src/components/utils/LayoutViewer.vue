<template>
  <div id="layoutViewer">
    <!-- Display a layout in a graphical way -->
    <div v-if="layout.length === 0">No layout to display</div>

    <div
      class="component"
      v-for="component in layout"
      :key="component.id"
      :style="{
        left: (component.x / analysisMaxX) * 100 + 1.5 + '%',
        top: (component.y / lowestY) * 100 + 2 + '%',
        width: (component.width / analysisMaxX) * 100 - 4 + '%',
        height: (component.height / lowestY) * 100 - 3 + '%',
        'background-image':
          'url(' +
          require(`@/components/debiai/statistics/dataAnalysis/widgets/${component.key}/icon.png`) +
          ')',
      }"
    >
      <div class="content">
        {{ component.key }}
      </div>
    </div>
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
  computed: {
    lowestY() {
      let lowestY = 0;
      this.layout.forEach((component) => {
        if (component.y + component.height > lowestY) {
          lowestY = component.y + component.height;
        }
      });
      return lowestY + 0.5;
    },
  },
};
</script>

<style scoped>
#layoutViewer {
  /* text-align: left; */
  padding: 5px;
  margin: 5px;
  border: 1px solid black;
  border-radius: 3px;
  width: 150px;
  height: 150px;
  position: relative;
  display: flex;
  align-items: center;
}
.component {
  cursor: pointer;
  background-color: white;
  border: 1px solid black;
  border-radius: 3px;
  width: 50px;
  height: 50px;
  position: absolute;

  display: flex;
  justify-content: center;
  align-items: center;

  border-top: 5px solid rgb(121, 121, 121);
  background-size: contain;
  background-position: center;
}

.component .content {
  display: none;
  background-color: white;
  border: 1px solid black;
  border-radius: 3px;
  z-index: 1;
  padding: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.component:hover .content {
  display: block;
}
</style>
