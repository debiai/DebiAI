<template>
  <div id="project">
    <!-- Settings modal -->
    <Modal v-if="settings && project">
      <!-- block structure creation or display -->
      <h2 class="aligned spaced">
        Block structure
        <button class="red" @click="settings = false">Close</button>
      </h2>
      <BlockStructrureCreation :projectId="project.id" v-on:create="createBlockLevels" />
      <!-- TODO results structure -->

      <!-- Tags -->
      <tags :project="project" />
    </Modal>

    <!-- ProjectInfo -->
    <ProjectInfo :project="project" v-on:settings="settings = !settings" v-on:refresh="loadProject"
      v-on:deleteProject="deleteProject" />
    <transition name="fade">
      <div id="projectContent" v-if="project">
        <div id="selectionAndModels">
          <!-- Data selection selection -->
          <Selections :project="project" :nbSelectedSamples="nbSelectedSamples"
            v-on:selectionSelected="selectionSelected" v-on:selectionDeleted="selectionDeleted"
            v-on:setSelectionIntersection="(si) => (selectionIntersection = si)" v-on:newSelection="loadProject" />

          <!-- Model selection -->
          <Models :project="project" :nbEvaluatedSamples="nbEvaluatedSamples" :nbSelectedSamples="nbSelectedSamples"
            :nbResults="nbResults" v-on:modelSelected="modelSelected" v-on:modelDeleted="modelDeleted"
            v-on:setCommomModelResults="(cmr) => (commomModelResults = cmr)" />
        </div>

        <!-- Start analysis -->
        <Analysis :disabled="!readyToAnalyse" v-on:startAnalysis="startAnalysis" />
      </div>
    </transition>
  </div>
</template>

<script>
// Components
import ProjectInfo from "./ProjectInfo";
import BlockStructrureCreation from "./blockStructure/BlockStructrureCreation.vue";
import Models from "./Models.vue";
import Selections from "./selections/Selections.vue";
import Tags from "./tags/Tags.vue";
import Analysis from "./Analysis.vue";

// Services
import dataLoader from "../../../services/dataLoader";
import swal from "sweetalert";

