<template>
  <div id="ProjectColumnsVisu">
    <h3>Data columns</h3>
    <div id="columns">
      <div
        class="category"
        v-for="(category, i) in Object.keys(columnsPerGroup)"
        :key="i"
      >
        <div class="categoryName">{{ category }}:</div>
        <div
          v-for="group in Object.keys(columnsPerGroup[category])"
          :key="group"
          class="group"
        >
          <div v-if="group">
            <!-- Grouped columns -->
            <Collapsible style="margin: 3px">
              <template v-slot:header>
                <h4>{{ group }}</h4>
              </template>
              <template v-slot:body>
                <div class="columns">
                  <Columns :columns="columnsPerGroup[category][group]" />
                </div>
              </template>
            </Collapsible>
          </div>
          <div
            v-else
            class="group"
          >
            <!-- Ungrouped columns -->
            <Columns :columns="columnsPerGroup[category][group]" />
          </div>
        </div>
      </div>
    </div>
    <div v-if="!projectColumns.length">No columns</div>

    <h3 v-if="projectResultsColumns.length">Results columns</h3>
    <div id="results">
      <div class="columns">
        <Columns :columns="projectResultsColumns" />
      </div>
    </div>
  </div>
</template>

<script>
import Columns from "./Columns.vue";

export default {
  name: "ProjectColumnsVisu",
  components: { Columns },
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

    columnsPerGroup() {
      // A column can have a group
      // This function returns, for each categories, the columns grouped by group
      const categoriesGroups = {};
      const categories = this.columnsPerCategory;

      for (let category in categories) {
        const columns = categories[category];
        const groups = { "": [] };
        for (let i = 0; i < columns.length; i++) {
          const column = columns[i];
          const group = column.group;
          if (!group) groups[""].push(column);
          else {
            if (!groups[group]) groups[group] = [];
            groups[group].push(column);
          }
        }
        categoriesGroups[category] = groups;
      }

      return categoriesGroups;
    },
  },
};
</script>

<style scoped lang="scss">
#ProjectColumnsVisu {
  min-width: 400px;
  min-height: 300px;
  padding-top: 20px;

  #columns {
    padding-bottom: 20px;
  }

  .category {
    margin: 5px;
    margin-top: 15px;

    .categoryName {
      font-weight: bold;
      margin-bottom: 10px;
    }
  }
}
</style>
