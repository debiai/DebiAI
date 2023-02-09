<template>
  <div id="SelectionExportMenu">
    <!-- Modal title -->
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
      <!-- Annotation Value -->
      <div class="data">
        <span class="name">
          Annotation value
          <DocumentationBlock>
            Add an extra value to the exported Json data.
            <br />
            This value can be used for anotation or for object creation purpose.
          </DocumentationBlock>
        </span>
        <span class="value">
          <input type="text" v-model="extraValue" />
        </span>
      </div>
      <!-- Exported data -->
      <div class="data">
        <span class="name">
          Exported Json <br />
          format
          <DocumentationBlock>
            This is not the exact exported Json file. It is only here to give
            you an idea of the structure of the exported Json file.

            <br /><br />

            The exported Json file will be filled with the selected samples ids.
          </DocumentationBlock>
        </span>
        <pre class="value" id="exportedSelection">

{{ JSON.stringify(selectionToExportDisplay, undefined, 2) }}

        </pre>
      </div>
    </form>

    <!-- Export method list -->
    <ExportMethodSelection
      :disableExport="exporting"
      @exportMethodSelected="exportSamples"
    />
  </div>
</template>

<script>
import ExportMethodSelection from "./ExportMethodSelection.vue";

export default {
  components: { ExportMethodSelection },
  name: "SelectionExportMenu",
  data() {
    const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
    const projectId = this.$store.state.ProjectPage.projectId;
    
    return {
      selectionName: "DebiAI Selection",
      extraValue: null,

      exporting: false,
      selectionToExportDisplay: {
        origin: "DebiAI",
        type: "selection",
        project_id: projectId,
        data_provider_id: dataProviderId,
        selection_name: "DebiAI Selection",
        date: "timestamp",
        sample_ids: [
          { id: "sample id 1" },
          { id: "sample id 2" },
          { id: "..." },
        ],
      },
    };
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {},
  methods: {
    exportSamples(methodId) {
      let selectedHash = this.selectedData.map(
        (selectedIndex) => this.data.sampleIdList[selectedIndex]
      );

      this.exporting = true;

      this.$backendDialog
        .exportSelection(
          this.selectionName,
          methodId,
          selectedHash,
          this.extraValue
        )
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
        })
        .finally(() => {
          this.exporting = false;
        });
    },
  },
  computed: {},
  watch: {
    selectionName() {
      this.selectionToExportDisplay.selection_name = this.selectionName;
    },
    extraValue() {
      this.selectionToExportDisplay.value = this.extraValue;
      if (this.extraValue === "") delete this.selectionToExportDisplay.value;
    },
  },
};
</script>

<style scoped>
/* Form: */
.dataGroup {
  flex-direction: column;
  align-items: center;
}

.dataGroup .data + .data {
  padding-top: 4px;
}

.dataGroup .value {
  flex: 1;
}

.dataGroup #exportedSelection {
  margin: 0;
  padding-left: 10px;
  max-width: 400px;
  max-height: 270px;
  overflow: scroll;
  font-size: 0.6em;
  font-family: monospace;
  text-align: left;
  display: block;
}
</style>