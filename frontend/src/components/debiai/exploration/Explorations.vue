<template>
  <div id="Explorations">
    <!-- Header -->
    <Header
      :project="project"
      v-on:settings="settings = !settings"
      v-on:refresh="loadProject"
      v-on:deleteProject="deleteProject"
      v-on:backToProjects="backToProjects"
    />
  </div>
</template>

<script setup>
import Header from "./Header";

export default {
  name: "Explorations",
  props: {},
  components: {
    Header,
  },
  data: () => {
    return {
      dataProviderId: null,
      projectId: null,
      project: null,
      loading: false,
      settings: false,

      // Explorations
      explorations: null,
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

      // Load the project data
      this.loadProject();
    } else {
      console.log("No project ID or no data provider ID");
      this.$router.push("/");
    }
  },
  methods: {
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
    backToProjects() {
      this.$router.push({
        name: "projects",
        params: {
          dataProviderId: this.dataProviderId,
        },
      });
    },
    deleteProject() {
      return;
    },
  },
};
</script>

<style></style>
