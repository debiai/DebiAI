<template>
  <div id="Aggregation">
    <!-- Back, title, proceed buttons -->
    <div id="top">
      <div id="title">
        Select the metrics used for the exploration and aggregate the columns if needed:
      </div>
      <button
        :disabled="!canProceed"
        @click="save"
      >
        Save
      </button>
    </div>

    <!-- Metric selections -->
    <div
      id="metricSelection"
      class="card"
    >
      <div class="title">Available metrics</div>
      <div id="metrics">
        <button
          :class="'radioBtn ' + (selectedMetrics.includes(metric) ? 'selected' : '')"
          v-for="metric in metrics"
          :key="metric"
          @click="selectMetric(metric)"
        >
          {{ metric }}
        </button>
      </div>
    </div>

    <!-- Loading animation -->
    <LoadingAnimation v-if="loading"> Gathering the selected columns metrics... </LoadingAnimation>

    <!-- No selected columns message -->
    <div
      v-if="!loading && selectedColumnsIndex.length === 0"
      class="tip"
    >
      <h3 class="title">No columns selected</h3>
      <p class="body">You need to select at least one column to proceed.</p>
    </div>

    <!-- Columns metrics -->
    <transition name="fade">
      <div
        v-if="!loading"
        id="columnsMetrics"
        class="card"
      >
        <div class="title">Selected columns:</div>
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
                      :class="'radioBtn chunk ' + (i === columnMetrics.nbChunks ? 'selected' : '')"
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
  props: {
    selectedColumnsIndex: { type: Array, default: () => [] }, // The selected columns index
  },
  data() {
    return {
      maximumUniqueValues: maximumUniqueValues,
      metrics: ["Samples number"],
      selectedMetrics: ["Samples number"],
      projectColumns: [],

      selectedColumnsMetrics: null,
      nbColumnsToAggregate: 0,
      loading: false,
    };
  },
  created() {
    // Get the project columns
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;
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
      this.loading = true;
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

    save() {
      this.$emit("save", {
        selectedMetrics: this.selectedMetrics,
        selectedColumnsMetrics: this.selectedColumnsMetrics,
      });
    },
  },
  computed: {
    canProceed() {
      // We need at least one metric
      return this.selectedColumnsIndex.length - this.nbColumnsToAggregate > 0;
    },
  },
  watch: {
    selectedColumnsIndex() {
      this.loadColumnsMetrics();
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
    padding: 10px;
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

    #metrics {
      padding: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
  }

  #columnsMetrics {
    max-width: 900px;
    width: 80%;

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