export default {
  name: "Project",
  components: {
    ProjectInfo,
    BlockStructrureCreation,
    Models,
    Selections,
    Tags,
    Analysis,
  },
  data: () => {
    return {
      projectId: null,
      project: null,
      loading: false,
      settings: false,

      // Analysis
      //    Selections
      selectedSelectionsIds: [],
      selectionIntersection: true,
      nbSelectedSamples: 0,
      //    Models
      selectedModelIds: [],
      commomModelResults: true,
      nbEvaluatedSamples: 0,
      nbResults: 0,
    };
  },
  created() {
    // get project ID from url path or router params
    let projectId = this.$route.params.projectId
      ? this.$route.params.projectId
      : this.$route.query.projectId;
    let startAns = this.$route.query.startAnalysis;

    if (projectId) {
      // Load the project data
      this.projectId = projectId;
      this.loadProject().then(() => {
        if (startAns) {
          console.log("Start analysis");
          let selectionIds = this.$route.query.selectionIds;
          let selectionIntersection = this.$route.query.selectionIntersection;
          let modelIds = this.$route.query.modelIds;
          let commomModelResults = this.$route.query.commomModelResults;

          // Convert str to lists
          if (selectionIds) selectionIds = selectionIds.split(".");
          if (modelIds) modelIds = modelIds.split(".");

          // Convert str to Boolean
          selectionIntersection = selectionIntersection === true;
          commomModelResults = commomModelResults === true;

          // Start analysis
          this.loadTree({
            projectId,
            selectionIds,
            selectionIntersection,
            modelIds,
            commomModelResults,
          });
        }
      });
    } else this.$router.push("/");
  },
  methods: {
    async loadProject() {
      this.project = null;
      return this.$backendDialog
        .getProject(this.projectId)
        .then((project) => {
          this.project = project;
          this.nbSelectedSamples = this.project.nbSamples;

          // Sort models and selections by update date
          this.project.selections = this.project.selections.sort(
            (a, b) => b.updateDate - a.updateDate
          );
          this.project.models = this.project.models.sort(
            (a, b) => b.updateDate - a.updateDate
          );

          // store some info
          this.$store.commit("setProjectId", this.project.id);
          this.$store.commit("setBlockLevels", this.project.blockLevelInfo);
        })
        .catch((e) => {
          console.log(e);
          this.$router.push("/");
        });
    },
    createBlockLevels(levelsInfo) {
      this.blockLevelCreation = false;
      this.project.blockLevelInfo = levelsInfo;
    },

    // Analysis Parameters

    selectionSelected(selectedSelectionsIds) {
      this.selectedSelectionsIds = selectedSelectionsIds;
      this.updateNbSamples();
    },
    modelSelected(selectedModelIds) {
      this.selectedModelIds = selectedModelIds;
      this.updateNbSamples();
    },
    updateNbSamples() {
      // Let the backend told us the common or grouped selections and evaluations
      this.loading = true;
      this.$backendDialog
        .getProjectSamples(this.project.id, {
          selectionIds: this.selectedSelections.map((s) => s.id),
          selectionIntersection: this.selectionIntersection,
          modelIds: this.selectedModels.map((m) => m.id),
          commonResults: this.commomModelResults,
        })
        .finally(() => (this.loading = false))
        .then((res) => {
          this.nbSelectedSamples = res.nbFromSelection;
          this.nbEvaluatedSamples = res.nbSamples;
          if (this.commomModelResults)
            this.nbResults = res.nbSamples * this.selectedModels.length;
          else this.nbResults = null; // Will draw a "?" on the dashboard
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Something went wrong while counting ",
          });
          this.loadProject();
        });
    },

    // Analysis start
    startAnalysis({ newTab }) {
      if (newTab) {
        let routeData = this.$router.resolve({
          path: "/project/" + this.projectId,
          query: {
            selectionIds: this.selectedSelectionsIds,
            selectionIntersection: this.selectionIntersection,
            modelIds: this.selectedModelIds,
            commomModelResults: this.commomModelResults,
            startAnalysis: true,
          },
        });
        window.open(routeData.href, "_blank");
      } else {
        this.loadTree({
          projectId: this.projectId,
          selectionIds: this.selectedSelectionsIds,
          selectionIntersection: this.selectionIntersection,
          modelIds: this.selectedModelIds,
          commomModelResults: this.commomModelResults,
        });
      }
    },

    loadTree({
      projectId,
      selectionIds = [],
      selectionIntersection = false,
      modelIds = [],
      commomModelResults = false,
    }) {
      console.time("LOAD TREE");
      this.loading = true;

      dataLoader
        .loadProjectSamples({
          projectId,
          selectionIds,
          selectionIntersection,
          modelIds,
          commomModelResults,
        })
        .then((data) => {
          // Creating the data object
          this.$store.commit("selectProjectId", projectId);
          this.$store.commit("setSelectionsIds", selectionIds);
          this.$store.commit("setColoredColumnIndex", 0);
          this.$store.commit("clearAllFilters");

          // Perf Log
          console.timeEnd("LOAD TREE");

          // Convert the lists in str for the querry
          if (selectionIds && selectionIds.length > 0)
            selectionIds = selectionIds.reduce(
              (sId, total) => total + "." + sId
            );
          if (modelIds && modelIds.length > 0)
            modelIds = modelIds.reduce((mId, total) => total + "." + mId);

          // start analysis immediatly
          this.$router.push({
            name: "dataAnalysis",
            query: {
              projectId,
              selectionIds,
              selectionIntersection,
              modelIds,
              commomModelResults,
            },
            params: { data },
          });
        })
        .finally(() => (this.loading = false))
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Something went wrong",
          });
          this.loadProject();
        });
    },

    // Other
    deleteProject() {
      swal({
        title: "Delete the project ?",
        text: "Do you realy want to delete the project ? There is no way back.",
        buttons: true,
        icon: "warning",
        dangerMode: true,
      }).then((validate) => {
        if (validate)
          this.$backendDialog.deleteProject(this.projectId).then(() => {
            this.$store.commit("sendMessage", {
              title: "success",
              msg: "Project deleted",
            });
            this.$router.push("/");
          });
      });
    },
    selectionDeleted(selectionId) {
      this.project.selections = this.project.selections.filter(
        (s) => s.id !== selectionId
      );
    },
    modelDeleted(modelId) {
      this.project.models = this.project.models.filter((m) => m.id !== modelId);
    },
  },
  computed: {
    readyToAnalyse() {
      // return true if the ans can be run
      if (this.disabled || this.loading || this.nbSelectedSamples === 0)
        return false;
      if (this.selectedModelIds.length > 0 && this.nbEvaluatedSamples === 0)
        return false;
      return true;
    },
    selectedSelections() {
      return this.selectedSelectionsIds.map((selecId) =>
        this.project.selections.find((s) => selecId === s.id)
      );
    },
    selectedModels() {
      return this.selectedModelIds.map((mId) =>
        this.project.models.find((m) => mId === m.id)
      );
    },
  },
  watch: {
    selectionIntersection() {
      this.updateNbSamples();
    },
    commomModelResults() {
      this.updateNbSamples();
    },
  },
};
</script>

<style scoped>
#project {
  text-align: left;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

#projectContent {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: rgb(240, 240, 240);
}

#selectionAndModels {
  display: flex;
  flex: 1;
  max-height: 67vh;
}
</style>
