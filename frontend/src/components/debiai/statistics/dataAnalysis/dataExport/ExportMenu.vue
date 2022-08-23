<template>
  <div id="ExportMenu">
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
          <input type="text" v-model="selectionName" style="flex: 2" />
        </span>
      </div>
    </form>
    <!-- Export method list -->
    <div>
      <h3 style="text-align: left; padding-top: 15px">
        Select an export method:
      </h3>
      <div id="exportMethods" class="card" v-if="exportMethods">
        <div class="itemList">
          <div
            class="exportMethod item"
            v-for="exportMethod in exportMethods"
            :key="exportMethod.id"
          >
            <h3 class="name">
              {{ exportMethod.name }}
              <button class="red" @click="deleteExportMethod(exportMethod.id)">
                <b>Delete</b>
              </button>
              <span style="flex: 1"></span>
              <button class="green" @click="exportSamples(exportMethod.id)">
                Export
              </button>
            </h3>

            <div class="details">
              <div class="type">{{ exportMethod.type }}</div>
              <div class="parameters">
                <div
                  class="parameter"
                  v-for="parameterKey in Object.keys(exportMethod.parameters)"
                  :key="parameterKey"
                >
                  <u> {{ parameterKey }}:</u>
                  {{ exportMethod.parameters[parameterKey] }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-else
        id="exportMethods"
        class="card"
        style="justify-content: center; color: grey"
      >
        Loading export methods
      </div>
    </div>
    <div style="text-align: right">
      <button class="green" @click="newExportMethod">New export method</button>
    </div>

    <!-- New Method modal -->
    <modal v-if="newExportMethodModal">
      <ExportMethodCreator
        @cancel="newExportMethodModal = false"
        @created="newExportMethodModal = false"
      />
    </modal>
  </div>
</template>

<script>
import ExportMethodCreator from "./ExportMethodCreator.vue";

export default {
  components: { ExportMethodCreator },
  name: "ExportMenu",
  data() {
    return {
      exportMethods: null,
      selectionName: "DebiAI Selection",

      newExportMethodModal: false,
    };
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Load the exportMethods
    // TODO
  },
  methods: {
    exportSamples() {
      //   this.$backendDialog
      //     .updateTag(projectId, this.selectionName, tagHash)
      //     .then(() => {
      //       this.$store.commit("sendMessage", {
      //         title: "success",
      //         msg: "Tag uploaded successfully",
      //       });
      //       this.$emit("created");
      //     })
      //     .catch((err) => {
      //       console.error(err);
      //       this.$store.commit("sendMessage", {
      //         title: "error",
      //         msg: "Error while saving or updating the tag to the server",
      //       });
      //     });
      this.$emit("exported");
    },

    deleteExportMethod() {
      // TODO
    },

    newExportMethod() {
      this.newExportMethodModal = !this.newExportMethodModal;
    },
  },
  computed: {
    selectionExportNameOk() {
      return this.selectionName.length >= 1;
    },
  },
};
</script>

<style scoped>
/* Form: */
.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}

/* Methods: */
#exportMethods {
  display: flex;
  min-width: 600px;
  height: 400px;
  overflow: auto;
}
.exportMethod {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: stretch;
}
.exportMethod .name {
  display: flex;
  align-items: center;
  gap: 10px;
}
.exportMethod .details {
  display: flex;
  align-items: flex-start;
  padding: 10px;
  gap: 10px;
}
.exportMethod .details .parameters {
  border-left: 1px solid rgb(75, 75, 75);
  text-align: left;
  padding-left: 15px;
  opacity: 80%;
}
.exportMethod .details .parameter {
  padding-bottom: 8px;
}
</style>