<template>
  <div class="categories">
    <!-- Column categories -->
    <div
      v-for="(columns, category) in columnsGroupedByCategory"
      :key="category"
      class="category"
    >
      <h3>{{ category }}</h3>
      <!-- Columns -->
      <div class="columns">
        <div
          v-for="column in columns"
          :key="column.name"
          class="column"
        >
          <!-- Name, type & unique values -->
          <div class="columnDetails">
            <!-- Btn -->
            <button
              @click="selectColumn(column)"
              :class="{
                selected: isColumnSelected(column) && !hasColumnMetrics(column.name),
                disabled: hasColumnAggregation(column.name) || hasColumnMetrics(column.name),
              }"
            >
              {{ column.name }}
            </button>
            <!-- Unique values -->
            <div class="nbUnique">{{ column.nbUniqueValues }}</div>
            <!-- Type -->
            <div
              class="type"
              :class="[column.type]"
            >
              {{ column.type }}
            </div>

            <!-- Statistics -->
            <div class="statistics">
              <!-- min -->
              <span
                v-if="column.type === 'number'"
                class="label"
                >Min:</span
              >
              <span
                v-if="column.type === 'number'"
                class="value"
                :title="column.min"
                >{{ $services.prettyNumber(column.min) }}</span
              >
              <!-- max -->
              <span
                v-if="column.type === 'number'"
                class="label"
                >Max:</span
              >
              <span
                v-if="column.type === 'number'"
                class="value"
                :title="column.max"
                >{{ $services.prettyNumber(column.max) }}</span
              >
              <!-- Average -->
              <span
                v-if="column.type === 'number'"
                class="label"
                >Mean:</span
              >
              <span
                v-if="column.type === 'number'"
                class="value"
                :title="column.average"
                >{{ $services.prettyNumber(column.average) }}</span
              >
            </div>
          </div>

          <!-- Controls -->
          <div class="controls">
            <!-- Metric -->
            <button
              v-if="!hasColumnAggregation(column.name) && column.type === 'number'"
              @click="openColumnMetricsModal(column)"
              title="Add combination metrics to this column"
              class="borderlessHover metrics"
            >
              <inline-svg
                :src="require('@/assets/svg/barPlot.svg')"
                height="20"
                width="20"
              />
              Metrics
              <span
                class="badge"
                v-if="hasColumnMetrics(column.name)"
              >
                {{ Object.keys(hasColumnMetrics(column.name)).length }}
              </span>
            </button>

            <!-- Aggregation -->
            <button
              @click="openColumnAggregationModal(column)"
              v-if="!hasColumnAggregation(column.name) && !hasColumnMetrics(column.name)"
              title="Reduce the number dimensions with aggregation"
              class="borderlessHover aggregation"
            >
              <inline-svg
                :src="require('@/assets/svg/aggregation.svg')"
                height="17"
                width="17"
              />
              Aggregation
            </button>

            <!-- Aggregation info -->
            <div
              v-if="hasColumnAggregation(column.name)"
              class="aggregation"
            >
              <button
                class="borderlessHover"
                @click="openColumnAggregationModal(column)"
              >
                <inline-svg
                  :src="require('@/assets/svg/aggregation.svg')"
                  height="16"
                  width="16"
                />

                <span v-if="column.type === 'number'">
                  {{ hasColumnAggregation(column.name).nbChunks }} chunks
                </span>
                <span v-if="column.type === 'text'">
                  {{ hasColumnAggregation(column.name).nbCharacters }} characters
                </span>
              </button>
              <button
                class="red"
                @click="removeAggregation(column.name)"
                title="Remove aggregation"
              >
                &times;
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Unsupported Columns -->
    <div
      v-if="unsupportedColumns.length"
      class="category"
    >
      <h3>Unsupported Columns</h3>
      <div class="columns unsupported">
        <div
          v-for="column in unsupportedColumns"
          :key="column.name"
          class="column"
        >
          <div>
            <button disabled>
              {{ column.name }}
            </button>
            <div class="nbUnique">?</div>
            <div
              class="type"
              :class="[column.type]"
            >
              {{ column.type }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Number column metrics modal -->
    <Modal
      v-if="selectedColumnForMetrics"
      @close="selectedColumnForMetrics = null"
      leftAlign
    >
      <!-- Title -->
      <h2
        class="aligned spaced gapped"
        style="padding-bottom: 20px"
      >
        '{{ selectedColumnForMetrics.name }}' number column metrics
        <button
          class="red"
          @click="selectedColumnForMetrics = false"
        >
          Close
        </button>
      </h2>

      <p>Add metrics for this columns</p>

      <form
        action=""
        @submit.prevent
      >
        <!-- Select metric -->
        <div
          class="form-group"
          v-for="metric in availableMetrics"
          :key="metric.name"
        >
          <button
            @click="selectMetric(metric.name)"
            :class="{
              selected: metric.selected,
            }"
          >
            {{ metric.name }}
          </button>
          <span class="description">{{ metric.description }}</span>
        </div>

        <!-- Apply button -->
        <div class="controls">
          <button
            class="green"
            @click="applyMetrics"
          >
            Apply metrics
          </button>
        </div>
      </form>
    </Modal>
    <!-- Number column aggregation modal -->
    <Modal
      v-if="selectedColumnForAggregation && selectedColumnForAggregation.type === 'number'"
      @close="selectedColumnForAggregation = null"
      leftAlign
    >
      <!-- Title -->
      <h2
        class="aligned spaced gapped"
        style="padding-bottom: 20px"
      >
        Reduce the '{{ selectedColumnForAggregation.name }}' number column <br />
        dimensions with aggregation
        <button
          class="red"
          @click="selectedColumnForAggregation = false"
        >
          Close
        </button>
      </h2>

      <p>Aggregate the column to reduce the number of unique values</p>

      <form
        action=""
        @submit.prevent
      >
        <!-- Number of chunks -->
        <div class="form-group">
          <label for="nbChunks">Aggregate the column in</label>
          <input
            type="number"
            id="nbChunks"
            v-model.number="nbChunks"
            min="1"
            style="width: 50px; margin: 0 10px"
            required
          />
          <span>chunks</span>
        </div>

        <!-- Even quantity or even range selector -->
        <div class="form-group">
          <label for="aggregationType">Aggregation type:</label>
          <select
            id="aggregationType"
            v-model="aggregationType"
          >
            <option value="evenRange">Even range</option>
            <option value="evenQuantity">Even quantity</option>
          </select>
        </div>

        <!-- Apply button -->
        <div class="controls">
          <button
            class="green"
            @click="applyAggregation"
            :disabled="!selectedColumnForAggregation || nbChunks < 1"
          >
            Apply aggregation
          </button>
        </div>
      </form>
    </Modal>
    <!-- String column aggregation modal -->
    <Modal
      v-if="selectedColumnForAggregation && selectedColumnForAggregation.type === 'text'"
      @close="selectedColumnForAggregation = null"
      leftAlign
    >
      <!-- Title -->
      <h2
        class="aligned spaced gapped"
        style="padding-bottom: 20px"
      >
        Reduce the '{{ selectedColumnForAggregation.name }}' text column <br />
        dimensions with aggregation
        <button
          class="red"
          @click="selectedColumnForAggregation = false"
        >
          Close
        </button>
      </h2>

      <p>Aggregate the column to reduce the text of unique values</p>

      <form
        action=""
        @submit.prevent
      >
        <!-- Number of first letters -->
        <div class="form-group">
          <label for="nbChunks">Aggregate by first characters</label>
          <input
            type="number"
            id="nbCharacters"
            v-model.number="nbCharacters"
            min="1"
            max="3"
            style="width: 50px; margin: 0 10px"
            required
          />
          <span>characters</span>
          <DocumentationBlock> e.g. 'Hello' and 'Hi' will be aggregated to 'H' </DocumentationBlock>
        </div>

        <!-- Number of characters skipped -->
        <div class="form-group">
          <label for="nbCharacters">Number of characters to skip:</label>
          <input
            type="number"
            id="nbCharacters"
            v-model.number="nbCharactersSkip"
            min="0"
            style="width: 50px; margin: 0 10px"
            required
          />
          <DocumentationBlock>
            e.g. 'Hello' will be considered has 'llo' if set to 2
          </DocumentationBlock>
        </div>

        <!-- Apply button -->
        <div class="controls">
          <button
            class="green"
            @click="applyAggregation"
            :disabled="nbCharacters < 1"
          >
            Apply aggregation
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script>
export default {
  name: "Columns",
  props: {
    project: {
      type: Object,
      required: true,
    },
    exploration: {
      type: Object,
      required: true,
    },
    columnsStatistics: {
      type: Array,
      required: true,
    },
    selectedColumns: {
      type: Array,
      required: true,
    },
    selectedColumnMetrics: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      // Column metrics
      selectedColumnForMetrics: null,
      availableMetrics: [{ name: "mean", description: "Mean value of the column combination" }],
      // Column aggregation
      selectedColumnForAggregation: null,
      // Number column aggregation
      nbChunks: 5,
      aggregationType: "evenRange",
      // String column aggregation
      nbCharacters: 1,
      nbCharactersSkip: 0,
    };
  },
  methods: {
    selectColumn(column) {
      if (this.isUnsupported(column)) return;
      if (column.aggregation || this.hasColumnMetrics(column.name)) return;

      const columnName = column.name;
      const existingColumn = this.selectedColumns.find((selected) => selected.label === columnName);

      if (existingColumn) {
        // If the column is already selected, unselect it
        this.selectedColumns.splice(this.selectedColumns.indexOf(existingColumn), 1);
      } else {
        this.selectedColumns.push({ label: columnName, aggregation: null });
      }
    },
    unselectColumn(columnLabel) {
      const index = this.selectedColumns.findIndex((selected) => selected.label === columnLabel);
      if (index !== -1) this.selectedColumns.splice(index, 1);
    },
    isUnsupported(column) {
      // const unsupportedTypes = ["dict", "list", "other", "mixed"];
      // return unsupportedTypes.includes(column.type);
      const supportedTypes = ["text", "number"];
      return !supportedTypes.includes(column.type);
    },
    isColumnSelected(column) {
      if (column.aggregation) return true; // Aggregated columns are considered selected
      return this.selectedColumns.some((selected) => selected.label === column.name);
    },

    // Metrics
    hasColumnMetrics(columnLabel) {
      const entry = this.selectedColumnMetrics.find(
        (metricEntry) => metricEntry.columnLabel === columnLabel
      );
      return entry ? entry.metrics : false;
    },
    openColumnMetricsModal(column) {
      this.selectedColumnForMetrics = column;

      // Reset available metrics selection
      const existingMetrics = this.hasColumnMetrics(column.name);
      if (!existingMetrics) for (const metric of this.availableMetrics) metric.selected = false;
      else
        for (const metric of this.availableMetrics)
          metric.selected = existingMetrics.includes(metric.name);
    },
    selectMetric(metricName) {
      const metric = this.availableMetrics.find((m) => m.name === metricName);
      if (!metric) return;

      // Toggle the selected state of the metric
      metric.selected = !metric.selected;

      this.$forceUpdate();
    },
    applyMetrics() {
      if (!this.selectedColumnForMetrics) return;

      // Unselect the column if it was selected
      if (this.isColumnSelected(this.selectedColumnForMetrics))
        this.unselectColumn(this.selectedColumnForMetrics.name);

      // Remove existing metrics for the column if any
      const existingMetricsIndex = this.selectedColumnMetrics.findIndex(
        (entry) => entry.columnLabel === this.selectedColumnForMetrics.name
      );
      if (existingMetricsIndex !== -1) this.selectedColumnMetrics.splice(existingMetricsIndex, 1);

      // Add the selected metrics for the column
      const metrics = this.availableMetrics
        .filter((metric) => metric.selected)
        .map((metric) => metric.name);

      if (metrics.length > 0) {
        this.selectedColumnMetrics.push({
          columnLabel: this.selectedColumnForMetrics.name,
          metrics,
        });
      }

      this.selectedColumnForMetrics = null;
    },

    // Aggregation
    hasColumnAggregation(columnLabel) {
      const column = this.selectedColumns.find((selected) => selected.label === columnLabel);
      if (!column) return false;
      return column.aggregation;
    },
    openColumnAggregationModal(column) {
      this.selectedColumnForAggregation = column;

      const existingAggregation = this.hasColumnAggregation(column.name);

      if (column.type === "text") {
        this.nbCharacters = existingAggregation?.nbCharacters || 1;
        this.nbCharactersSkip = existingAggregation?.nbCharactersSkip || 0;
      } else if (column.type === "number") {
        this.nbChunks = existingAggregation?.nbChunks || 5;
        this.aggregationType = existingAggregation?.type || "evenRange";
      }
    },
    applyAggregation() {
      if (!this.selectedColumnForAggregation) return;

      // Select the column if not already selected
      if (!this.isColumnSelected(this.selectedColumnForAggregation))
        this.selectColumn(this.selectedColumnForAggregation);

      // Find the column in the selectedColumns array
      const columnIndex = this.selectedColumns.findIndex(
        (selected) => selected.label === this.selectedColumnForAggregation.name
      );
      if (columnIndex === -1) return;

      // Update the selected column with aggregation details
      if (this.selectedColumnForAggregation.type === "number") {
        this.selectedColumns[columnIndex].aggregation = {
          type: this.aggregationType,
          nbChunks: this.nbChunks,
        };
      } else if (this.selectedColumnForAggregation.type === "text") {
        this.selectedColumns[columnIndex].aggregation = {
          type: "firstCharacters",
          nbCharacters: this.nbCharacters,
          nbCharactersSkip: this.nbCharactersSkip,
        };
      }

      this.selectedColumnForAggregation = null;
    },
    removeAggregation(columnLabel) {
      const column = this.selectedColumns.find((selected) => selected.label === columnLabel);
      if (column) column.aggregation = null; // Remove aggregation

      // Unselect the column
      this.unselectColumn(columnLabel);
      this.$forceUpdate();
    },
  },
  computed: {
    columnsGroupedByCategory() {
      const columns = this.columnsStatistics;
      const columnsGroupedByCategory = {};

      for (const column of columns) {
        if (this.isUnsupported(column)) continue;
        const category = column.category || "Other";
        if (!columnsGroupedByCategory[category]) columnsGroupedByCategory[category] = [];
        columnsGroupedByCategory[category].push(column);
      }

      return columnsGroupedByCategory;
    },
    unsupportedColumns() {
      const columns = this.columnsStatistics;
      return columns.filter((column) => this.isUnsupported(column));
    },
  },
};
</script>

