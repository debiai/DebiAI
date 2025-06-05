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
                <inline-svg
                  :src="require('@/assets/svg/data.svg')"
                  width="30"
                  height="30"
                />
                <strong>{{ project.nbSamples }} </strong>
                <div>Project samples</div>
              </div>
              <div class="combinationsDisplay theoreticalCombinations">
                <div>
                  <inline-svg
                    :src="require('@/assets/svg/theoreticalCombinations.svg')"
                    width="30"
                    height="30"
                  />
                  <transition name="highlight">
                    <strong :key="theoreticalCombinations">{{ theoreticalCombinations }}</strong>
                  </transition>
                  <div>Theoretical combinations</div>
                </div>
                <button
                  :disabled="reasonNotReadyToComputeRealCombinations"
                  :title="reasonNotReadyToComputeRealCombinations"
                >
                  Compute real combinations
                </button>
              </div>
              <div class="combinationsDisplay realCombinations">
                <div>
                  <inline-svg
                    :src="require('@/assets/svg/realCombinations.svg')"
                    width="30"
                    height="30"
                  />
                  <strong v-if="realCombinations === null">?</strong>
                  <strong v-else>{{ realCombinations }} combinations</strong>
                  <div>Real combinations</div>
                </div>
                <button :disabled="!realCombinations">Start combination analysis</button>
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
          if (this.exploration.config) {
            this.selectedColumns = this.exploration.config.selectedColumns || [];
          }

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
    async updateExplorationConfig() {
      if (!this.exploration) return;
      this.exploration.config.selectedColumns = this.selectedColumns;
      return this.$explorationDialog
        .updateExplorationConfig(this.projectId, this.exploration.id, this.exploration.config)
        .then(() => {})
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error while updating exploration",
          });
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
    reasonNotReadyToComputeRealCombinations() {
      if (this.theoreticalCombinations <= 0) return "No columns selected";
      if (this.theoreticalCombinations > 10000) return "Too many combinations";
      if (this.theoreticalCombinations >= this.project.nbSamples) return "Too many combinations";
      return null;
    },
  },
  watch: {
    selectedColumns: {
      handler() {
        this.updateExplorationConfig();
      },
      deep: true,
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
        .projectNbSamples {
          display: flex;
          justify-content: flex-start;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          margin: 0.5rem;
        }

        .combinationsDisplay {
          display: flex;
          justify-content: space-between;
          padding: 0.5rem 1rem;
          margin: 0.5rem;
          border: 1px solid #ccc;
          border-radius: 5px;

          div {
            display: flex;
            justify-content: flex-start;
            align-items: center;
            gap: 0.5rem;
          }
        }
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

.highlight-enter-active {
  animation: highlightChange 0.5s ease-in-out;
}

@keyframes highlightChange {
  0% {
    transform: scale(1.3) translateY(-2px) rotate(5deg);
  }
  100% {
    transform: scale(1);
  }
}
</style>
