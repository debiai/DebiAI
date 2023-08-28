<template>
  <div
    id="dataAnalysis"
    v-if="data"
  >
    <!--============= Modals =============-->
    <!-- customColumnCreation -->
    <modal
      v-if="customColumnCreation"
      @close="customColumnCreation = false"
    >
      <CustomColumnCreator
        :data="data"
        @cancel="customColumnCreation = false"
        @create="createCustomColumn"
      />
    </modal>
    <!-- saveSelectionWidget -->
    <SelectionCreator
      v-if="saveSelectionWidget"
      :data="data"
      :selectedData="selectedData"
      @cancel="saveSelectionWidget = false"
      @done="saveSelectionWidget = false"
    />
    <!-- tagCreationWidget -->
    <modal
      v-if="tagCreationWidget"
      @close="tagCreationWidget = false"
    >
      <TagCreator
        :data="data"
        :selectedData="selectedData"
        @cancel="tagCreationWidget = false"
        @created="tagCreationWidget = false"
      />
    </modal>
    <!-- Selection selection -->
    <modal
      v-if="selectionSelect"
      @close="selectionSelect = false"
    >
      <SelectionSelection @cancel="selectionSelect = false" />
    </modal>
    <!-- Selection export -->
    <modal
      v-if="selectionExport"
      @close="selectionExport = false"
    >
      <SelectionExportMenu
        :data="data"
        :selectedData="selectedData"
        @cancel="selectionExport = false"
        @exported="selectionExport = false"
      />
    </modal>
    <!-- Layout -->
    <modal
      v-if="layoutModal"
      @close="layoutModal = false"
    >
      <Layouts
        :data="data"
        :components="components"
        :gridstack="grid"
        @cancel="layoutModal = false"
        @selected="loadLayout"
      />
    </modal>
    <!-- Algorithms -->
    <modal
      v-if="algorithmModal"
      @close="algorithmModal = false"
    >
      <Algorithms
        @cancel="algorithmModal = false"
        :data="data"
        :selectedData="selectedData"
      />
    </modal>
    <!-- WidgetCatalog -->
    <modal
      v-show="widgetCatalog"
      @close="widgetCatalog = false"
      :preventBodyScroll="false"
    >
      <WidgetCatalog
        @cancel="widgetCatalog = false"
        @add="addWidget"
        @addWithConf="
          ({ componentKey, configuration }) => addWidget(componentKey, null, configuration)
        "
      />
    </modal>

    <!-- WIDGET GRIDSTACK BOARD -->
    <div class="grid-stack">
      <div
        v-for="component in components"
        :key="component.id"
        :id="component.id"
        :data-gs-id="component.id"
        :data-gs-x="component.layout.x"
        :data-gs-y="component.layout.y"
        :data-gs-width="component.layout.width"
        :data-gs-min-width="component.layout.minWidth"
        :data-gs-max-width="component.layout.maxWidth"
        :data-gs-height="component.layout.height"
        :data-gs-min-height="component.layout.minHeight"
        :data-gs-max-height="component.layout.maxHeight"
      >
        <Widget
          :data="data"
          :widgetKey="component.widgetKey"
          :title="component.name"
          :configuration="component.configuration"
          :index="component.id"
          :ref="component.id"
          v-on:remove="removeWidget(component)"
          v-on:copy="(configuration) => copyWidget({ component, configuration })"
        >
          <component
            :is="component.widgetKey"
            :component="component"
            :data="data"
            :selectedData="selectedData"
            :index="component.id"
          />
        </Widget>
      </div>
    </div>

    <!-- Header menu -->
    <!-- Displays:
      The DebiAI logo
      The name of the project 
      The number of selected data 
      A button for the filters and for the colored column
    -->
    <Header
      :data="data"
      :selectedData="selectedData"
      @addWidget="widgetCatalog = !widgetCatalog"
    />

    <!-- Side menu -->
    <SideBar :menuList="menuList" />
  </div>
</template>

<script>
import { GridStack } from "gridstack";
import "gridstack/dist/gridstack.css";

