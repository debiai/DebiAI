<template>
  <div id="SelectionExportMenu">
    <h2>
      Export the selected samples
      <button @click="$emit('cancel')" class="red">Cancel</button>
    </h2>
    <!-- Export params -->
    <form v-on:submit.prevent class="dataGroup">
      <!-- Selected samples -->
      <div class="data">
        <span class="name"> Exported samples </span>
        <span class="value">
          {{ selectedData.length }} / {{ data.nbLines }}
        </span>
      </div>
      <!-- Selection Name -->
      <div class="data">
        <span class="name">
          Selection name

          <DocumentationBlock>
            Name that will be written in the expoted 'selection_name' Json
            field.
          </DocumentationBlock>
        </span>
        <span class="value">
          <input type="text" v-model="selectionName" style="flex: 2" required />
        </span>
      </div>
    </form>

    <!-- Export method list -->
    <ExportMethodSelection :disableExport="exporting" @exportMethodSelected="exportSamples" />

  </div>
</template>

<script>
import ExportMethodSelection from "./ExportMethodSelection.vue";

export default {
  components: { ExportMethodSelection },
  name: "SelectionExportMenu",
  data() {
    return {
      selectionName: "DebiAI Selection",
      exporting: false,
    };
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  created() { },
  methods: {
    exportSamples(methodId) {
      let projectId = this.$store.state.ProjectPage.projectId;
      let selectedHash = this.selectedData.map(
        (selectedIndex) => this.data.sampleHashList[selectedIndex]
      );

      this.exporting = true;

      this.$backendDialog
        .exportSelection(projectId, this.selectionName, methodId, selectedHash)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Selection exported successfully",
          });
          this.$emit("exported");
        })
        .catch((e) => {
          console.log(e);
          if (e.response && e.response.data) {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: e.response.data,
            });
          } else {
            this.$store.commit("sendMessage", {
              title: "error",
              msg: "Error while exporting the selection",
            });
          }
        }).finally(() => {
          this.exporting = false;
        });
    },
  },
  computed: {},
};
</script>

<style scoped>
/* Form: */
.dataGroup {
  flex-direction: column;
}

.dataGroup .data+.data {
  padding-top: 4px;
}

.dataGroup .value {
  flex: 1;
}
</style>