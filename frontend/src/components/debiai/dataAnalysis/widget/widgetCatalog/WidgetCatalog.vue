<template>
  <div id="WidgetCatalog">
    <!-- Title and close button -->
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

    <div id="content">
      <!-- Category selection -->
      <div id="categorySelection">
        <!-- Categories -->
        <u>Widget categories:</u>
        <div id="buttonList">
          <button
            v-for="category in widgetCategoriesSorted"
            :key="category"
            @click="
              selectedCategory === category
                ? (selectedCategory = '')
                : (selectedCategory = category)
            "
            :class="{ radioBtn: true, selected: selectedCategory == category }"
          >
            {{ category }}
          </button>
        </div>

        <!-- Project Types -->
        <u>Project types:</u>
        <div id="buttonList">
          <button
            v-for="projectType in widgetProjectTypesSorted"
            :key="projectType"
            @click="
              selectedCategory === projectType
                ? (selectedCategory = '')
                : (selectedCategory = projectType)
            "
            :class="{ radioBtn: true, selected: selectedCategory == projectType }"
          >
            {{ projectType }}
          </button>
        </div>
      </div>

      <!-- Widget list  -->
      <div id="widgetList">
        <transition-group name="scale">
          <Widget
            v-for="(widget, i) in selectedWidgets"
            :key="i"
            :widget="widget"
            :nbConfigurations="widgetConfigurationsOverview[widget.componentKey]"
            v-on:add="addWidget"
            v-on:addWithConf="addWidgetWithConf"
            v-on:confDeleted="loadWidgetConfigurationsOverview"
          />
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script>
import componentsGridStackData from "@/services/statistics/gridstackComponents";
import Widget from "./Widget";

export default {
  name: "widgetCatalog",
  components: { Widget },
  data() {
    return {
      widgets: [],
      widgetCategories: [],
      widgetProjectTypes: [],
      selectedCategory: "",
    };
  },
  mounted() {
    // Get the available widgets names
    this.widgets = componentsGridStackData.getAvailableWidgets();

    // Get the available widgets categories and project types
    for (let widget of this.widgets) {
      if (widget.configuration?.categories) {
        for (let category of widget.configuration.categories)
          if (!this.widgetCategories.includes(category)) this.widgetCategories.push(category);
      }
      if (widget.configuration?.projectTypes) {
        for (let projectType of widget.configuration.projectTypes)
          if (!this.widgetProjectTypes.includes(projectType))
            this.widgetProjectTypes.push(projectType);
      }
    }

    console.log(this.widgetCategories);

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
    widgetCategoriesSorted() {
      return this.widgetCategories.sort();
    },
    widgetProjectTypesSorted() {
      return this.widgetProjectTypes.sort();
    },
    selectedWidgets() {
      if (this.selectedCategory === "") return this.widgets;

      return this.widgets.filter((widget) => {
        if (widget.configuration?.categories) {
          for (let category of widget.configuration.categories)
            if (category === this.selectedCategory) return true;
        }
        if (widget.configuration?.projectTypes) {
          for (let projectType of widget.configuration.projectTypes)
            if (projectType === this.selectedCategory) return true;
        }
        return false;
      });
    },
  },
};
</script>

<style lang="scss" scoped>
#WidgetCatalog {
  width: 900px;
  height: 85vh;
  display: flex;
  flex-direction: column;

  #title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--greyDark);
  }

  #content {
    display: flex;

    #categorySelection {
      width: 200px;
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      u {
        margin: 15px 0 5px 0;
        font-size: 1.1em;
      }

      #buttonList {
        display: flex;
        flex-direction: column;
        align-items: flex-start;

        button {
          border: none;
        }
      }
    }
  }
}
</style>
