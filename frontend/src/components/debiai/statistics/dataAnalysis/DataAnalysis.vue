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
    <modal
      v-if="saveSelectionWidget"
      @close="saveSelectionWidget = false"
    >
      <SelectionCreator
        :data="data"
        :selectedData="selectedData"
        @cancel="saveSelectionWidget = false"
        @done="saveSelectionWidget = false"
      />
    </modal>
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
        @cancel="layoutModal = false"
        @selected="loadLayout"
        :components="components"
        :gridstack="grid"
      />
    </modal>
    <!-- WidgetCatalog -->
    <modal
      v-if="widgetCatalog"
      @close="widgetCatalog = false"
    >
      <WidgetCatalog
        @cancel="widgetCatalog = false"
        @add="addWidget"
        @addWithConf="
          ({ componentKey, configuration }) => addWidget(componentKey, null, configuration)
        "
      />
    </modal>

    <!-- floating menu -->
    <fab
      name="menu"
      bg-color="var(--primaryDark)"
      position="top-right"
      main-tooltip="Menu"
      main-icon="menu"
      fixed-tooltip="true"
      z-index="2"
      :actions="menuList"
      @customColumn="customColumn"
      @saveSelection="saveSelection"
      @tagCreation="tagCreation"
      @exportSelection="exportSelection"
      @layout="layout"
      @restoreDefaultLayout="restoreDefaultLayout"
      @clearLayout="clearLayout"
    />
    <!-- floating wiget catalog menu -->
    <div @click="widgetCatalog = !widgetCatalog">
      <fab
        name="widgetCatalog"
        bg-color="var(--success)"
        size="small"
        position="right"
        main-tooltip="Add a widget"
        main-icon="add"
        z-index="2"
      />
    </div>
    <header />

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
          :simple="component.simple"
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

    <!-- Bottom menu -->
    <Footer
      :data="data"
      :selectedData="selectedData"
    />
  </div>
  <div
    id="dataAnalysis"
    v-else
  >
    Loading
  </div>
</template>

<script>
import { GridStack } from "gridstack";
import "gridstack/dist/gridstack.css";
import fab from "vue-fab"; // For the bubble floating menu

// Widget
import Widget from "./utils/Widget";
import Vue from "vue";

// Menu
import CustomColumnCreator from "./dataCreation/CustomColumnCreator";
import SelectionCreator from "./dataCreation/SelectionCreator";
import TagCreator from "./dataCreation/TagCreator";
import SelectionExportMenu from "./dataExport/SelectionExportMenu";
import Layouts from "./utils/layouts/Layouts";
import WidgetCatalog from "./utils/widgetCatalog/WidgetCatalog";
import Footer from "./dataNavigation/Footer";

// Services
import componentsGridStackData from "../../../../services/statistics/gridstackComponents";
import samplesFiltering from "../../../../services/statistics/samplesFiltering";

