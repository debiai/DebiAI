<template>
  <div id="Explorations">
    <!-- Header -->
    <Header
      :project="project"
      v-on:refresh="loadProjectAndExplorations"
    />

    <!-- New exploration modal -->
    <Modal
      v-if="newExploration"
      @close="newExploration = false"
    >
      <h2 class="aligned spaced">
        New exploration
        <button
          class="red"
          @click="newExploration = false"
        >
          Close
        </button>
      </h2>
      <form
        @submit.prevent="createExploration"
        class="exploration-form"
      >
        <div class="form-group">
          <label for="exploration-name">Exploration name</label>
          <input
            type="text"
            id="exploration-name"
            v-model="explorationName"
            required
          />
        </div>
        <div class="form-group">
          <label for="exploration-description">Description</label>
          <textarea
            id="exploration-description"
            v-model="explorationDescription"
          ></textarea>
        </div>
        <button
          type="submit"
          class="green"
          :disabled="!newExplorationFormValid"
        >
          Create exploration
        </button>
      </form>
    </Modal>

    <!-- Header & new explorations btn -->
    <div class="explorations-header">
      <h2>Explorations</h2>
      <button
        class="green"
        @click="newExploration = true"
      >
        Create new exploration
      </button>
    </div>

    <!-- Explorations -->
    <transition name="fade">
      <div
        class="explorations itemList"
        v-if="project && explorations"
      >
        <exploration-card
          v-for="exploration in explorations"
          :key="exploration.id"
          :exploration="exploration"
          :project="project"
          @edit="editExploration"
          @delete="deleteExploration"
          @refresh="loadExplorations"
        />
      </div>
    </transition>

    <!-- No explorations -->
    <div
      v-if="explorations !== null && explorations.length === 0"
      class="no-explorations"
    >
      <p>No explorations found.</p>
      <p>Click the button above to create a new exploration.</p>
    </div>
  </div>
</template>

<script>
import Header from "./Header";
import ExplorationCard from "./ExplorationCard.vue";

export default {
  name: "Explorations",
  props: {},
  components: {
    Header,
    ExplorationCard,
  },
  data: () => {
    return {
      // Project
      dataProviderId: null,
      projectId: null,
      project: null,

      // NewExploration
      newExploration: false,
      explorationName: "",
      explorationDescription: "",

      // Explorations
      explorations: null,
      explorationsRefreshInterval: null,
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

    if (dataProviderId && projectId) {
      this.dataProviderId = dataProviderId;
      this.projectId = projectId;
      this.$store.commit("setDataProviderId", dataProviderId);
      this.$store.commit("setProjectId", projectId);

      // Load data-provider info
      this.$backendDialog.getSingleDataInfo().then((dataInfo) => {
        this.$store.commit("setDataProviderInfo", dataInfo);
      });

      // Load the project and explorations data
      this.loadProjectAndExplorations();
    } else {
      console.log("No project ID or no data provider ID");
      this.$router.push("/");
    }
  },
  methods: {
    loadProjectAndExplorations() {
      Promise.all([this.loadProject(), this.loadExplorations()]).catch((e) => {
        console.log(e);
      });
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
    async loadExplorations() {
      this.explorations = null;
      return this.$explorationDialog
        .getExplorations(this.projectId)
        .then((explorations) => {
          this.explorations = explorations;

          if (this.explorationsRefreshInterval) clearInterval(this.explorationsRefreshInterval);

          // Check if explorations are ongoing and set an interval to refresh them
          if (this.explorations.some((exploration) => exploration.state === "ongoing")) {
            this.explorationsRefreshInterval = setInterval(() => {
              this.$explorationDialog.getExplorations(this.projectId).then((explorations) => {
                this.explorations = explorations;

                // If no ongoing explorations, clear the interval
                if (!this.explorations.some((exploration) => exploration.state === "ongoing")) {
                  clearInterval(this.explorationsRefreshInterval);
                  this.explorationsRefreshInterval = null;
                }
              });
            }, 1000);
          }
        })

        .catch((e) => {
          console.log(e);
        });
    },

    createExploration() {
      this.$explorationDialog
        .createExploration(this.projectId, this.explorationName, this.explorationDescription)
        .then(() => {
          this.loadExplorations();
          this.newExploration = false;
          this.explorationName = "";
          this.explorationDescription = "";
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Exploration created successfully",
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error while creating exploration",
          });
        });
    },
    editExploration({ explorationId, isMiddleClick }) {
      if (isMiddleClick) {
        this.$router.push({
          name: "exploration",
          params: {
            dataProviderId: this.dataProviderId,
            projectId: this.projectId,
            explorationId: explorationId,
          },
        });
      } else {
        this.$router.push({
          name: "exploration",
          params: {
            dataProviderId: this.dataProviderId,
            projectId: this.projectId,
            explorationId: explorationId,
          },
        });
      }
    },
    deleteExploration(explorationId) {
      this.$explorationDialog
        .deleteExploration(this.projectId, explorationId)
        .then(() => {
          this.loadExplorations();
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Exploration deleted successfully",
          });
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Error while deleting exploration",
          });
        });
    },
  },
  computed: {
    newExplorationFormValid() {
      return this.explorationName;
    },
  },
};
</script>

<style lang="scss" scoped>
#Explorations {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;

  .explorations-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    width: 100%;
    max-width: 1000px;
    padding-top: 30px;

    h2 {
      font-size: 24px;
      font-weight: bold;
    }
  }

  .explorations {
    padding: 20px;
    width: 100%;
    max-width: 1000px;

    .no-explorations {
      text-align: center;
      font-size: 18px;
      color: #666;
    }
  }
}
.no-explorations {
  margin-top: 20px;
}

.exploration-form {
  display: flex;
  flex-direction: column;
  width: 400px;
  gap: 20px;

  .form-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;

    label {
      font-weight: bold;
    }

    input,
    textarea {
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
      width: 378px;
    }
  }
}
</style>