<style lang="scss" scoped>
.categories {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;

  .category {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    h3 {
      margin-bottom: 0.5rem;
      border-bottom: 1px solid #ccc;
      text-align: left;
      text-transform: capitalize;
    }

    .columns {
      display: flex;
      flex-wrap: wrap;
      flex-direction: column;
      gap: 0.5rem;

      .column {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;

        .columnDetails {
          display: flex;
          align-items: center;
          gap: 0.5rem;

          button {
            max-width: 300px;
            word-break: break-all;
          }

          .nbUnique {
            font-weight: bold;
          }

          .type {
            &.text {
              color: var(--class);
            }
            &.number {
              color: var(--number);
            }
            &.list {
              color: var(--array);
            }
            &.dict {
              color: var(--dict);
            }
          }

          .statistics {
            display: flex;
            align-items: center;
            gap: 0.3rem;
            color: var(--fontColorLight);
            opacity: 0.5;

            .label {
              font-weight: bold;
            }
          }
        }

        .controls {
          display: flex;
          align-items: center;
          gap: 0.5rem;

          .aggregation {
            display: flex;
            align-items: center;
          }
        }
      }
    }
  }
}

// Modal
.gapped {
  gap: 2rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  #aggregationType {
    margin-left: 0.5rem;
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
  }

  .controls {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding-top: 1rem;

    button {
      svg {
        fill: white;
      }
    }
  }

  .form-group {
    display: flex;
    align-items: center;
    gap: 0.2rem;

    label {
      font-weight: bold;
    }

    input {
      width: 100px;
      padding: 0.2rem;
      border-radius: 4px;
      border: 1px solid #ccc;
    }
  }
}
.controls {
  .metrics {
    svg {
      fill: white;
    }
  }
  .aggregation {
    svg {
      fill: black;
    }
  }
}
</style>