export default {
  components: {
    // Widget
    Widget,

    // Menu
    CustomColumnCreator,
    SelectionCreator,
    TagCreator,
    SelectionExportMenu,
    Layouts,
    WidgetCatalog,

    Footer,

    // Other
    fab, // (Floating Action Button)
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
      saveSelectionWidget: false,
      tagCreationWidget: false,
      selectionExport: false,
      layoutModal: false,
      widgetCatalog: false,

      // Menu
      menuList: [
        {
          name: "customColumn",
          icon: "playlist_add",
          tooltip: "Add a virtual column",
          color: "var(--success)",
        },
        {
          name: "saveSelection",
          icon: "save",
          tooltip: "Create a new selection",
          color: "var(--success)",
        },
        {
          name: "tagCreation",
          icon: "local_offer",
          tooltip: "Tag the selected samples",
          color: "var(--success)",
        },
        {
          name: "exportSelection",
          icon: "send",
          tooltip: "Export the selected samples",
          color: "var(--success)",
        },
        {
          name: "layout",
          icon: "auto_awesome_mosaic",
          tooltip: "Save or load layout",
          color: "var(--info)",
        },
        {
          name: "restoreDefaultLayout",
          icon: "undo",
          tooltip: "Restore the default layout",
          color: "var(--warning)",
        },
        {
          name: "clearLayout",
          icon: "delete",
          tooltip: "Clear layout",
          color: "var(--dangerDark)",
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
      let commomModelResults = this.$route.query.commomModelResults;

      if (dataProviderId && projectId) {
        // Go back to project page to start an analysis imediatly
        this.$router.push({
          path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
          query: {
            projectId: projectId,
            dataProviderId: dataProviderId,
            selectionIds: selectionIds,
            selectionIntersection: selectionIntersection,
            modelIds: modelIds,
            commomModelResults: commomModelResults,
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

      // Load local storage grid stack layout or the default one if no layout is saved
      let savedGridStackLayout = window.localStorage.getItem("gridStackLayout");
      if (savedGridStackLayout) {
        savedGridStackLayout = JSON.parse(savedGridStackLayout);
        this.loadLayout(savedGridStackLayout);
      } else {
        // No saved layout
        this.defaultLayout();
      }
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

    this.grid = GridStack.init(gridStackOptions);
    this.grid.on("resizestop", () => {
      // Create move event to update the plotly plots
      this.$emit("GridStack_resizestop");
      window.dispatchEvent(new Event("resize"));
    });
    this.grid.on("added removed change", () => {
      // Save layout in local cache
      this.saveLayout();
    });
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
    loadLayout(layout) {
      this.clearLayout();
      this.layoutModal = false;
      layout.forEach((c) => {
        // Get the key (previous cache version)
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

        // add to model
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

      // Create the componen with its configuration if possible
      this.addWidget(component.widgetKey, gsComp, configuration);
    },
    getLayout() {
      if (this.grid) {
        let gsPos = this.grid.save();
        let layout = [];
        gsPos.forEach((gsComp) => {
          const gridComponent = this.components.find((c) => gsComp.id == c.id);
          if (!gridComponent) return;
          gsComp.widgetKey = gridComponent.widgetKey;
          layout.push(gsComp);
        });
        return JSON.stringify(layout);
      }
    },
    saveLayout() {
      // TODO
      const layout = this.getLayout();
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
    saveSelection() {
      this.saveSelectionWidget = true;
    },
    tagCreation() {
      this.tagCreationWidget = true;
    },
    exportSelection() {
      this.selectionExport = true;
    },
    clearLayout() {
      while (this.components.length > 0) this.removeWidget(this.components[0]);
    },
    layout() {
      this.layoutModal = true;

      // Fetch the configuration of each component
      this.components.forEach((component) => {
        const componentConfig = this.$refs[component.id][0].getComponentConf();
        component.config = componentConfig;
      });
    },
  },
  computed: {
    filters() {
      // Get the filters form the store
      return this.$store.state.SatisticalAnasysis.filters;
    },
  },
  watch: {
    filters() {
      // Update the selected samples from the filters
      try {
        let { selectedSampleIds, filtersEffecs } = samplesFiltering.getSelected(
          this.filters,
          this.data
        );
        this.$store.commit("setFiltersEffects", filtersEffecs);
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
    // this.$store.commit("selectProjectId", null);
    this.$store.commit("setSelectionsIds", null);
    this.$store.commit("setColoredColumnIndex", 0);
  },
};
</script>

<style scoped>
header {
  display: flex;
  background-color: var(--third);
  height: 43px;
}

header #widgetList {
  display: flex;
}

header #widgetList button + button {
  margin-left: 5px;
}

/* Grid stack */
.grid-stack-item {
  overflow: hidden;
}

.ui-resizable-handle {
  z-index: 2 !important;
}
</style>

<style>
/* Css for all plot childrens */
.dataVisualisationWidget {
  height: 100%;
}

.plot {
  height: 100%;
}

.grid-stack {
  background-color: lightgray;
}

.grid-stack-placeholder {
  border: 1px dashed black;
  transform-origin: center;
  transform: scale(0.95);
}

.ui-resizable-handle {
  z-index: 2;
}
</style>
