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
        <transition-group
          name="scale"
          class="itemList"
          style="width: 100%"
        >
          <Widget
            v-for="widget in selectedWidgets"
            :key="widget.componentKey"
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
    // Load widget configurations then setup widgets
    this.loadWidgetConfigurationsOverview();
  },
  methods: {
    loadWidgetConfigurationsOverview() {
      this.widgetConfigurationsOverview = {};

      this.$backendDialog
        .getWidgetConfigurationsOverview()
        .then((configuration) => {
          this.widgetConfigurationsOverview = configuration;
        })
        .finally(() => {
          this.setupWidgets();
        });
    },
    setupWidgets() {
      // Get the available widgets names
      this.widgets = componentsGridStackData.getAvailableWidgets();

      // Get the available widgets categories and project types
      for (let widget of this.widgets) {
        if (widget.categories) {
          for (let category of widget.categories)
            if (!this.widgetCategories.includes(category)) this.widgetCategories.push(category);
        }
        if (widget.projectTypes) {
          for (let projectType of widget.projectTypes)
            if (!this.widgetProjectTypes.includes(projectType))
              this.widgetProjectTypes.push(projectType);
        }
      }
    },
    addWidget(widget) {
      this.$emit("add", widget.componentKey);
    },
    addWidgetWithConf({ widget, configuration }) {
      this.$emit("addWithConf", {
        componentKey: widget.componentKey,
        configuration,
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
      // Sort the widget by number of categories so that
      // the most important ones are displayed first
      const sortedWidgets = this.widgets.sort((a, b) => {
        if (a.categories && b.categories) {
          if (a.categories.length > b.categories.length) return -1;
          if (a.categories.length < b.categories.length) return 1;
        }
        if (a.categories && !b.categories) return -1;
        if (!a.categories && b.categories) return 1;
        return 0;
      });

      if (this.selectedCategory === "") return sortedWidgets;

      return sortedWidgets.filter((widget) => {
        if (widget.categories) {
          for (let category of widget.categories)
            if (category === this.selectedCategory) return true;
        }
        if (widget.projectTypes) {
          for (let projectType of widget.projectTypes)
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
      width: 150px;
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
    #widgetList {
      flex: 1;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-start;
      overflow-y: auto;
      height: 80vh;
    }
  }
}
</style>
