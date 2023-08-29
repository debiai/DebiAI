<template>
  <div id="ExplorationMode">
    <!-- Header -->
    <Header
      :project="project"
      v-on:refresh="loadProject"
      v-on:deleteProject="deleteProject"
      v-on:backToProjects="backToProjects"
    />

    <!-- Content -->
    <div id="content">
      <ColumnSelectionVue />
      <!-- <AggregationVue /> -->
    </div>
  </div>
</template>

<script>
import Header from "./Header.vue";
import swal from "sweetalert";

// Widgets
import AggregationVue from "./aggregation/Aggregation.vue";
import FilteringVue from "./filtering/Filtering.vue";
import ColumnSelectionVue from "./columnSelection/ColumnSelection.vue";

export default {
  name: "ExplorationMode",
  components: {
    Header,
    AggregationVue,
    FilteringVue,
    ColumnSelectionVue,
  },
  data: () => {
    return {
      // Project
      dataProviderId: null,
      projectId: null,
      project: null,
      loading: false,
    };
  },
  created() {
    // get data-provider ID and project ID from url path or router params
    const dataProviderId = this.$route.params.dataProviderId
      ? this.$route.params.dataProviderId
      : this.$route.query.dataProviderId;
    const projectId = this.$route.params.projectId
      ? this.$route.params.projectId
      : this.$route.query.projectId;

    // Check if we need to start analysis right away
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
          this.nbSelectedSamples = this.project.nbSamples;

          // Sort models and selections by update date
          this.project.selections = this.project.selections.sort(
            (a, b) => b.updateDate - a.updateDate
          );
          this.project.models = this.project.models.sort((a, b) => b.updateDate - a.updateDate);

          // Get the project columns
          // Expected project columns example :
          //  [
          //      { "name": "storage", "category": "other" },
          //      { "name": "age", "category": "context" },
          //      { "name": "path", "category": "input" },
          //      { "name": "label", "category": "groundtruth" },
          //      { "name": "type" }, # category is not specified, it will be "other"
          //  ]
          if (!this.project.columns) this.project.columns = [];

          // Expected project results columns example :
          // [
          //   { name: "Model prediction", type: "number" },
          //   { name: "Model error", type: "number" },
          // ];
          if (!this.project.resultStructure) this.project.resultStructure = [];

          // Store some info
          this.$store.commit("setProjectColumns", this.project.columns);
          this.$store.commit("setProjectResultsColumns", this.project.resultStructure);
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
    deleteProject() {
      swal({
        title: "Delete the project ?",
        text: "Do you really want to delete the project ? There is no way back.",
        buttons: true,
        icon: "warning",
        dangerMode: true,
      }).then((validate) => {
        if (validate)
          this.$backendDialog
            .deleteProject()
            .then(() => {
              this.$store.commit("sendMessage", {
                title: "success",
                msg: "Project deleted",
              });
              this.$router.push("/");
            })
            .catch((e) => {
              console.log(e);
              this.$store.commit("sendMessage", {
                title: "error",
                msg: "Could not delete the project",
              });
            });
      });
    },
    backToProjects() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped lang="scss">
#ExplorationMode {
  height: 100%;
  display: flex;
  flex-direction: column;
}

#header {
  display: flex;
  align-items: center;
  color: white;
  padding: 2px;
  background-color: var(--primary);
}

#debiaiMenuLogo {
  display: flex;
  justify-content: center;
  align-items: center;
  background: red;
  color: #fff;
  text-decoration: none;
  background: none;
}

#title2 {
  align-self: center;
}

#title3 {
  align-self: center;
  padding-top: 9px;
}

#content {
  flex: 1;
  height: 100%;
}
</style>
