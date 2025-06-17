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
      this.$emit("selectSampleMetrics", this.selectedSampleMetrics);
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
}
</style>
