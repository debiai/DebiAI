<template>
  <div id="ColumnSelection">
    <!-- <div id="top">
      <h3 id="title">Select the columns you want to use for the exploration:</h3>
      <button
        :disabled="selectedColumnsIndex.length === 0"
        @click="save"
      >
        Save
      </button>
    </div> -->
    <ProjectColumns
      :columns="projectColumns"
      :selectedColumnsIndex="selectedColumnsIndex"
      :saveButtonCallback="save"
      :saveButtonDisabled="selectedColumnsIndex.length === 0"
      title=""
      selectable
      @selectedColumnsIndexUpdate="selectedColumnsIndex = $event"
    />
  </div>
</template>

<script>
import ProjectColumns from "../../project/projectColumns/ProjectColumns.vue";

export default {
  components: { ProjectColumns },
  props: {
    selectColumnsIndex: { type: Array, default: () => [] }, // The selected columns index
  },
  data() {
    return {
      projectColumns: [],
      selectedColumnsIndex: [],
    };
  },
  created() {
    // Get the project info
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;

    // Expected project columns example :
    //  [
    //      { "name": "storage", "category": "other" },
    //      { "name": "age", "category": "context" },
    //      { "name": "path", "category": "input" },
    //      { "name": "label", "category": "groundtruth" },
    //      { "name": "type" }, # category is not specified, it will be "other"
    //  ]

    // Set the selected columns index
    this.selectedColumnsIndex = [...this.selectColumnsIndex];
  },
  methods: {
    save() {
      // Go to the aggregation page
      this.$emit("save", this.selectedColumnsIndex);
    },
  },
  computed: {},
};
</script>

<style scoped lang="scss">
#ColumnSelection {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 10px;

  // #top {
  //   max-width: 800px;
  //   width: 90%;
  //   margin: 20px;
  //   display: flex;
  //   justify-content: space-between;
  //   align-items: center;
  // }
}
</style>
