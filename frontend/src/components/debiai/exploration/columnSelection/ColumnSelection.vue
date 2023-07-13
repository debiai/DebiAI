<template>
  <div id="ColumnSelection">
    <div id="top">
      <h3 id="title">Select the columns you want to use for the exploration:</h3>
      <button
        :disabled="selectedColumnsIndex.length === 0"
        @click="proceed"
      >
        Proceed >
      </button>
    </div>
    <div
      id="columns"
      class="card"
    >
      <ProjectColumns
        :columns="projectColumns"
        :selectedColumnsIndex="selectedColumnsIndex"
        title=""
        selectable
        @selectedColumnsIndexUpdate="selectedColumnsIndex = $event"
      />
    </div>
  </div>
</template>

<script>
import ProjectColumns from "../../project/projectColumns/ProjectColumns.vue";

export default {
  components: { ProjectColumns },
  data() {
    return {
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

    // Expected project columns example :
    //  [
    //      { "name": "storage", "category": "other" },
    //      { "name": "age", "category": "context" },
    //      { "name": "path", "category": "input" },
    //      { "name": "label", "category": "groundtruth" },
    //      { "name": "type" }, # category is not specified, it will be "other"
    //  ]

    if (this.projectColumns.length === 0) {
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

    const providedSelectedColumnsIndex = this.$route.query.selectedColumnsIndex;
    if (providedSelectedColumnsIndex) {
      // If the selected columns index is provided, we use it
      this.selectedColumnsIndex = providedSelectedColumnsIndex;
    }
  },
  methods: {
    proceed() {
      // Go to the aggregation page
      this.$router.push({
        name: "aggregation",
        query: {
          projectId: this.$route.query.projectId,
          dataProviderId: this.$route.query.dataProviderId,
          selectedColumnsIndex: this.selectedColumnsIndex,
        },
      });
    },
  },
  computed: {
    // selectedColumns() {
    //   return this.selectedColumnsIndex.map((index) => this.projectColumns[index]);
    // },
  },
};
</script>

<style scoped lang="scss">
#ColumnSelection {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: center;

  #top {
    max-width: 800px;
    width: 90%;
    margin: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  #columns {
    max-width: 800px;
    width: 90%;
    margin: 20px;
    padding: 10px;
  }
}
</style>
