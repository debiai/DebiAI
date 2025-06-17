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
        <!-- Columns -->
        <div
          id="columns"
          class="card"
        >
          <div class="title">
            <h2>Project columns</h2>
          </div>
          <div class="columns">
            <columns
              :project="project"
              :exploration="exploration"
              :columnsStatistics="columnsStatistics"
              :selectedColumns="selectedColumns"
            />
          </div>
        </div>
        <!-- Combinations and Metrics -->
        <div id="right">
          <!-- Combinations -->
          <div
            id="combinations"
            class="card"
          >
            <div class="title">
              <h2>Combinations</h2>
            </div>
            <div class="content">
              <!-- Nb samples -->
              <div class="projectNbSamples">
                <inline-svg
                  :src="require('@/assets/svg/data.svg')"
                  width="33"
                  height="30"
                />
                <strong>{{ project.nbSamples }} </strong>
                <div>Project samples</div>
              </div>
              <!-- Theoretical -->
              <div class="theoreticalCombinations">
                <!-- Icon, title & number -->
                <div class="combinationsDisplay">
                  <div>
                    <inline-svg
                      :src="require('@/assets/svg/theoreticalCombinations.svg')"
                      width="35"
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
                    @click="computeRealCombinations"
                  >
                    Compute real combinations
                  </button>
                </div>

                <!-- Ongoing exploration display -->
                <ComputationStatus
                  :exploration="exploration"
                  :project="project"
                  @cancelled="loadExploration()"
                />
              </div>

              <!-- Real Combinations -->
              <div class="realCombinations">
                <div>
                  <inline-svg
                    :src="require('@/assets/svg/realCombinations.svg')"
                    width="35"
                    height="30"
                  />
                  <strong v-if="exploration.real_combinations === null">?</strong>
                  <strong v-else>{{ exploration.real_combinations }} combinations</strong>
                  <div>Real combinations</div>
                </div>
                <button
                  :disabled="!exploration.real_combinations || exploration.state !== 'completed'"
                  @click="startCombinationAnalysis"
                >
                  Start combination analysis
                </button>
              </div>
            </div>
          </div>

          <!-- Metrics -->
          <div
            id="metrics"
            class="card"
          >
            <div class="title">
              <h2>Metrics</h2>
            </div>
            <div class="content">
              <Metrics
                :project="project"
                :exploration="exploration"
                :selectedSampleMetrics="selectedSampleMetrics"
              />
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import ExplorationHeader from "./ExplorationHeader";
import ComputationStatus from "./ComputationStatus";
import Columns from "./Columns";
import Metrics from "./Metrics.vue";

export default {
  name: "Exploration",
  props: {},
  components: {
    ExplorationHeader,
    ComputationStatus,
    Columns,
    Metrics,
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
      selectedSampleMetrics: ["Nb Samples"],

      // Combinations
      realCombinations: null,

      // Other
      explorationRefreshInterval: null,
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
    async loadExploration(clearPrevious = true, updateColumns = true) {
      if (clearPrevious) this.exploration = null;

      return this.$explorationDialog
        .getExploration(this.projectId, this.explorationId, updateColumns)
        .then((exploration) => {
          this.exploration = exploration;
          if (this.exploration.config && updateColumns) {
            this.selectedColumns = this.exploration.config.selectedColumns || [];
            this.selectedSampleMetrics = this.exploration.config.selectedSampleMetrics || [
              "Nb Samples",
            ];
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

          // If the exploration is ongoing, start the refresh interval
          if (this.exploration.state === "ongoing") this.startExplorationRefreshInterval();
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
      this.exploration.config.selectedSampleMetrics = this.selectedSampleMetrics;
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
    async computeRealCombinations() {
      try {
        const exploration = await this.$explorationDialog.computeRealCombinations(
          this.projectId,
          this.explorationId,
          this.exploration.config
        );
        this.exploration = exploration;

        // Start the exploration refresh interval to update the exploration data
        this.startExplorationRefreshInterval();
      } catch (e) {
        console.log(e);
        this.$store.commit("sendMessage", {
          title: "error",
          msg: "Error while starting the real combinations computation",
        });
      }
    },
    startExplorationRefreshInterval() {
      // Refresh the exploration data every second
      if (this.explorationRefreshInterval) clearInterval(this.explorationRefreshInterval);
      this.explorationRefreshInterval = setInterval(() => {
        this.loadExploration(false, false).then(() => {
          // Stop refreshing if the exploration computation is done
          if (this.exploration.state !== "ongoing") {
            clearInterval(this.explorationRefreshInterval);
            this.explorationRefreshInterval = null;

            if (this.exploration.state === "completed") {
              this.$store.commit("sendMessage", {
                title: "success",
                msg: "Exploration computation completed successfully",
              });
            } else if (this.exploration.state === "error") {
              this.$store.commit("sendMessage", {
                title: "error",
                msg: "Exploration computation failed",
              });
            }
          }
        });
      }, 1000);
    },
    startCombinationAnalysis() {
      if (this.exploration.state !== "completed" || !this.exploration.combinations) return;

      this.$router.push({
        name: "dataAnalysis",
        query: {
          dataProviderId: this.dataProviderId,
          projectId: this.projectId,
          explorationId: this.exploration.id,
        },
        params: { exploration: this.exploration },
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
      if (this.theoreticalCombinations > 1000000) return "Too many combinations";
      if (this.exploration.state === "ongoing")
        return "Exploration is ongoing, please wait until it is finished";
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
  beforeDestroy() {
    if (this.explorationRefreshInterval) clearInterval(this.explorationRefreshInterval);
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

      .columns {
        overflow-y: auto;
      }
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

        .theoreticalCombinations {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          margin: 0.5rem;
          border: 1px solid #ccc;
          border-radius: 5px;

          .combinationsDisplay {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;

            div {
              display: flex;
              justify-content: flex-start;
              align-items: center;
              gap: 0.5rem;
            }
          }
        }
        .realCombinations {
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
