<template>
  <div id="WidgetCatalog">
    <!-- Widget list  -->
    <div id="widgetList">
      <Widget
        v-for="(widget, i) in widgets"
        :key="i"
        :widget="widget"
        :nbConfigurations="widgetConfigurationsOverview[widget.componentKey]"
        v-on:add="addWidget"
        v-on:addWithConf="addWidgetWithConf"
        v-on:selected="selectedWidgetNumber = i"
        v-on:confDeleted="loadWidgetConfigurationsOverview"
      />
    </div>

    <!-- Widget details -->
    <div id="widgetDetails">
      <div id="controls">
        <button class="red" @click="$emit('cancel')">Cancel</button>
      </div>
      <div id="content">
        <div class="well well-sm pre-scrollable" v-html="previewText"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Widget from "./Widget";
let marked = require("marked");

export default {
  name: "widgetCatalog",
  components: { Widget },
  props: { widgets: { requiered: true, type: Array } },
  data() {
    return {
      selectedWidgetNumber: 0,
      widgetDescriptions: {},
      widgetConfigurationsOverview: {}, // { <widgetTitle>: <nbOfConfigurations> }
    };
  },
  mounted() {
    // Load md widgets descriptions
    this.widgets.forEach((widget) => {
      try {
        const widgetGuide = require("raw-loader!../../widgets/" +
          widget.componentKey +
          "/guide.md").default;
        this.widgetDescriptions[widget.componentKey] = widgetGuide;
      } catch (error) {
        console.warn("No guide for " + widget.componentKey);
      }
    });

    // Load widget configurations
    this.loadWidgetConfigurationsOverview();
  },
  methods: {
    addWidget(widget) {
      this.$emit("add", widget.componentKey);
    },
    addWidgetWithConf({ widget, configuration }) {
      this.$emit("addWithConf", {
        componentKey: widget.componentKey,
        configuration,
      });
    },
    loadWidgetConfigurationsOverview() {
      this.widgetConfigurationsOverview = {};

      this.$backendDialog.getWidgetConfigurationsOverview().then((configuration) => {
        this.widgetConfigurationsOverview = configuration;
      });
    },
  },
  computed: {
    widgetDescription() {
      if (this.widgets.length == 0) return "";
      return this.widgetDescriptions[
        this.widgets[this.selectedWidgetNumber].componentKey
      ];
    },
    previewText() {
      marked.setOptions({
        renderer: new marked.Renderer(),
      });
      if (this.widgetDescription) return marked(this.widgetDescription);
      else return null;
    },
    iconPath() {
      if (this.widgets.length == 0) return null;
      return (
        "documentation/images/" +
        this.widgets[this.selectedWidgetNumber].name +
        "/icon.png"
      );
    },
  },
};
</script>

<style scoped>
#WidgetCatalog {
  display: grid;
  grid-template-columns: 1fr 1.7fr;
  grid-template-rows: 1fr;
  gap: 0px 0px;
  grid-template-areas: "widgetList widgetDetails";

  height: 80vh;
  width: 80vw;
}
#widgetList {
  grid-area: widgetList;
  border-radius: 10px;
  overflow-y: auto;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);
}
#widgetDetails {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: min-content min-content 1.9fr;
  gap: 0px 0px;
  grid-template-areas:
    "controls controls"
    "title title"
    "content content";
  grid-area: widgetDetails;
  max-height: 100%;
  max-height: 100%;
  overflow: auto;
}
#controls {
  grid-area: controls;
  text-align: right;
  padding-right: 10px;
}
#content {
  grid-area: content;
  max-height: 100%;
  padding: 10px;
}
#title {
  display: grid;
  grid-template-columns: min-content 1fr min-content;
  grid-template-rows: 1fr;
  gap: 0px 0px;
  grid-template-areas: "icon name";
  grid-area: title;
}
#icon {
  grid-area: icon;
  padding-left: 20px;
}
#icon {
  max-height: 150px;
  max-width: 150px;
}
#name {
  grid-area: name;
}

#btn {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>