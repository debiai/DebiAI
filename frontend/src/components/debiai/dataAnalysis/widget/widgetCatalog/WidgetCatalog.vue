<template>
  <div id="WidgetCatalog">
    <h2 id="title">
      <span class="aligned">
        Select a widget

        <documentation-block>
          DebiAI provide a large set of widgets that can be used to display data in the dashboard.
          <br />
          <br />
          Find, according to your needs, the widgets that suits your activity the best.
          <br />
          <br />
          Full documentation
          <a
            href="https://debiai.irt-systemx.fr/dashboard/widgets/"
            target="_blank"
            >here</a
          >.
        </documentation-block>
      </span>

      <button
        class="red"
        @click="$emit('cancel')"
      >
        Close
      </button>
    </h2>
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
  </div>
</template>

<script>
import componentsGridStackData from "@/services/statistics/gridstackComponents";
import Widget from "./Widget";
import { marked } from "marked";

export default {
  name: "widgetCatalog",
  components: { Widget },
  data() {
    return {
      widgets: [],
      selectedWidgetNumber: 0,
      widgetDescriptions: {},
      widgetConfigurationsOverview: {}, // { <widgetTitle>: <nbOfConfigurations> }
    };
  },
  mounted() {
    // Loading the available widgets names
    this.widgets = componentsGridStackData.getAvailableWidgets();

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
      return this.widgetDescriptions[this.widgets[this.selectedWidgetNumber].componentKey];
    },
    previewText() {
      if (this.widgetDescription === undefined) return "No documentation";
      try {
        return marked.parse(this.widgetDescription);
      } catch (error) {
        console.log("Error while parsing markdown");
        console.log(this.widgetDescription);
        console.log(error);
        return "Error while parsing the documentation";
      }
    },
    iconPath() {
      if (this.widgets.length == 0) return null;
      return "documentation/images/" + this.widgets[this.selectedWidgetNumber].name + "/icon.png";
    },
  },
};
</script>

<style lang="scss" scoped>
#WidgetCatalog {
  width: 800px;
  display: flex;
  flex-direction: column;

  #title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
  }
}
</style>
