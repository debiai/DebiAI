<template>
  <div id="ProjectColumns">
    <!-- Title of the column list -->
    <h3
      id="title"
      v-if="title"
    >
      {{ title }}
    </h3>

    <!-- Selected columns info -->
    <div
      id="selectionInfo"
      v-if="selectable"
    >
      <div id="nbSelected">
        <NbItem
          :nbSelected="getNbSelectedColumns(columns)"
          :nbTotal="columns.length"
        />
      </div>

      <div id="controls">
        <button
          class="white"
          @click="selectedColumns = []"
          :disabled="selectedColumns.length === 0"
        >
          Unselect all
        </button>
        <button
          class="white"
          @click="selectedColumns = columns.map((c) => c.index)"
          :disabled="selectedColumns.length === columns.length"
        >
          Select all
        </button>
      </div>
    </div>

    <!-- Columns -->
    <div id="columns">
      <div
        class="category"
        v-for="category in Object.keys(dataColumnsPerGroup)"
        :key="category"
      >
        <div
          class="categoryName"
          v-if="category"
        >
          {{ category }}:
        </div>
        <div
          v-for="group in Object.keys(dataColumnsPerGroup[category])"
          :key="group"
          class="group"
        >
          <div v-if="group">
            <!-- Grouped columns -->
            <Collapsible style="margin: 3px">
              <template v-slot:header>
                <!-- Group title -->
                <h4>
                  {{ group }}
                  <!-- Nb selected columns in group: -->
                  <NbItem
                    v-if="selectable"
                    :nbSelected="getNbSelectedColumns(dataColumnsPerGroup[category][group])"
                    :nbTotal="dataColumnsPerGroup[category][group].length"
                  />
                </h4>
              </template>
              <template v-slot:body>
                <div class="columns">
                  <ColumnsDisplay
                    :columns="dataColumnsPerGroup[category][group]"
                    :selectable="selectable"
                    :selectedColumns="selectedColumns"
                    @selectColumn="selectColumn"
                  />
                </div>
              </template>
            </Collapsible>
          </div>
          <div
            v-else
            class="group"
          >
            <!-- Ungrouped columns -->
            <ColumnsDisplay
              :columns="dataColumnsPerGroup[category][group]"
              :selectable="selectable"
              :selectedColumns="selectedColumns"
              @selectColumn="selectColumn"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="!columns.length">No columns</div>
  </div>
</template>

<script>
import Columns from "./Columns.vue";

export default {
  name: "ProjectColumns",
  components: { ColumnsDisplay: Columns },
  props: {
    columns: {
      type: Array,
      required: true,
    },
    title: {
      type: String,
      default: "Columns",
    },
    selectable: {
      type: Boolean,
      default: false,
    },
    selectedColumnsIndex: {
      type: Array,
      default: () => [],
      // The columns already selected
    },
  },
  data: () => {
    return {
      selectedColumns: [],
    };
  },
  created() {
    // Copy the selected columns
    this.selectedColumns = [...this.selectedColumnsIndex];
  },
  methods: {
    groupCategoriesPerGroup(categories) {
      // A column can have a group
      // This function returns, for each categories, the columns grouped by group
      const result = {};
      for (let category in categories) {
        const groups = { "": [] };
        for (let column of categories[category]) {
          const group = column.group;
          if (!group) {
            groups[""].push(column);
            continue;
          }

          if (!groups[group]) groups[group] = [];
          groups[group].push(column);
        }
        result[category] = groups;
      }
      return result;
    },
    selectColumn(columnIndex) {
      if (!this.selectable) return;

      // Add or remove the column from the selected columns
      if (this.selectedColumns.includes(columnIndex)) {
        this.selectedColumns = this.selectedColumns.filter((index) => index !== columnIndex);
      } else {
        this.selectedColumns.push(columnIndex);
      }

      // The event will be emitted by the watcher
    },
    getNbSelectedColumns(columns) {
      // Return the number of selected columns in the given columns
      let nbSelectedColumns = 0;
      for (let column of columns)
        if (this.selectedColumns.includes(column.index)) nbSelectedColumns++;

      return nbSelectedColumns;
    },
  },
  computed: {
    columnsPerCategory() {
      let columnsPerCategory = {};
      // Iterate through all columns
      for (let i = 0; i < this.columns.length; i++) {
        // Get the current column and its category
        let column = this.columns[i];
        let category = column.category ? column.category + "s" : "";
        // Capitalize first letter
        category = category.charAt(0).toUpperCase() + category.slice(1);
        // Add the column to its category
        if (!columnsPerCategory[category]) columnsPerCategory[category] = [];
        columnsPerCategory[category].push(column);
      }
      return columnsPerCategory;
    },

    dataColumnsPerGroup() {
      return this.groupCategoriesPerGroup(this.columnsPerCategory);
    },
  },
  watch: {
    selectedColumns() {
      this.$emit("selectedColumnsIndexUpdate", this.selectedColumns);
    },
  },
};
</script>

<style scoped lang="scss">
#ProjectColumns {
  min-width: 600px;
  min-height: 300px;

  #title {
    margin-top: 15px;
  }

  #selectionInfo {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    padding: 0 10px;

    .nbItem {
      font-weight: bold;
    }

    .blue {
      color: #1e88e5;
    }

    #controls {
      display: flex;
      justify-content: space-between;
      align-items: center;

      button {
        margin-left: 10px;
      }
    }
  }

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
