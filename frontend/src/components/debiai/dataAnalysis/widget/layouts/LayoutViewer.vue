<template>
  <div
    id="layoutViewer"
    :class="{ bigger }"
  >
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
          require(`@/components/debiai/dataAnalysis/widgets/${component.widgetKey}/icon.png`) +
          ')',
      }"
    >
      <div class="content">
        {{ component.widgetKey }}
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
    bigger: { type: Boolean, default: false },
  },
  data: () => {
    return {
      analysisMaxX: 12,
      analysisMinY: 8,
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
      return Math.max(lowestY + 0.5, this.analysisMinY);
    },
  },
};
</script>

<style scoped>
#layoutViewer {
  /* text-align: left; */
  padding: 5px;
  margin: 5px;
  border: 1px solid var(--greyDarker);
  background-color: var(--grey);
  width: 150px;
  height: 150px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
#layoutViewer.bigger {
  width: 200px;
  height: 200px;
}
.component {
  cursor: pointer;
  background-color: white;
  position: absolute;

  display: flex;
  justify-content: center;
  align-items: center;

  border-top: 3px solid var(--greyDark);
  background-size: contain;
  background-position: center;

  transition: all 0.1s ease-in-out;
  overflow: visible;
}

.component .content {
  display: none;
  background-color: white;
  border: 1px solid var(--grey);
  border-radius: 3px;
  padding: 4px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.component:hover {
  transform: scale(1.1);
  z-index: 2;
}
.component:hover .content {
  display: block;
}
</style>
