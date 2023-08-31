<template>
  <div id="ExplorationMode">
    <!-- Header -->
    <Header
      :project="project"
      v-on:refresh="loadProject"
      v-on:deleteProject="deleteProject"
      v-on:backToProjects="backToProjects"
    />

    <!-- Content -->
    <div
      class="grid-stack"
      v-if="!loading"
    >
      <!-- Column selection -->
      <div
        id="colSelection"
        data-gs-width="6"
        data-gs-height="3"
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
        data-gs-height="3"
      >
        <div class="card">
          <div class="title grid-stack-item-content">Aggregation</div>
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
        data-gs-height="5"
      >
        <div class="card">
          <div class="title grid-stack-item-content">Filter the data that you want to explore</div>
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
</template>

<script>
import { GridStack } from "gridstack";
import "gridstack/dist/gridstack.css";

import Header from "./Header.vue";
import swal from "sweetalert";

// Widgets
import AggregationVue from "./aggregation/Aggregation.vue";
import FilteringVue from "./filtering/Filtering.vue";
import ColumnSelectionVue from "./columnSelection/ColumnSelection.vue";

export default {
  name: "ExplorationMode",
  components: {
    Header,
    AggregationVue,
    FilteringVue,
    ColumnSelectionVue,
  },
  data: () => {
    return {
      // Project
      dataProviderId: null,
      projectId: null,
      project: null,
      loading: false,

      // Exploration
      selectedColumnsIndex: [1, 2, 3], // The selected columns index
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
      this.project = null;
      this.loading = true;
      return this.$backendDialog
        .getProject()
        .then((project) => {
          this.project = project;
          this.nbSelectedSamples = this.project.nbSamples;

          // Sort models and selections by update date
          this.project.selections = this.project.selections.sort(
            (a, b) => b.updateDate - a.updateDate
          );
          this.project.models = this.project.models.sort((a, b) => b.updateDate - a.updateDate);

          // Get the project columns
          // Expected project columns example :
          //  [
          //      { "name": "storage", "category": "other" },
          //      { "name": "age", "category": "context" },
          //      { "name": "path", "category": "input" },
          //      { "name": "label", "category": "groundtruth" },
          //      { "name": "type" }, # category is not specified, it will be "other"
          //  ]
          if (!this.project.columns) this.project.columns = [];

          // Expected project results columns example :
          // [
          //   { name: "Model prediction", type: "number" },
          //   { name: "Model error", type: "number" },
          // ];
          if (!this.project.resultStructure) this.project.resultStructure = [];

          // Store some info
          this.$store.commit("setProjectColumns", this.project.columns);
          this.$store.commit("setProjectResultsColumns", this.project.resultStructure);
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
    deleteProject() {
      swal({
        title: "Delete the project ?",
        text: "Do you really want to delete the project ? There is no way back.",
        buttons: true,
        icon: "warning",
        dangerMode: true,
      }).then((validate) => {
        if (validate)
          this.$backendDialog
            .deleteProject()
            .then(() => {
              this.$store.commit("sendMessage", {
                title: "success",
                msg: "Project deleted",
              });
              this.$router.push("/");
            })
            .catch((e) => {
              console.log(e);
              this.$store.commit("sendMessage", {
                title: "error",
                msg: "Could not delete the project",
              });
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
        float: false,
        disableOneColumnMode: true,
        resizable: {
          autoHide: true,
          handles: "e, se, s, sw, w",
        },
        animate: true,
      };

      // Init gridStack
      if (!document.querySelector(".grid-stack")) throw "No grid-stack selector found in the DOM";
      this.grid = GridStack.init(gridStackOptions);

      // Event listeners
      this.grid.on("resizestop", () => {
        // Create move event to update the plotly plots
        this.$emit("GridStack_resizestop");
        window.dispatchEvent(new Event("resize"));
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
  height: 100%;
  display: flex;
  flex-direction: column;
}

#header {
  display: flex;
  align-items: center;
  color: white;
  padding: 2px;
  background-color: var(--primary);
}

#debiaiMenuLogo {
  display: flex;
  justify-content: center;
  align-items: center;
  background: red;
  color: #fff;
  text-decoration: none;
  background: none;
}

.grid-stack {
  background-color: var(--greyLight);

  .card {
    height: 99%;
    width: 99%;

    .title {
      height: 20px;
      position: static;
      box-shadow: none;
      overflow: hidden;
      white-space: nowrap;
    }

    .body {
      height: 100%;
      overflow: auto;
    }
  }
}
</style>

<style>
body {
  /* background: var(--greyLight); */
}
/* Grid stack */
.grid-stack-item {
}

.grid-stack-placeholder {
  border: none;
  background-color: var(--greyDark);
  border-radius: 5px;
  transform: scale(0.95);
  transform-origin: center;
}

.ui-resizable-handle {
  z-index: 0 !important;
}
</style>
