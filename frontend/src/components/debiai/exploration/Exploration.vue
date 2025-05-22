<template>
  <div id="Exploration">
    <!-- Header -->
    <ExplorationHeader
      :project="project"
      :exploration="exploration"
      v-on:refresh="loadProjectAndExploration"
    />

    <!-- Content -->
    <transition
      name="fade"
      mode="out-in"
    >
      <div
        id="content"
        v-if="project && exploration && columnsStatistics"
      >
        <div
          id="columns"
          class="card"
        >
          <div class="title">
            <h2>Project columns</h2>
          </div>
          <columns
            :project="project"
            :exploration="exploration"
            :columnsStatistics="columnsStatistics"
            :selectedColumns="selectedColumns"
          />
        </div>
        <div id="right">
          <div
            id="combinations"
            class="card"
          >
            <div class="title">
              <h2>Combinations</h2>
            </div>
            <div class="content">
              <div class="projectNbSamples">
                <div>
                  <strong>Project</strong>
                </div>
                <div>{{ project.nbSamples }} samples</div>
              </div>
              <div class="theoreticalCombinations">
                <div>
                  <strong>Theoretical combinations</strong>
                </div>
                <div>{{ theoreticalCombinations }} combinations</div>
              </div>
              <div class="realCombinations">
                <div>
                  <strong>Real combinations</strong>
                </div>
                <div v-if="realCombinations === null">?</div>
                <div v-else>{{ realCombinations }} combinations</div>
              </div>
            </div>
          </div>
          <div
            id="metrics"
            class="card"
          >
            <div class="title">
              <h2>Metrics</h2>
            </div>
            <div class="content">
              <div>Metrics content goes here.</div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import ExplorationHeader from "./ExplorationHeader";
import Columns from "./Columns";

export default {
  name: "Exploration",
  props: {},
  components: {
    ExplorationHeader,
    Columns,
  },
  data: () => {
    return {
      // Project
      dataProviderId: null,
      projectId: null,
      project: null,

      // Exploration
      explorationId: null,
      exploration: null,
      columnsStatistics: null,
      columnsStatisticsStatus: null,
      selectedColumns: [],

      // Combinations
      realCombinations: null,
    };
  },
  created() {
    // Get data-provider ID and project ID from url path or router params
    let dataProviderId = this.$route.params.dataProviderId
      ? this.$route.params.dataProviderId
      : this.$route.query.dataProviderId;
    let projectId = this.$route.params.projectId
      ? this.$route.params.projectId
      : this.$route.query.projectId;
    let explorationId = this.$route.params.explorationId
      ? this.$route.params.explorationId
      : this.$route.query.explorationId;

    if (dataProviderId && projectId) {
      this.dataProviderId = dataProviderId;
      this.projectId = projectId;
      this.$store.commit("setDataProviderId", dataProviderId);
      this.$store.commit("setProjectId", projectId);

      if (explorationId) this.explorationId = explorationId;
      else
        this.$router.push({
          name: "explorations",
          params: {
            dataProviderId,
            projectId,
          },
        });

      // Load data-provider info
      this.$backendDialog.getSingleDataInfo().then((dataInfo) => {
        this.$store.commit("setDataProviderInfo", dataInfo);
      });

      // Load the project and exploration data
      this.loadProjectAndExploration();
    } else {
      this.$router.push("/");
    }
  },
  methods: {
    async loadProjectAndExploration() {
      try {
        await Promise.all([
          this.loadProject(),
          this.loadExploration(),
          this.loadColumnsStatistics(),
        ]);
      } catch (e) {
        console.log(e);
      }
    },
    async loadProject() {
      this.project = null;
      return this.$backendDialog
        .getProject()
        .then((project) => {
          this.project = project;

          // Change the browser title
          if (this.project.name) document.title = this.project.name;
          else document.title = this.project.id;
        })
        .catch((e) => {
          if (e.response && e.response.status === 500) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Internal server error while loading project",
            });
          } else if (e.response && e.response.status === 404) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Project not found",
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error while loading project",
            });
          }
          console.log(e);
          this.$router.push("/");
        });
    },
    async loadExploration() {
      this.exploration = null;
      return this.$explorationDialog
        .getExploration(this.projectId, this.explorationId)
        .then((exploration) => {
          this.exploration = exploration;
          if (!this.exploration) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Exploration not found",
            });
            this.$router.push({
              name: "explorations",
              params: {
                dataProviderId: this.dataProviderId,
                projectId: this.projectId,
              },
            });
          }
        })
        .catch((e) => {
          console.log(e);
        });
    },
    async loadColumnsStatistics() {
      this.columnsStatistics = null;
      return this.$explorationDialog
        .getColumnsStatistics(this.dataProviderId, this.projectId)
        .then((columnsStatisticsResult) => {
          if (columnsStatisticsResult.columns)
            this.columnsStatistics = columnsStatisticsResult.columns;
          else this.columnsStatistics_status = columnsStatisticsResult.status;
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  computed: {
    theoreticalCombinations() {
      if (this.selectedColumns.length === 0) return 0;
      let combinations = 1;
      for (let i = 0; i < this.selectedColumns.length; i++) {
        const columnNbUniqueValues = this.columnsStatistics.find(
          (column) => column.name === this.selectedColumns[i]
        ).nbUniqueValues;
        combinations *= columnNbUniqueValues;
      }
      return combinations;
    },
  },
};
</script>

<style lang="scss" scoped>
#Exploration {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;

  #content {
    display: flex;
    flex: 1;
    flex-direction: row;
    overflow: hidden;

    #columns {
      flex: 1;
    }

    #right {
      flex: 1;
      display: flex;
      flex-direction: column;

      #combinations {
        flex: 1;
      }
      #metrics {
        flex: 1;
      }
    }
    .card {
      border-radius: 5px;
    }
  }
}
</style>
