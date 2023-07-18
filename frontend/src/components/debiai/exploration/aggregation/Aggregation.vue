<template>
  <div id="Aggregation">
    <!-- Back, title, proceed buttons -->
    <div id="top">
      <button @click="back">&lt; Column selection</button>
      <h3 id="title">
        Select the metrics used for the exploration and aggregate the columns if needed:
      </h3>
      <button
        :disabled="!canProceed"
        @click="proceed"
      >
        Proceed >
      </button>
    </div>

    <!-- Metric selections -->
    <div
      id="metricSelection"
      class="card"
    >
      <h3>Available metrics:</h3>
      <div id="metrics">
        <div
          :class="'metric ' + (selectedMetrics.includes(metric) ? 'selected' : '')"
          v-for="metric in metrics"
          :key="metric"
          @click="selectMetric(metric)"
        >
          {{ metric }}
        </div>
      </div>
    </div>

    <!-- Loading animation -->
    <LoadingAnimation v-if="loading"> Gathering the selected columns metrics... </LoadingAnimation>

    <!-- Columns metrics -->
    <transition name="fade">
      <div
        v-if="!loading"
        id="columnsMetrics"
        class="card"
      >
        <h3>Selected columns:</h3>
        <transition name="fade">
          <div
            id="warningMessage"
            class="tip warning"
            v-show="nbColumnsToAggregate > 0"
          >
            The exploration mode only support columns with a certain number of unique values,
            <b> {{ maximumUniqueValues }} unique values at most</b>. If a column has too many unique
            values, it will be ignored.
            <br />
            If you want to use a column with many unique values, you can aggregate it by chunks.
          </div>
        </transition>

        <!-- Columns -->
        <div
          v-for="columnMetrics in selectedColumnsMetrics"
          :key="columnMetrics.label"
          class="column"
        >
          <Collapsible
            :headerColor="columnAggregationValid(columnMetrics) ? 'green' : 'red'"
            :headerTitle="
              columnAggregationValid(columnMetrics)
                ? ''
                : 'The number of unique values is too high to be used in the exploration mode.'
            "
          >
            <!-- Column header -->
            <template v-slot:header>
              <div
                class="columnTitle"
                :title="
                  columnAggregationValid(columnMetrics)
                    ? ''
                    : 'The number of unique values is too high to be used in the exploration mode.'
                "
              >
                <!-- Title -->
                <h4 class="label">
                  {{ columnMetrics.label }}
                </h4>
                <!-- Unique values -->
                <div class="nbUniqueValues">
                  <b> {{ columnMetrics.nbUniqueValues }} </b>unique values

                  <!-- Chunk size -->
                  <span v-if="columnMetrics.nbChunks">/ {{ columnMetrics.nbChunks }} chunk </span>
                </div>
              </div>
            </template>
            <template v-slot:body>
              <div class="aggregationParameters">
                <div class="parameter">
                  <h4>Aggregate the column by chunks</h4>
                  <div class="chunks">
                    Number of chunks:
                    <br />
                    <button
                      v-for="i in Math.min(maximumUniqueValues, columnMetrics.nbUniqueValues)"
                      :key="i"
                      :class="'chunk ' + (i === columnMetrics.nbChunks ? '' : 'white')"
                      @click="
                        columnMetrics.nbChunks = i === columnMetrics.nbChunks ? null : i;
                        calculateNbColumnsToAggregate();
                      "
                    >
                      {{ i }}
                    </button>
                  </div>
                </div>
                <!-- <div class="parameter">
                  <h4>Aggregate the column using timestamp</h4>
                  <div>WIP</div>
                </div> -->
              </div>
            </template>
          </Collapsible>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
const maximumUniqueValues = 20;

