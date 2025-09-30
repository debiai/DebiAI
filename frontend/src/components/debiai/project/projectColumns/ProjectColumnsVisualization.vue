<template>
  <div id="ProjectColumnsVisualization">
    <h3>Data columns</h3>
    {{ dataColumnsPerGroup }}
    <div id="columns">
      <div
        class="category"
        v-for="(category, i) in Object.keys(dataColumnsPerGroup)"
        :key="i"
      >
        <div class="categoryName">{{ category }}:</div>
        <div
          v-for="group in Object.keys(dataColumnsPerGroup[category])"
          :key="group"
          class="group"
        >
          <div v-if="group">
            <!-- Grouped columns -->
            <Collapsible style="margin: 3px">
              <template v-slot:header>
                {{ group }}
                <span class="nbItem"> {{ dataColumnsPerGroup[category][group].length }} </span>
              </template>
              <template v-slot:body>
                <div class="columns">
                  <Columns :columns="dataColumnsPerGroup[category][group]" />
                </div>
              </template>
            </Collapsible>
          </div>
          <div
            v-else
            class="group"
          >
            <!-- Ungrouped columns -->
            <Columns :columns="dataColumnsPerGroup[category][group]" />
          </div>
        </div>
      </div>
    </div>
    <div v-if="!projectColumns.length">No columns</div>

    <!-- Results columns -->
    <h3>Results columns</h3>
    <div
      id="results"
      v-if="projectResultsColumns.length"
    >
      <div
        v-for="group in Object.keys(resultsColumnsPerGroup.results)"
        :key="group"
        class="group"
      >
        <div v-if="group">
          <!-- Grouped columns -->
          <Collapsible style="margin: 3px">
            <template v-slot:header>
              {{ group }}
              <span class="nbItem"> {{ resultsColumnsPerGroup.results[group].length }} </span>
            </template>
            <template v-slot:body>
              <div class="columns">
                <Columns :columns="resultsColumnsPerGroup.results[group]" />
              </div>
            </template>
          </Collapsible>
        </div>
        <div
          v-else
          class="group"
        >
          <!-- Ungrouped columns -->
          <Columns :columns="resultsColumnsPerGroup.results[group]" />
        </div>
      </div>
    </div>
    <div v-else>No results columns</div>
  </div>
</template>

<script>
import Columns from "./Columns.vue";

export default {
  name: "ProjectColumnsVisualization",
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
  methods: {
    groupCategoriesPerGroup(categories) {
      // A column can have a group
      // This function returns, for each categories, the columns grouped by group
      const categoriesGroups = {};
      for (let category in categories) {
        const groups = { "": [] };
        for (let column of categories[category]) {
          const group = column.metadata.group;
          if (!group) {
            groups[""].push(column);
            continue;
          }

          if (!groups[group]) groups[group] = [];
          groups[group].push(column);
        }
        categoriesGroups[category] = groups;
      }
      return categoriesGroups;
    },
  },
  computed: {
    columnsPerCategory() {
      let columnsPerCategory = {};
      for (let i = 0; i < this.projectColumns.length; i++) {
        let column = this.projectColumns[i];
        let category = column.metadata.category + "s";
        // Capitalize first letter
        category = category.charAt(0).toUpperCase() + category.slice(1);
        if (!category) category = "other";
        if (!columnsPerCategory[category]) columnsPerCategory[category] = [];
        columnsPerCategory[category].push(column);
      }
      return columnsPerCategory;
    },

    dataColumnsPerGroup() {
      return this.groupCategoriesPerGroup(this.columnsPerCategory);
    },
    resultsColumnsPerGroup() {
      return this.groupCategoriesPerGroup({ results: this.projectResultsColumns });
    },
  },
};
</script>

<style scoped lang="scss">
#ProjectColumnsVisualization {
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
