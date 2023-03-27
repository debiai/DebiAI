<template>
  <div id="ProjectColumnsVisu">
    <h3>Data colums</h3>
    <div id="columns">
      <div
        class="category"
        v-for="category in Object.keys(columnsPerCategory)"
        :key="category"
      >
        <div class="categoryName">
          {{ category }}:
        </div>
        <div class="columns">
          <div
            class="column"
            v-for="column in columnsPerCategory[category]"
            :key="column.name"
          >
            <div class="columnName">
              {{ column.name }}
            </div>
            <div class="columnType">
              {{ column.type !== undefined ? column.type : "auto" }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!projectColumns.length">No columns</div>

    <h3 v-if="projectResultsColumns.length">Results columns</h3>
    <div id="results">
      <div class="columns">
        <div
          class="column"
          v-for="column in projectResultsColumns"
          :key="column.name"
        >
          <div class="columnName">
            {{ column.name }}
          </div>
          <div class="columnType">
            {{ column.type !== undefined ? column.type : "auto" }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectColumnsVisu",
  components: {},
  data: () => {
    return {
      projectColumns: [],
      projectResultsColumns: [],
    };
  },
  created() {
    // Expected project columns example :
    //  [
    //      { "name": "storage", "category": "other" },
    //      { "name": "age", "category": "context" },
    //      { "name": "path", "category": "input" },
    //      { "name": "label", "category": "groundtruth" },
    //      { "name": "type" }, # category is not specified, it will be "other"
    //  ]
    this.projectColumns = this.$store.state.ProjectPage.projectColumns;
    if (!this.projectColumns) this.projectColumns = [];

    // Expected project results columns example :
    // [
    //   { name: "Model prediction", type: "number" },
    //   { name: "Model error", type: "number" },
    // ];
    this.projectResultsColumns = this.$store.state.ProjectPage.projectResultsColumns;
    if (!this.projectResultsColumns) this.projectResultsColumns = [];
  },
  methods: {},
  computed: {
    columnsPerCategory() {
      let columnsPerCategory = {};
      for (let i = 0; i < this.projectColumns.length; i++) {
        let column = this.projectColumns[i];
        let category = column.category + "s";
        // Capitalize first letter
        category = category.charAt(0).toUpperCase() + category.slice(1);
        if (!category) category = "other";
        if (!columnsPerCategory[category]) columnsPerCategory[category] = [];
        columnsPerCategory[category].push(column);
      }
      return columnsPerCategory;
    },
  },
};
</script>

<style scoped>
#ProjectColumnsVisu {
  min-width: 400px;
  min-height: 300px;
  padding-top: 20px;
}
#projectColumns {
  display: flex;
  align-items: center;
  flex-direction: column;
}

#columns {
  padding-bottom: 20px;
}

.category {
  margin: 5px;
  margin-top: 15px;
}

.categoryName {
  font-weight: bold;
}

.columns {
  display: flex;
  flex-direction: column;
}

.column {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 10px;
  margin: 1px;
  border: 1px solid #00000027;
  border-radius: 10px;
}

.columnType {
  width: 50px;
  text-align: right;
  opacity: 0.5;
}
</style>