export default {
  data() {
    return {
      maximumUniqueValues: maximumUniqueValues,
      metrics: ["Samples number"],
      selectedMetrics: ["Samples number"],
      projectColumns: [],
      selectedColumnsIndex: [],

      selectedColumnsMetrics: null,
      nbColumnsToAggregate: 0,
      loading: true,
    };
  },
  created() {
    // Checking url references
    let dataProviderId = this.$route.query.dataProviderId;
    let projectId = this.$route.query.projectId;

    if (!dataProviderId || !projectId) this.$router.push("/");

    // Get the project columns
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;
    this.selectedColumnsIndex = this.$route.query.selectedColumnsIndex;

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

    // Load the metrics
    this.loadColumnsMetrics();
  },
  methods: {
    selectMetric(metric) {
      if (this.selectedMetrics.includes(metric)) {
        this.selectedMetrics = this.selectedMetrics.filter((m) => m !== metric);
      } else {
        this.selectedMetrics.push(metric);
      }
    },

    loadColumnsMetrics() {
      const columnLabels = this.selectedColumnsIndex.map(
        (index) => this.projectColumns[index].name
      );

      this.$backendDialog
        .getColumnsMetrics(columnLabels)
        .then((metrics) => {
          this.selectedColumnsMetrics = metrics;

          // Add a nbChunks property to each column
          this.selectedColumnsMetrics.forEach((column) => {
            column.nbChunks = null;
          });

          // Calculate the number of columns to aggregate
          this.calculateNbColumnsToAggregate();
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

    columnAggregationValid(column) {
      if (!"nbUniqueValues" in column) return false;

      if (column.nbUniqueValues > maximumUniqueValues) {
        if (!column.nbChunks) return false;
      }

      return true;
    },

    calculateNbColumnsToAggregate() {
      let nbColumns = 0;

      // Check if some columns needs aggregation
      // And if they do, check if the aggregation is fixed
      for (let columnMetrics of this.selectedColumnsMetrics) {
        if (columnMetrics.nbUniqueValues > maximumUniqueValues) {
          if (!columnMetrics.nbChunks) {
            nbColumns++;
          }
        }
      }

      this.$forceUpdate();

      this.nbColumnsToAggregate = nbColumns;
    },

    // Router
    back() {
      this.$router.push({
        name: "columnSelection",
        query: {
          projectId: this.$route.query.projectId,
          dataProviderId: this.$route.query.dataProviderId,
          selectedColumnsIndex: this.selectedColumnsIndex,
        },
      });
    },
    proceed() {
      this.$router.push({
        name: "filtering",
        query: {
          projectId: this.$route.query.projectId,
          dataProviderId: this.$route.query.dataProviderId,
          selectedColumnsIndex: this.selectedColumnsIndex,
          selectedMetrics: this.selectedMetrics,
          selectedColumnsMetrics: this.selectedColumnsMetrics,
        },
      });
    },
  },
  computed: {
    canProceed() {
      // We need at least one metric
      return this.selectedColumnsIndex.length - this.nbColumnsToAggregate > 0;
    },
  },
};
</script>

<style scoped lang="scss">
#Aggregation {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: center;

  #top {
    width: 90%;
    margin: 20px;
    gap: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    button {
      min-width: 120px;
    }
  }

  #metricSelection {
    max-width: 900px;
    width: 80%;
    margin: 10px;
    padding: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
    h3 {
      margin: 10px;
    }

    #metrics {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;

      .metric {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f0f0;
        cursor: pointer;

        &:hover {
          background-color: #e0e0e0;
        }

        &:active {
          background-color: #d0d0d0;
        }

        &.selected {
          background-color: var(--primary);
          color: white;
          font-weight: bold;
        }
      }
    }
  }

  #columnsMetrics {
    max-width: 900px;
    width: 80%;
    margin: 10px;
    padding: 10px;

    h3 {
      margin: 10px;
    }

    .column {
      margin: 5px;

      .columnTitle {
        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 10px;

        .label {
          font-weight: bold;
        }

        .nbUniqueValues {
          border-radius: 5px;
          border: 1px solid;
          padding: 5px;
        }
      }

      .aggregationParameters {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .parameter {
          padding: 10px;
        }
        .chunk {
          padding: 5px 12px;
        }
      }
    }
  }
}
</style>
