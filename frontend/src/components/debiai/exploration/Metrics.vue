<template>
  <div class="combinationsMetrics">
    <div class="sampleMetrics">
      <h3>Sample Metrics</h3>
      <div class="metrics">
        <div
          v-for="metric in sampleMetrics"
          :key="metric.name"
          class="metric"
        >
          <button
            class="name"
            :class="{ selected: selectedSampleMetrics.includes(metric.name) }"
            @click="selectSampleMetric(metric)"
            :disabled="metric.name === 'Nb Samples'"
          >
            {{ metric.name }}
          </button>

          <span class="description">{{ metric.description }}</span>
        </div>
      </div>

      <h3>Column Metrics</h3>
      <div class="columnsMetrics">
        <div
          v-for="columnMetric in selectedColumnMetrics"
          :key="columnMetric.columnLabel"
          class="metricColumn"
        >
          <div class="columnName">{{ columnMetric.columnLabel }}:</div>
          <div class="columnMetrics">
            <div
              v-for="metric in columnMetric.metrics"
              :key="metric"
              class="metric"
            >
              {{ metric }}
              <button
                class="remove red"
                @click="removeMetricFromColumn(columnMetric.columnLabel, metric)"
                :disabled="metric === 'Nb Samples'"
              >
                &times;
              </button>
              <span v-if="columnMetric.metrics.indexOf(metric) !== columnMetric.metrics.length - 1"
                >,</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Metrics",
  props: {
    project: {
      type: Object,
      required: true,
    },
    exploration: {
      type: Object,
      required: true,
    },
    selectedSampleMetrics: {
      type: Array,
      required: true,
    },
    selectedColumnMetrics: {
      type: Array,
      required: true,
      // [{columnLabel: "Column Name", metrics: ["Metric1", "Metric2"]}, ...]
    },
  },
  data() {
    return {
      sampleMetrics: [
        { name: "Nb Samples", description: "Total number of samples for each combinations." },
      ],
    };
  },
  methods: {
    selectSampleMetric(metric) {
      // "Nb Samples" can be unselected
      if (metric.name === "Nb Samples") return;

      const index = this.selectedSampleMetrics.indexOf(metric.name);
      if (index > -1) {
        // Metric is already selected, remove it
        this.selectedSampleMetrics.splice(index, 1);
      } else {
        // Metric is not selected, add it
        this.selectedSampleMetrics.push(metric.name);
      }
    },
    removeMetricFromColumn(columnLabel, metric) {
      const column = this.selectedColumnMetrics.find((col) => col.columnLabel === columnLabel);
      if (column) {
        const index = column.metrics.indexOf(metric);
        if (index > -1) column.metrics.splice(index, 1);
      }

      // If the column has no metrics left, we could remove the column entirely if needed
      if (column && column.metrics.length === 0) {
        const columnIndex = this.selectedColumnMetrics.indexOf(column);
        if (columnIndex > -1) this.selectedColumnMetrics.splice(columnIndex, 1);
      }
    },
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
.combinationsMetrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;

  .sampleMetrics {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    h3 {
      text-align: left;
      width: 100%;
      border-bottom: 1px solid #ccc;
      padding-bottom: 0.5rem;
      margin-bottom: 0.5rem;
    }

    .metrics {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;

      .metric {
        display: flex;
        gap: 0.5rem;
        align-items: center;
      }
    }
  }

  .columnsMetrics {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    .metricColumn {
      display: flex;
      align-items: center;
      gap: 0.5rem;

      .columnName {
        font-weight: bold;
      }

      .columnMetrics {
        flex: 1;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        border: 1px solid #ccc;
        padding: 0.5rem;
        border-radius: 4px;
      }
    }
  }
}
</style>
