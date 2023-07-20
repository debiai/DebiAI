<template>
  <div id="Filtering">
    <!-- Combinations list modal -->
    <Modal
      v-if="showCombinationsList"
      @close="showCombinationsList = false"
    >
      <div class="aligned spaced">
        <h3>Combinations list</h3>
        <button @click="showCombinationsList = false">Close</button>
      </div>
      <div id="combinationsListModal">
        <br />
        <table>
          <thead>
            <tr>
              <th>N°</th>
              <th
                v-for="i in selectedColumnsIndex"
                :key="i"
              >
                {{ projectColumns[i].name }}
              </th>
              <th
                v-for="metric in Object.keys(combinationsMetrics[0].metrics)"
                :key="metric"
                class="metric"
              >
                {{ metric }}
              </th>
            </tr>
          </thead>

          <tbody id="combinationsList">
            <tr
              class="combination"
              v-for="(combination, i) in combinationsMetrics"
              :key="i"
            >
              <!-- Combination number -->
              <td class="number">
                {{ i + 1 }}
              </td>

              <!-- Combination values -->
              <td
                class="value"
                v-for="(value, j) in combination.combination"
                :key="j"
              >
                {{ value }}
              </td>

              <!-- Metrics -->
              <td
                class="metric"
                v-for="(metric, j) in combination.metrics"
                :key="j"
              >
                {{ metric }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Modal>

    <!-- Back btn and title -->
    <div id="top">
      <button @click="back">&lt; Aggregation panel</button>
      <h3 id="title">Filter the data that you want to explore:</h3>
    </div>

    <!-- Loading animation -->
    <LoadingAnimation
      v-if="loading"
      center
    >
      Gathering the selected columns combinations...
    </LoadingAnimation>

    <!-- Plot and warning message-->
    <div
      id="content"
      class="card"
    >
      <!-- Parallel categories plot -->
      <div id="parallelCategories" />
    </div>
    <!-- Warning message -->
    <div
      class="tip warning"
      v-show="tooManyCombinationsWarning"
    >
      The number of combinations is too high to be used in the exploration mode and has been reduced
      in order to avoid a crash.
      <br />
      If you want to use a column with many unique values, you can aggregate it by chunks or reduce
      the number of columns.
    </div>
    <!-- Combinations -->
    <div
      class="card"
      id="combinations"
    >
      <div class="padded">Total possible combinations: {{ nbCombinations }}</div>
      <button @click="showCombinationsList = true">All combinations</button>
    </div>

    <!-- Filters & metrics-->
    <div
      class="card"
      id="filters"
    >
      <!-- Selected filters -->
      <h3
        class="aligned spaced"
        style="height: 30px"
      >
        Filters

        <transition name="fade">
          <button
            v-if="filters.length > 0"
            @click="clearFilters"
          >
            Clear filters
          </button>
        </transition>
      </h3>

      <div id="filterList">
        <transition-group name="scaleRight">
          <div
            class="filter"
            v-for="filter in filters"
            :key="filter.columnLabel"
          >
            <div class="name">{{ filter.columnLabel }}:</div>
            <div class="value">{{ filter.value }}</div>
          </div>
        </transition-group>
      </div>

      <!-- Selected combinations -->
      <h3
        v-if="selectedCombinations.length > 0"
        class="aligned spaced"
      >
        Selected combinations
      </h3>
      <div
        id="combinationList"
        v-if="selectedCombinations.length > 0"
      >
        <transition-group name="scaleRight">
          <div
            class="combination"
            v-for="(combination, i) in selectedCombinations"
            :key="i"
          >
            <div class="values">
              <div
                class="value"
                v-for="(value, j) in combination.combination"
                :key="j"
              >
                {{ value }}
              </div>
            </div>
            <div class="metrics">
              <div
                class="metric"
                v-for="(metric, j) in combination.metrics"
                :key="j"
              >
                <div class="name">{{ j }}:</div>
                <div class="value">{{ metric }}</div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Nothing selected tip -->
      <transition name="fade">
        <div v-if="filters.length === 0">
          <div class="tip">
            No filter applied, click on a path in the Parallel Categories diagram to add a filter.
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  data() {
    return {
      loading: true,
      tooManyCombinationsWarning: false,
      showCombinationsList: false,
      selectedColumnsIndex: [],
      projectColumns: [],

      combinationsMetrics: [],
      nbCombinations: 0,

      filters: [],
      selectedCombinations: [],
    };
  },
  mounted() {
    // Checking url references
    let dataProviderId = this.$route.query.dataProviderId;
    let projectId = this.$route.query.projectId;

    if (!dataProviderId || !projectId) {
      this.$router.push("/");
      return;
    }
    this.$store.commit("setDataProviderId", dataProviderId);
    this.$store.commit("setProjectId", projectId);

    // Get the project columns
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;
    this.selectedColumnsIndex = this.$route.query.selectedColumnsIndex;
    this.selectedMetrics = this.$route.query.selectedMetrics;
    this.selectedColumnsMetrics = this.$route.query.selectedColumnsMetrics;

    if (this.projectColumns?.length === 0 || this.selectedColumnsIndex?.length === 0) {
      // Go back to project page and start the exploration immediately
      this.$router.push({
        path: "/dataprovider/" + dataProviderId + "/project/" + projectId,
        query: {
          projectId: projectId,
          dataProviderId: dataProviderId,
          startExploration: true,
        },
      });
    }

    if (this.selectedMetrics?.length === 0 || this.selectedColumnsMetrics?.length === 0) {
      // Go back to the aggregation page
      this.$router.push({
        name: "Aggregation",
        query: {
          projectId: projectId,
          dataProviderId: dataProviderId,
          selectedColumnsIndex: this.selectedColumnsIndex,
        },
      });
    }

    // Load the combinations metrics
    this.combinationsMetrics = [];
    this.loadCombinations();
  },
  methods: {
    loadCombinations() {
      // Build request parameters
      const parameters = [];

      this.selectedColumnsMetrics.forEach((column, index) => {
        parameters.push({
          label: column.label,
          nbChunks: column.nbChunks,
        });
      });

      this.$backendDialog
        .getColumnsCombinatorialMetrics(parameters)
        .then((metrics) => {
          this.combinationsMetrics = metrics.combinations;

          if (metrics.totalCombinations > metrics.combinations.length)
            this.tooManyCombinationsWarning = true;

          this.nbCombinations = metrics.totalCombinations;
          this.nonNullCombinations = this.combinationsMetrics.filter((c) => c.metrics.nbValues > 0);

          this.drawPlot();
        })
        .catch((error) => {
          console.error(error);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "An error occurred while loading the metrics.",
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },

    drawPlot() {
      const columnsCombinations = [];

      this.selectedColumnsMetrics.forEach((column, i) => {
        const combinations = this.nonNullCombinations.map((c) => c.combination[i]);

        columnsCombinations.push({ label: column.label, values: combinations });
      });

      const counts = this.nonNullCombinations.map((c) => c.metrics.nbValues);

      const colors = new Int8Array(this.nonNullCombinations.length);

      const trace = {
        type: "parcats",
        dimensions: columnsCombinations,
        counts: counts,
        line: {
          color: colors,
          cmin: 0,
          cmax: 1,
        },
      };

      let layout = {
        margin: {
          l: 20,
          r: 30,
          b: 20,
          t: 30,
        },
        height: 600,
      };

      const plotDiv = document.getElementById("parallelCategories");

      Plotly.newPlot(plotDiv, [trace], layout, {
        displayModeBar: false,
        responsive: true,
      });

      // Set plot selection event
      // this.divParCat.removeListener("plotly_click", this.selectDataOnPlot);
      // this.divParCat.on("plotly_click", this.selectDataOnPlot);

      // Update color on selection and click

      plotDiv.on("plotly_click", (points_data) => {
        const new_color = new Int8Array(this.nonNullCombinations.length);

        for (var i = 0; i < points_data.points.length; i++) {
          new_color[points_data.points[i].pointNumber] = 1;
        }

        // Update color of selected paths in parallel categories diagram
        Plotly.restyle(plotDiv, { "line.color": new_color }, 0);

        // Construct the filters
        this.filters = [];
        for (const constraintColumnIndex of Object.keys(points_data.constraints)) {
          if (constraintColumnIndex === "color") continue;

          this.filters.push({
            columnLabel: this.selectedColumnsMetrics[constraintColumnIndex].label,
            value: points_data.constraints[constraintColumnIndex],
          });
        }

        // Get the selected combinations
        this.selectedCombinations = [];
        for (const pointNumber of points_data.points) {
          this.selectedCombinations.push(this.nonNullCombinations[pointNumber.pointNumber]);
        }
      });
    },

    clearFilters() {
      this.filters = [];
      this.selectedCombinations = [];
      const colors = new Int8Array(this.nonNullCombinations.length);
      Plotly.restyle(
        document.getElementById("parallelCategories"),
        { "line.color": colors, "line.cmin": 0, "line.cmax": 1 },
        0
      );
    },

    // Router
    back() {
      this.$router.push({
        name: "aggregation",
        query: {
          projectId: this.$route.query.projectId,
          dataProviderId: this.$route.query.dataProviderId,
          selectedColumnsIndex: this.selectedColumnsIndex,
        },
        // TODO: Pass agrerations
      });
    },
  },
};
</script>

<style scoped lang="scss">
#Filtering {
  text-align: left;
  display: flex;
  flex-direction: column;

  #top {
    width: 90%;
    margin: 20px;
    gap: 20px;
    display: flex;
    justify-content: flex-start;
    align-items: center;

    button {
      min-width: 120px;
    }
  }
  #content {
    padding: 5px;
    height: 600px;
  }
  #combinations {
    margin: 3px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }
  #combinationsListModal {
    max-height: 600px;
    min-width: 800px;
    margin-top: 20px;
    padding-right: 10px;
    overflow: auto;

    // Table style:

    table {
      border-collapse: collapse;
      width: 100%;
      position: relative;
      border-collapse: collapse;
    }

    th {
      position: sticky;
      padding: 8px;
      top: 0;
      background-color: #f2f2f2;
    }
    td {
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    .metric {
      text-align: right;
      border-left: 1px solid #ddd;
    }
  }
  #filters {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;

    #filterList span {
      display: flex;
      flex-direction: row;
      overflow: auto;
      padding-bottom: 20px;
      gap: 10px;

      .filter {
        display: flex;
        flex-direction: row;
        gap: 10px;
        padding: 5px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f2f2f2;

        .name {
          font-weight: bold;
        }
      }
    }
    #combinationList span {
      display: flex;
      flex-direction: row;
      overflow: auto;
      padding-bottom: 20px;
      gap: 10px;

      .combination {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 5px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f2f2f2;

        max-height: 100px;

        .values {
          display: flex;
          flex-direction: row;
          gap: 10px;

          .value {
            font-size: 0.8em;
            white-space: nowrap;

            &:not(:last-child)::after {
              content: ">";
            }
          }
        }

        .metrics {
          display: flex;
          gap: 10px;

          .metric {
            display: flex;
            border: 1px solid rgb(85, 85, 85);
            padding: 10px;
            gap: 5px;
            border-radius: 5px;
          }
        }
      }
    }
  }
}
</style>
