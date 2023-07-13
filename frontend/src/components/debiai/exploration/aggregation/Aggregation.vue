<template>
  <div id="Aggregation">
    <div id="top">
      <button @click="back">&lt; Column selection</button>
      <h3 id="title">
        Select the metrics used for the exploration and aggregate the columns if needed:
      </h3>
      <button>Proceed ></button>
    </div>
    <div
      id="metricSelection"
      class="card"
    >
      <h4>Available metrics:</h4>
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      metrics: ["Samples number"],
      selectedMetrics: ["Samples number"],
      projectColumns: [],
      selectedColumnsIndex: [],
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
  },
  methods: {
    selectMetric(metric) {
      if (this.selectedMetrics.includes(metric)) {
        this.selectedMetrics = this.selectedMetrics.filter((m) => m !== metric);
      } else {
        this.selectedMetrics.push(metric);
      }
    },

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
    margin: 20px;
    padding: 30px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;

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
}
</style>
