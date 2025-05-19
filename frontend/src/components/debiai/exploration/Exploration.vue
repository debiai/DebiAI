<template>
  <div id="Exploration">
    <!-- Header -->
    <ExplorationHeader
      :project="project"
      :exploration="exploration"
      v-on:refresh="loadProjectAndExploration"
    />

    <!-- Content -->
    {{ explorationId }}
    {{ exploration }}
  </div>
</template>

<script>
import ExplorationHeader from "./ExplorationHeader";

export default {
  name: "Exploration",
  props: {},
  components: {
    ExplorationHeader,
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
        await Promise.all([this.loadProject(), this.loadExploration()]);
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
  },
  computed: {},
};
</script>

<style lang="scss" scoped>
#Exploration {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
}
</style>
