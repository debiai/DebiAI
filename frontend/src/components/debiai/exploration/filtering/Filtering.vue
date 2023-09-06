<template>
  <div id="Filtering">
    <!-- Combinations list modal -->
    <Modal
      v-if="showCombinationsList"
      @close="showCombinationsList = false"
    >
      <!-- Title and checkbox -->
      <div class="aligned spaced">
        <h3>Combinations list</h3>
        <div id="sortByValuesCheckBox">
          Sort by number of values
          <input
            type="checkbox"
            id="sortByValuesCB"
            class="customCbx"
            v-model="sortCombinationsByValues"
            style="display: none"
          />
          <label
            for="sortByValuesCB"
            class="toggle"
          >
            <span></span>
          </label>
        </div>
        <button @click="showCombinationsList = false">Close</button>
      </div>
      <!-- Table of all the combinations with their metrics. -->
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
              v-for="(combination, i) in combinationsMetricsDisplay"
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

    <!-- New selection modal -->
    <Modal
      v-if="newSelectionModal"
      @close="newSelectionModal = false"
    >
      <h3 class="aligned spaced gapped padded">
        Create a new selection
        <button
          @click="newSelectionModal = false"
          class="red"
        >
          Cancel
        </button>
      </h3>
      <div class="aligned spaced gapped padded">
        <label for="selectionName">Name:</label>
        <input
          type="text"
          id="selectionName"
          v-model="newSelectionName"
          @keyup.enter="createSelection"
          ref="selectionNameInput"
        />
        <button
          @click="createSelection"
          :disabled="dataIdLoading"
          class="green"
        >
          Create
        </button>
      </div>
    </Modal>

    <!-- Loading animation -->
    <LoadingAnimation
      v-if="loading"
      center
    >
      Gathering the selected columns combinations...
    </LoadingAnimation>

    <!-- Plot and warning message-->
    <div id="content">
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
    <transition name="fade">
      <div
        class="card"
        id="combinations"
        v-if="!loading"
      >
        <div class="padded">Total combinations number: {{ nbCombinations }}</div>
        <button @click="showCombinationsList = true">All combinations</button>
      </div>
    </transition>

    <!-- Filters & metrics-->
    <transition name="fade">
      <div
        class="card"
        id="filters"
        v-if="!loading"
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
          <TransitionGroup name="scaleRight">
            <div
              class="filter"
              v-for="filter in filters"
              :key="filter.columnLabel"
            >
              <div class="name">{{ filter.columnLabel }}:</div>
              <div class="value">{{ filter.value }}</div>
            </div>
          </TransitionGroup>
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
              v-for="combination in selectedCombinations"
              :key="combination.index"
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

        <!-- Metrics -->
        <h3 v-if="selectedCombinations.length > 0">Metrics</h3>

        <div
          id="metrics"
          v-if="selectedCombinations.length > 0"
        >
          Total selected samples: {{ totalSelectedSamples }} / {{ totalSamples }} ({{
            ((totalSelectedSamples / totalSamples) * 100).toFixed(2)
          }}%)
        </div>

        <!-- Nothing selected tip -->
        <transition name="fade">
          <div v-if="filters.length === 0">
            <div class="tip">
              No filter applied, select a path on the parallel categories diagram to add a filter.
            </div>
          </div>
        </transition>
      </div>
    </transition>

    <!-- Controls -->
    <div
      id="controls"
      class="aligned padded onRight"
      v-if="selectedCombinations.length > 0"
    >
      <button
        :disabled="dataIdLoading"
        @click="
          newSelectionModal = true;
          $nextTick(() => $refs.selectionNameInput.focus());
        "
      >
        Create a selection
      </button>
      <button :disabled="dataIdLoading">Analyze the data</button>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

export default {
  props: {
    selectedColumnsIndex: { type: Array, default: () => [] },
    selectedMetrics: { type: Array, default: () => [] },
    selectedColumnsMetrics: { type: Array, default: () => [] },
  },
  data() {
    return {
      loading: false,
      tooManyCombinationsWarning: false,
      showCombinationsList: false,
      projectColumns: [],

      combinationsMetrics: [],
      nbCombinations: 0,
      sortCombinationsByValues: false,

      filters: [],
      selectedCombinations: [],

      dataIdLoading: false,
      newSelectionModal: false,
      newSelectionName: "Exploration selection",
    };
  },
  mounted() {
    // Get the project columns
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;

    if (this.selectedColumnsIndex.length > 0) this.loadCombinations(); // Development purpose
  },
  methods: {
    loadCombinations() {
      console.log("Load combinations");
      console.log(this.selectedColumnsMetrics);
      if (!this.selectedColumnsMetrics?.length) return;

      this.combinationsMetrics = [];
      this.loading = true;

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
          this.combinationsMetrics = [...metrics.combinations];

          if (metrics.totalCombinations > metrics.combinations.length)
            this.tooManyCombinationsWarning = true;

          this.nbCombinations = metrics.totalCombinations;
          this.nonNullCombinations = this.combinationsMetrics.filter((c) => c.metrics.nbValues > 0);
          // Add an index to each combination
          this.nonNullCombinations = this.nonNullCombinations.map((c, i) => {
            c.index = i;
            return c;
          });

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
        height: 390,
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
    createSelection() {
      // Get the data ids of the selected combinations
      this.dataIdLoading = true;
      this.$backendDialog
        .getDataIdListFromFilters(this.filters)
        .then((dataIds) => {
          // Create the selection
          this.$backendDialog
            .addSelection(dataIds, this.newSelectionName)
            .then(() => {
              console.log("3");
              this.$store.commit("sendMessage", {
                title: "success",
                msg: "The selection has been created.",
              });
            })
            .catch((error) => {
              console.error(error);
              this.$store.commit("sendMessage", {
                title: "error",
                msg: "An error occurred while creating the selection.",
              });
            })
            .finally(() => {
              this.dataIdLoading = false;
              this.newSelectionModal = false;
            });
        })
        .catch((error) => {
          console.error(error);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "An error occurred while getting the data ids of the selected combinations.",
          });
          this.dataIdLoading = false;
        });
    },
    analyzeData() {},
  },
  computed: {
    totalSamples() {
      return this.combinationsMetrics.reduce((acc, comb) => acc + comb.metrics.nbValues, 0);
    },
    totalSelectedSamples() {
      return this.selectedCombinations.reduce((acc, comb) => acc + comb.metrics.nbValues, 0);
    },
    combinationsMetricsSorted() {
      return [...this.combinationsMetrics].sort((a, b) => b.metrics.nbValues - a.metrics.nbValues);
    },
    combinationsMetricsDisplay() {
      if (this.sortCombinationsByValues) return this.combinationsMetricsSorted;
      return this.combinationsMetrics;
    },
  },
  watch: {
    selectedColumnsIndex() {
      this.loadCombinations();
    },
    selectedColumnsMetrics() {
      this.loadCombinations();
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
    height: 400px;
  }
  #combinations {
    margin: 3px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }
  #sortByValuesCheckBox {
    padding: 5px;
    background-color: #e1e1e1;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
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
            padding: 4px;
            gap: 5px;
            border-radius: 5px;
          }
        }
      }
    }
  }
}
</style>
