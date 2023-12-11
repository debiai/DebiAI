<template>
  <div id="ExplorationMode">
    <div id="content">
      <!-- Columns configuration -->
      <ColumnsConfiguration :data="data" v-if="data"/>

      <!-- WIDGET GRIDSTACK BOARD -->
      <div
        class="grid-stack"
        v-if="!loading"
      >
        <!-- Column selection -->
        <div
          id="colSelection"
          data-gs-width="6"
          data-gs-height="4"
        >
          <div class="card">
            <div class="title grid-stack-item-content">
              Select the columns you want to use for the exploration
            </div>
            <div class="body">
              <ColumnSelectionVue @save="selectedColumnsIndex = $event" />
            </div>
          </div>
        </div>

        <!-- Aggregation -->
        <div
          id="aggregation"
          data-gs-width="6"
          data-gs-height="4"
        >
          <div class="card">
            <div class="title grid-stack-item-content">
              Aggregation

              <documentation-block>
                The exploration mode only support columns <br />
                with <b> 20 unique values at most</b>. If a <br />
                column has too many unique values, <br />
                it will be ignored. <br />
                <br />
                If you want to use a column with many unique<br />
                values, you can aggregate it using different<br />
                aggregation methods. <br />
              </documentation-block>
            </div>
            <div class="body">
              <AggregationVue
                :selectedColumnsIndex="selectedColumnsIndex"
                @save="
                  selectedMetrics = $event['selectedMetrics'];
                  selectedColumnsMetrics = $event['selectedColumnsMetrics'];
                "
              />
            </div>
          </div>
        </div>

        <!-- Filtering -->
        <div
          id="filtering"
          data-gs-width="12"
          data-gs-height="8"
        >
          <div class="card">
            <div class="title grid-stack-item-content">
              Filter the data that you want to explore
            </div>
            <div class="body">
              <FilteringVue
                :selectedColumnsIndex="selectedColumnsIndex"
                :selectedColumnsMetrics="selectedColumnsMetrics"
                :selectedMetrics="selectedMetrics"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Header -->
    <Header
      :project="project"
      v-on:backToProjects="backToProjects"
    />

    <!-- Side menu -->
    <SideBar :menuList="[]" />
  </div>
</template>

<script>
import { GridStack } from "gridstack";
import "gridstack/dist/gridstack.css";

import Header from "./Header.vue";
import SideBar from "../dataAnalysis/SideBar.vue";

// Content
import ColumnsConfiguration from "./ColumnsConfiguration/ColumnsConfiguration.vue";

// Widgets
import AggregationVue from "./aggregation/Aggregation.vue";
import FilteringVue from "./filtering/Filtering.vue";
import ColumnSelectionVue from "./columnSelection/ColumnSelection.vue";

// Models
import Data from "./models/Data";

export default {
  name: "ExplorationMode",
  components: {
    Header,
    SideBar,
    ColumnsConfiguration,
    AggregationVue,
    FilteringVue,
    ColumnSelectionVue,
  },
  data: () => {
    return {
      loading: false,

      // Project
      dataProviderId: null,
      projectId: null,
      project: null,

      // Exploration
      data: null,
      selectedColumnsIndex: [], // The selected columns index
      selectedMetrics: ["Samples number"],
      selectedColumnsMetrics: null,
    };
  },
  created() {
    // get data-provider ID and project ID from url path or router params
    const dataProviderId = this.$route.params.dataProviderId
      ? this.$route.params.dataProviderId
      : this.$route.query.dataProviderId;
    const projectId = this.$route.params.projectId
      ? this.$route.params.projectId
      : this.$route.query.projectId;

    // Check if the data-provider ID and the project ID are defined
    if (dataProviderId && projectId) {
      this.dataProviderId = dataProviderId;
      this.projectId = projectId;
      this.$store.commit("setDataProviderId", dataProviderId);
      this.$store.commit("setProjectId", projectId);

      // Load data-provider info
      this.$backendDialog.getSingleDataInfo().then((dataInfo) => {
        this.$store.commit("setDataProviderInfo", dataInfo);
      });

      // Load the project data
      this.loadProject();
    } else {
      console.log("No project ID or no data provider ID");
      this.$router.push("/");
    }
  },
  mounted() {},
  methods: {
    async loadProject() {
      // this.project = null;
      this.loading = true;
      return this.$backendDialog
        .getAllColumnsMetrics()
        .then((columns) => {
          console.log(columns);
          this.data = new Data(columns);

          console.log(this.data);

          // this.project = project;
          // this.nbSelectedSamples = this.project.nbSamples;

          // Sort models and selections by update date
          // this.project.selections = this.project.selections.sort(
          //   (a, b) => b.updateDate - a.updateDate
          // );
          // this.project.models = this.project.models.sort((a, b) => b.updateDate - a.updateDate);

          // Get the project columns
          // if (!this.project.columns) this.project.columns = [];

          // Expected project results columns example :
          // [
          //   { name: "Model prediction", type: "number" },
          //   { name: "Model error", type: "number" },
          // ];
          // if (!this.project.resultStructure) this.project.resultStructure = [];

          // Store some info
          // this.$store.commit("setProjectColumns", this.project.columns);
          // this.$store.commit("setProjectResultsColumns", this.project.resultStructure);
        })
        .catch((e) => {
          if (e.response && e.response.status === 500) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Internal server error while loading project",
            });
          } else if (e.response && e.response.status === 404) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Project not found",
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error while loading project",
            });
          }
          console.log(e);
          this.$router.push("/");
        })
        .finally(() => {
          this.loading = false;
          // Setup widgets at next tick
          this.$nextTick(() => {
            this.setupWidgets();
          });
        });
    },
    backToProjects() {
      this.$router.push("/");
    },

    // Grid
    setupWidgets() {
      // Init gridStack
      let gridStackOptions = {
        minRow: 25, // don't collapse when empty
        cellHeight: 100,
        disableOneColumnMode: true,
        animate: true,
        float: false,
        resizable: {
          autoHide: true,
          handles: "e, se, s, sw, w",
        },
      };

      // Check that the selector ".grid-stack" is present in the DOM
      if (!document.querySelector(".grid-stack")) throw "No grid-stack selector found in the DOM";
      this.grid = GridStack.init(gridStackOptions);

      // Event listeners
      this.grid.on("resizestop", () => {
        // Create move event to update the plotly plots
        setTimeout(() => {
          this.$emit("GridStack_resizestop");
          window.dispatchEvent(new Event("resize"));
        }, 200);
      });

      // Animate the component when added
      this.grid.on("added", (event, items) => {
        // Get the component from the components list
        const component = items[0].el;
        if (!component) return;

        const componentElement = document.getElementById(component.id);
        componentElement.style.animation = "hiThere 500ms ease";
      });

      // this.grid.on("added removed change", () => {
      //   // Save layout in local cache
      //   this.saveLayout();
      // });

      // Setup widgets
      this.grid.removeAll();
      this.grid.makeWidget(document.getElementById("colSelection"));
      this.grid.makeWidget(document.getElementById("aggregation"));
      this.grid.makeWidget(document.getElementById("filtering"));
    },
  },
};
</script>

<style scoped lang="scss">
#ExplorationMode {
  display: flex;
  flex-direction: column;
  padding-top: 60px; /* Height of Header */
}

/* Grid stack */

#content {
  margin-left: 60px; /* Width of Sidebar */
  background-color: var(--greyLight);
  .grid-stack {
    .card {
      height: 97%;
      margin: 5px;
    }
  }
}

</style>

<style lang="scss">
// Css for all widgets
// Import Analysis mode css
@import "@/assets/css/analysis.scss";
</style>
