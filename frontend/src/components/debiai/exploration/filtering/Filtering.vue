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
    <LoadingAnimation v-if="loading">
      <br />
      <br />
      <br />
      Gathering the selected columns combinations...
    </LoadingAnimation>

    <!-- Plot and warning message-->
    <div
      id="content"
      class="card"
    >
      <!-- Warning message -->
      <div
        class="tip warning"
        v-show="tooManyCombinationsWarning"
      >
        The number of combinations is too high to be used in the exploration mode and has been
        reduced in order to avoid a crash.
        <br />
        If you want to use a column with many unique values, you can aggregate it by chunks or
        reduce the number of columns.
      </div>

      <!-- Parallel categories plot -->
      <div id="parallelCategories" />
    </div>

    <!-- Combinations -->
    <div
      class="card"
      id="combinations"
    >
      <div class="padded">Total possible combinations: {{ nbCombinations }}</div>
      <button @click="showCombinationsList = true">All combinations</button>
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
    };
  },
  mounted() {
    // Checking url references
    let dataProviderId = this.$route.query.dataProviderId;
    let projectId = this.$route.query.projectId;

    if (!dataProviderId || !projectId) this.$router.push("/");

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
      const colWithSelectedSamples = [];

      const nonNullCombinations = this.combinationsMetrics.filter((c) => c.metrics.nbValues > 0);

      this.selectedColumnsMetrics.forEach((column, i) => {
        const combinations = nonNullCombinations.map((c) => c.combination[i]);

        colWithSelectedSamples.push({ label: column.label, values: combinations });
      });

      const counts = nonNullCombinations.map((c) => c.metrics.nbValues);

      const trace = {
        type: "parcats",
        dimensions: colWithSelectedSamples,
        counts: counts,
      };

      let layout = {
        margin: {
          l: 20,
          r: 30,
          b: 20,
          t: 30,
        },
      };

      Plotly.newPlot("parallelCategories", [trace], layout, {
        displayModeBar: false,
        responsive: true,
      });

      // Set plot selection event
      // this.divParCat.removeListener("plotly_click", this.selectDataOnPlot);
      // this.divParCat.on("plotly_click", this.selectDataOnPlot);
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
        // TODO: Pass aggrerations
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
}
</style>
