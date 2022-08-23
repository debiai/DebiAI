<template>
  <div id="ExportMenu">
    <h2>Export the selected samples</h2>
    <form v-on:submit.prevent class="dataGroup">
      <!-- createdTags -->
      <!-- Selected samples -->
      <div class="data">
        <span class="name"> Exported samples </span>
        <span class="value">
          {{ selectedData.length }} / {{ data.nbLines }}
        </span>
      </div>
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
    <span>
      <!-- Export method list -->
      <div class="exportMethod">
        M1
        <button class="green" @click="exportSamples(1)">Export</button>
        <!-- TODO -->
      </div>
      <button @click="$emit('cancel')" class="red">Cancel</button>
    </span>
  </div>
</template>

<script>
export default {
  name: "ExportMenu",
  data() {
    return {
      selectionName: "DebiAI Selection",
      exportMethods: [],
    };
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Load the tagged exportMethods
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
  },
  computed: {
    selectionExportNameOk() {
      return this.selectionName.length >= 1;
    },
  },
};
</script>

<style scoped>
.errorMsg {
  color: red;
}

.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 4px;
}
.dataGroup .value {
  flex: 1;
}
</style>