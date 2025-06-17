<template>
  <div class="categories">
    <!-- Columns category -->
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
          <div>
            <!-- Btn -->
            <button
              @click="selectColumn(column)"
              :class="{
                selected: isColumnSelected(column),
                disabled: hasColumnAggregation(column.name),
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
          </div>

          <!-- Controls -->
          <div class="controls">
            <!-- Aggregation -->
            <button
              @click="openColumnAggregationModal(column)"
              v-if="column.type === 'number' && !hasColumnAggregation(column.name)"
              title="Reduce the number dimensions with aggregation"
              class="borderlessHover"
            >
              <inline-svg
                :src="require('@/assets/svg/aggregation.svg')"
                height="16"
                width="16"
              />
              Aggregate
            </button>

            <!-- Aggregation info -->
            <div
              v-if="hasColumnAggregation(column.name)"
              class="aggregation"
            >
              <inline-svg
                :src="require('@/assets/svg/aggregation.svg')"
                height="16"
                width="16"
              />
              <span>
                {{ hasColumnAggregation(column.name).nbChunks }} chunks

                <!-- ({{
                  column.aggregation.type === "evenQuantity" ? "Even quantity" : "Even range"
                }}) -->
              </span>
              <button
                class="red"
                @click="removeAggregation(column.name)"
                title="Remove aggregation"
              >
                x
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
            <option value="evenQuantity">Even quantity</option>
            <option value="evenRange">Even range</option>
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
  },
  data() {
    return {
      // Number column aggregation
      selectedColumnForAggregation: null,
      nbChunks: 5,
      aggregationType: "evenQuantity",
    };
  },
  methods: {
    selectColumn(column) {
      if (this.isUnsupported(column)) return;
      if (column.aggregation) return;

      const columnName = column.name;
      const existingColumn = this.selectedColumns.find((selected) => selected.label === columnName);

      if (existingColumn) {
        // If the column is already selected, unselect it
        this.selectedColumns.splice(this.selectedColumns.indexOf(existingColumn), 1);
      } else {
        this.selectedColumns.push({ label: columnName, aggregation: null, column_metrics: [] });
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
    hasColumnAggregation(columnLabel) {
      const column = this.selectedColumns.find((selected) => selected.label === columnLabel);
      if (!column) return false;
      return column.aggregation;
    },
    openColumnAggregationModal(column) {
      this.selectedColumnForAggregation = column;
      // Reset form to default value
      this.nbChunks = 5;
      this.aggregationType = "evenQuantity";
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
      this.selectedColumns[columnIndex].aggregation = {
        type: this.aggregationType,
        nbChunks: this.nbChunks,
      };

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

        div {
          display: flex;
          align-items: center;
          gap: 0.5rem;

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
        }

        .statistics {
          color: var(--fontColorLight);

          .label {
            font-weight: bold;
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
  }
}
</style>