// Widget
import Widget from "./widget/Widget";
import Vue from "vue";

// Menu
import Header from "./Header";
import SideBar from "./SideBar";
import CustomColumnCreator from "./dataCreation/CustomColumnCreator";
import SelectionSelection from "./dataNavigation/SelectionSelection";
import SelectionCreator from "./dataCreation/SelectionCreator";
import TagCreator from "./dataCreation/TagCreator";
import SelectionExportMenu from "./dataExport/SelectionExportMenu";
import Algorithms from "./algoProviders/Algorithms";
import Layouts from "./widget/layouts/Layouts";
import WidgetCatalog from "./widget/widgetCatalog/WidgetCatalog";

// Services
import componentsGridStackData from "@/services/statistics/gridstackComponents";
import samplesFiltering from "@/services/statistics/samplesFiltering";
import { getAnalysisExport } from "@/services/statistics/analysisExport";

export default {
  components: {
    // Widget
    Widget,

    // Menu
    Header,
    SideBar,
    CustomColumnCreator,
    SelectionSelection,
    SelectionCreator,
    TagCreator,
    SelectionExportMenu,
    Algorithms,
    Layouts,
    WidgetCatalog,
  },
  data() {
    return {
      // Analysis data
      data: null, // Contain all the data that the widget will read
      selectedData: null, // Index of the selected samples or results

      // Workspace
      components: [],
      grid: null,

      // Modals
      customColumnCreation: false,
      selectionExport: false,
      selectionSelect: false,
      saveSelectionWidget: false,
      tagCreationWidget: false,
      algorithmModal: false,
      layoutModal: false,
      widgetCatalog: false,

      // Menu
      menuList: [
        {
          name: "Generate report",
          icon: "downloadImage",
          menuList: [
            {
              name: "Markdown",
              description:
                "Generate a zip file with a markdown containing the widget images, comments and configurations",
              callback: this.exportAnalysisPage,
            },
          ],
        },
        {
          name: "Selections",
          icon: "loop",
          menuList: [
            {
              name: "Create a new selection",
              description: "Create a new selection from the samples that are currently selected",
              callback: this.saveSelection,
            },
            {
              name: "Open a selection",
              description: "Start a new analysis with another selection",
              callback: this.selectionSelectionBtn,
            },
          ],
        },
        {
          name: "Compute new data",
          icon: "algorithm",
          menuList: [
            {
              name: "Create a virtual column",
              description: "Create a virtual column locally based on other columns and a formula",
              callback: this.customColumn,
            },
            {
              name: "Use an external algorithm",
              description: "Use an algorithm from DebiAI or from an external algo-provider",
              callback: this.useAlgorithm,
            },
          ],
        },
        {
          name: "Annotate the selected data",
          icon: "tag",
          menuList: [
            {
              name: "Tag",
              description: "Create locally a new column with a value matching the selected samples",
              callback: this.tagCreation,
            },
            {
              name: "Export with an annotation",
              description:
                "Export to another application the selected samples ID with an annotation",
              callback: this.exportSelection,
            },
          ],
        },
        {
          name: "Layout",
          icon: "layout",
          menuList: [
            {
              name: "Save or load",
              description:
                "Save the current layout to load it later, or load a previously saved layout",
              callback: this.layout,
            },
            {
              name: "Restore default",
              description: "Clear the current layout and restore the default one",
              callback: this.restoreDefaultLayout,
            },
            {
              name: "Clear",
              description: "Clear the current layout and enjoy a blank page",
              callback: this.clearLayout,
            },
          ],
        },
      ],
    };
  },
  created() {
    // check data integrity
    if (!this.$route.params.data) {
      // No data sended, checking url references
      let dataProviderId = this.$route.query.dataProviderId;
      let projectId = this.$route.query.projectId;
      let selectionIds = this.$route.query.selectionIds;
      let selectionIntersection = this.$route.query.selectionIntersection;
      let modelIds = this.$route.query.modelIds;
      let commonModelResults = this.$route.query.commonModelResults;

      if (dataProviderId && projectId) {
        // Go back to project page to start an analysis immediately
        this.$router.push({
          path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
          query: {
            projectId: projectId,
            dataProviderId: dataProviderId,
            selectionIds: selectionIds,
            selectionIntersection: selectionIntersection,
            modelIds: modelIds,
            commonModelResults: commonModelResults,
            startAnalysis: true,
          },
        });
      } else this.$router.push("/");
    } else {
      // Load provided data and set selected data to 100%
      this.data = this.$route.params.data;
      this.selectedData = [...Array(this.data.nbLines).keys()];

      // Load available Widgets from the widget folder
      this.loadWidgets();

      // Load saved layout
      this.loadLastLayout();
    }
  },
  mounted() {
    // Init gridStack
    let gridStackOptions = {
      minRow: 25, // don't collapse when empty
      cellHeight: 100,
      disableOneColumnMode: true,
      float: false,
      margin: 0,
      resizable: {
        autoHide: true,
        handles: "e, se, s, sw, w",
      },
    };

    // Check that the selector ".grid-stack" is present in the DOM
    if (!document.querySelector(".grid-stack")) return;
    this.grid = GridStack.init(gridStackOptions);
    this.grid.on("resizestop", () => {
      // Create move event to update the plotly plots
      this.$emit("GridStack_resizestop");
      window.dispatchEvent(new Event("resize"));
    });

    // Animate the widget when added
    this.grid.on("added", (event, items) => {
      // Get the component from the components list
      const component = this.components.find((c) => items[0].id == c.id);
      if (!component) return;

      // Animate the component
      const componentElement = document.getElementById(component.id);
      componentElement.style.opacity = 0.5;
      componentElement.style.transform = "scale(1.05)";
      setTimeout(() => {
        componentElement.style.transition = "transform 100ms ease-in-out 0s";
        componentElement.style.transform = "scale(1)";
        componentElement.style.opacity = 1;
      }, 10);
    });

    // this.grid.on("added removed change", () => {
    //   // Save layout in local cache
    //   this.saveLayout();
    // });
  },
  methods: {
    // Grid stack & widgets
    loadWidgets() {
      // Load every available widget from the widget folder
      // Load every files with the .vue extension in the widgets folder
      // Somehow, the require.context doesn't work with a variable path
      const availableWidgetPath = require.context("./widgets/", true, /\.vue$/i);

      availableWidgetPath.keys().forEach((componentFilePath) => {
        // Get the component name from the file name
        const componentKey = componentFilePath.split("/")[1];

        // Load the component
        Vue.component(componentKey, () =>
          import("./widgets/" + componentKey + "/" + componentKey + ".vue")
        );
      });
    },
    loadLastLayout() {
      // Get the last layout saved for this project
      const projectId = this.$store.state.ProjectPage.projectId;
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;

      // Get all the saved layouts
      this.$backendDialog
        .getLayouts()
        .then((layouts) => {
          // Find the last layout saved for this project
          const lastLayout = layouts.find(
            (l) =>
              l.projectId == projectId && l.dataProviderId == dataProviderId && l.lastLayoutSaved
          );

          if (lastLayout) {
            // Load the layout
            this.loadLayout(lastLayout);
          } else {
            // No layout found, load default layout
            this.restoreDefaultLayout();
          }
        })
        .catch((e) => {
          console.log(e);
        });
    },
    loadLayout(layout_full) {
      const layout = layout_full.layout;
      const selectedColorColumn = layout_full.selectedColorColumn;

      this.clearLayout();
      this.layoutModal = false;

      // Set selectedColorColumn
      if (selectedColorColumn) {
        // Get the column index
        const column = this.data.columns.find((c) => c.label == selectedColorColumn);
        const coloredColumnIndex = this.$store.state.StatisticalAnalysis.coloredColumnIndex;

        // Set the column index
        if (column == null) {
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + selectedColorColumn + " hasn't been found",
          });
        } else if (coloredColumnIndex != column.index) {
          this.$store.commit("setColoredColumnIndex", column.index);
        }
      } else this.$store.commit("setColoredColumnIndex", null);

      layout.forEach((c) => {
        // Get the key (previous layout version saved in cache)
        if (!c.widgetKey) c.widgetKey = c.key;

        if (!c.widgetKey || !componentsGridStackData.widgetExists(c.widgetKey)) {
          console.warn("Component " + c.widgetKey + " not found");
          return;
        }

        // get comp default layout :
        const component = componentsGridStackData.createWidget(c.widgetKey);

        // set shape from given layout
        component.layout.x = c.x;
        component.layout.y = c.y;
        component.layout.height = c.height;
        component.layout.width = c.width;

        // set configuration from given layout
        if (c.config) component.configuration = { configuration: c.config };

        this.components.push(component);
      });

      // wait until vue has completely rendered the new components
      this.$nextTick(() => {
        this.components.forEach((component) => {
          this.grid.makeWidget(document.getElementById(component.id));
        });
      });
    },
    addWidget(compKey, layout, configuration = null) {
      this.widgetCatalog = false;

      // get layout
      let component = componentsGridStackData.createWidget(compKey);
      if (layout) component.layout = { ...component.layout, ...layout };
      if (configuration) component.configuration = configuration;

      // Add the component to the grid
      this.components.push(component);

      // wait until vue has completely rendered the new component
      this.$nextTick(() => {
        this.grid.makeWidget(document.getElementById(component.id));
      });
    },
    removeWidget(component) {
      this.grid.removeWidget(document.getElementById(component.id), false);
      this.components = this.components.filter((c) => c.id !== component.id);
    },
    copyWidget({ component, configuration }) {
      // Find the layout of the component
      let gsComp = this.grid.save().find((c) => c.id == component.id);

      // Create the component with its configuration if possible
      this.addWidget(component.widgetKey, gsComp, configuration);
    },
    updateLayoutConfig() {
      // Update the components list with their config
      this.components.forEach((component) => {
        component.config = this.$refs[component.id][0].getComponentConf();
      });
    },
    saveLayout() {
      // Get the current layout
      if (!this.grid) return;

      // Get the current layout from the gridstack
      this.updateLayoutConfig();
      let gridStackLayout = this.grid.save();
      const layout = [];
      gridStackLayout.forEach((gsComp) => {
        // Get the component from the components list
        const gridComponent = this.components.find((c) => gsComp.id == c.id);
        if (!gridComponent) return;

        // Add the widgetKey and config to the gs layout
        gsComp.widgetKey = gridComponent.widgetKey;
        gsComp.config = gridComponent.config;

        layout.push(gsComp);
      });

      // Create the layout save request body
      const projectId = this.$store.state.ProjectPage.projectId;
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;

      const requestBody = {
        name: projectId + " last layout",
        description:
          "Last layout for project " + projectId + " and data provider " + dataProviderId,
        layout: [],
        lastLayoutSaved: true, // This will erase the previous last layout saved
      };

      // Add the selectedColorColumn
      const coloredColumnIndex = this.$store.state.StatisticalAnalysis.coloredColumnIndex;
      if (coloredColumnIndex !== null) {
        requestBody.selectedColorColumn = this.data.columns[coloredColumnIndex].label;
      }

      // We remove some properties from the layout
      // Expected layout:
      // [{ x, y, w, h, widgetKey, config }];
      layout.forEach((component) => {
        requestBody.layout.push({
          x: component.x,
          y: component.y,
          width: component.width,
          height: component.height,
          widgetKey: component.widgetKey,
          config: component.config,
        });
      });

      // Send the request
      this.$backendDialog
        .saveLayout(requestBody)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Layout saved",
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't save the layout",
          });
        });
    },

    // Buttons
    restoreDefaultLayout() {
      setTimeout(() => {
        this.loadLayout(componentsGridStackData.defaultLayout);
      }, 100);
    },
    clearLayout() {
      while (this.components.length > 0) this.removeWidget(this.components[0]);
    },
    customColumn() {
      this.customColumnCreation = true;
    },
    createCustomColumn(newCol) {
      this.customColumnCreation = false;
      this.data.columns.push(newCol);
      this.data.nbColumns += 1;
      this.data.labels.push(newCol.label);
      this.$store.commit("sendMessage", {
        title: "success",
        msg: "Column created successfully",
      });
    },
    selectionSelectionBtn() {
      this.selectionSelect = true;
    },
    saveSelection() {
      this.saveSelectionWidget = true;
    },
    tagCreation() {
      this.tagCreationWidget = true;
    },
    exportSelection() {
      this.selectionExport = true;
    },
    useAlgorithm() {
      this.algorithmModal = true;
    },
    clearLayout() {
      while (this.components.length > 0) this.removeWidget(this.components[0]);
    },
    layout() {
      this.updateLayoutConfig();
      this.layoutModal = true;
    },
    async exportAnalysisPage() {
      let proceed = true;

      // Start progress bar
      const requestCode = this.$services.uuid();
      this.$store.commit("startRequest", {
        name: "Generating analysis export",
        code: requestCode,
        progress: 0,
        cancelCallback: () => {
          proceed = false;
        },
      });

      try {
        // Ask all the components for their results
        const widgetsResults = [];
        for (let i = 0; i < this.components.length; i++) {
          // Check if the user cancelled the export
          if (!proceed) {
            this.$store.commit("sendMessage", {
              title: "success",
              msg: "Export cancelled",
            });
            return;
          }

          // Update progress bar
          this.$store.commit("updateRequestProgress", {
            code: requestCode,
            progress: i / this.components.length,
          });

          const component = this.components[i];
          const componentId = component.id;

          // Get image
          const imageUrl = await this.$refs[componentId][0].getImage();

          // Get configuration
          const config = this.$refs[componentId][0].getComponentConf();

          // Get Comments
          const comments = this.$refs[componentId][0].getComments();

          widgetsResults.push({
            id: componentId,
            name: component.name,
            widget: component.widgetKey,
            comments: comments,
            imageUrl: imageUrl,
            config: config,
          });
        }

        // Get the project name
        const projectName = this.$store.state.ProjectPage.projectId;

        // Generate the analysis export
        getAnalysisExport(widgetsResults, projectName);
      } catch (error) {
        console.error(error);
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Error while exporting the analysis",
        });
      } finally {
        this.$store.commit("endRequest", requestCode);
      }
    },
  },
  computed: {
    filters() {
      // Get the filters form the store
      return this.$store.state.StatisticalAnalysis.filters;
    },
  },
  watch: {
    filters() {
      // Update the selected samples from the filters
      try {
        let { selectedSampleIds, filtersEffects } = samplesFiltering.getSelected(
          this.filters,
          this.data
        );
        this.$store.commit("setFiltersEffects", filtersEffects);
        this.selectedData = selectedSampleIds;
      } catch (error) {
        console.error(error);
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Error while filtering the samples",
        });
      }
    },
  },
  beforeDestroy() {
    // Save the layout
    this.saveLayout();

    // this.$store.commit("selectProjectId", null);
    this.$store.commit("setSelectionsIds", null);
    this.$store.commit("setColoredColumnIndex", 0);

    // Remove the grid
    if (this.grid) this.grid.destroy();
  },
};
</script>

<style scoped>
#dataAnalysis {
  padding-top: 60px; /* Height of Header */
}

/* Grid stack */
.grid-stack-item {
  overflow: hidden;
}
</style>

<style>
/* Css for all widgets */
.dataVisualizationWidget {
  height: 100%;
  min-height: 100px;
}

.plot {
  height: 100%;
}

.grid-stack {
  margin-left: 60px; /* Width of Sidebar */
  background-color: var(--greyLight);
}

.grid-stack-placeholder {
  border: 1px dashed black;
  transform-origin: center;
  transform: scale(0.95);
}

.ui-resizable-handle {
  z-index: 0 !important;
}
</style>
