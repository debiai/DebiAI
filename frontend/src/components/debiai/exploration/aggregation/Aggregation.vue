<template>
  <div id="Aggregation">
    <!-- Back, title, proceed buttons -->
    <div
      id="top"
      v-if="selectedColumnsIndex.length > 0 && !loading"
    >
      <div id="title">
        <ColorTag
          color="yellow"
          v-if="nbColumnsToAggregate > 0"
          title="Some columns need to be aggregated before proceeding."
        />
      </div>
      <button
        :disabled="!canProceed"
        @click="save"
      >
        Save
      </button>
    </div>

    <!-- Metric selections -->
    <!-- <div
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
    </div> -->

    <!-- No selected columns message -->
    <!-- <div
      v-else
      class="tip"
    >
      <h3>No columns selected</h3>
      <p class="body">You need to select at least one column to proceed.</p>
    </div> -->

    <!-- Loading animation -->
    <LoadingAnimation
      v-if="loading"
      style="padding: 30px"
    >
      Gathering the selected columns metrics...
    </LoadingAnimation>

    <!-- Columns metrics -->
    <transition name="fade">
      <div
        v-if="!loading"
        id="columnsMetrics"
      >
        <!-- Columns -->
        <div
          v-for="columnMetrics in selectedColumnsMetrics"
          :key="columnMetrics.label"
          class="column"
        >
          <!-- Title -->
          <h4 class="label aligned gapped">
            {{ columnMetrics.label }}
            <div class="tag">
              {{ columnMetrics.type }}
            </div>
          </h4>

          <!-- Unique values -->
          <div class="nbUniqueValues">
            <!-- Warning if the number of unique values is too high -->
            <ColorTag
              color="yellow"
              v-if="!columnAggregationValid(columnMetrics)"
              title="The number of unique values is too high to be used in the exploration mode."
            />

            <!-- Chunk size -->
            <b> {{ columnMetrics.nbUniqueValues }} </b>unique values
            <span v-if="columnMetrics.nbChunks">/ {{ columnMetrics.nbChunks }} chunk </span>

            <!-- Aggregate button -->
            <button
              @click="
                columnMetrics.openAggregationModal = true;
                $forceUpdate();
              "
            >
              Aggregate
            </button>
          </div>

          <!-- Aggregation parameters modal -->
          <Modal
            v-if="columnMetrics.openAggregationModal"
            @close="
              columnMetrics.openAggregationModal = false;
              $forceUpdate();
            "
          >
            <div class="aggregationParameters">
              <h3>Aggregate the column to reduce the number of unique values</h3>

              <div
                class="aggregationMethod chunks"
                v-if="columnMetrics.type === 'number'"
              >
                Aggregate by chunks

                <select
                  v-model="columnMetrics.nbChunks"
                  @change="calculateNbColumnsToAggregate()"
                >
                  <option
                    v-for="i in Math.min(maximumUniqueValues, columnMetrics.nbUniqueValues)"
                    :key="i"
                    :value="i"
                  >
                    {{ i }}
                  </option>
                </select>
              </div>

              <div
                class="aggregationMethod letters"
                v-if="columnMetrics.type === 'text'"
              >
                Aggregate using the first letters of the column values. <br />

                Number of letters to use:
                <select
                  v-model="columnMetrics.nbChunks"
                  @change="calculateNbColumnsToAggregate()"
                >
                  <option
                    v-for="i in 2"
                    :key="i"
                    :value="Math.pow(15, i)"
                  >
                    {{ i }}
                  </option>
                </select>
              </div>

              <div class="controls">
                <span>
                  <button
                    class="green"
                    @click="
                      columnMetrics.openAggregationModal = false;
                      $forceUpdate();
                    "
                  >
                    Done
                  </button>
                  <button
                    class="red"
                    @click="
                      columnMetrics.openAggregationModal = false;
                      $forceUpdate();
                    "
                  >
                    Close
                  </button>
                </span>
              </div>
            </div>
          </Modal>
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

            // Find the column in the project columns
            const projectColumn = this.projectColumns.find((c) => c.name === column.label);
            // {
            //   category: "other",
            //   index: 1,
            //   name: "col",
            //   type: "auto"
            // }

            // Add the column type
            column.type = projectColumn.type;

            // Add aggregation modal parameters
            column.openAggregationModal = false;
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
  width: 100%;

  #top {
    width: 95%;
    padding: 10px;
    gap: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    button {
    }
  }

  #metricSelection {
    #metrics {
      padding: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
  }

  #columnsMetrics {
    width: 100%;
    .column {
      margin: 5px;
      padding: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;

      border: 1px solid var(--greyDark);
      border-radius: 5px;

      .label {
        font-weight: bold;
      }

      .nbUniqueValues {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
      }

      .aggregationParameters {
        display: flex;
        flex-direction: column;
        gap: 20px;

        .chunks {
          display: flex;
          align-items: center;
          gap: 10px;
        }
      }

      .controls {
        display: flex;
        justify-content: flex-end;
      }
    }
  }
}
</style>
