<template>
  <div
    id="ColumnSelection"
    class="card"
  >
    <!-- Header -->
    <div class="title">
      <h3>{{ title }}</h3>
      <div
        id="controls"
        v-if="validateRequired"
      >
        <button @click="none('')">None</button>
        <button @click="all('')">All</button>
      </div>
      <div class="selectedColumns">
        <div v-if="validateRequired">
          <div class="name">Selected columns</div>
          <div class="value">{{ selectedColumns.length }} / {{ data.nbColumns }}</div>
        </div>
        <div v-if="minimumSelection > 0">
          <div class="name">Minimum required columns</div>
          <div class="value">{{ minimumSelection }}</div>
        </div>
      </div>
      <div class="buttons">
        <button
          v-if="cancelAvailable"
          class="red"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
        <button
          v-if="validateRequired"
          class="green"
          @click="validate"
          :disabled="selectedColumns.length < minimumSelection"
        >
          Validate
        </button>
      </div>
    </div>
    <div id="searchBar">
      Filter:
      <input
        ref="columnsSearch"
        v-model="searchFilter"
        type="text"
      />
      <inline-svg
        :src="require('@/assets/svg/loop.svg')"
        height="14"
        width="14"
      />
    </div>
    <!-- Columns -->
    <div
      id="columns"
      v-if="selectedColumns"
    >
      <Category
        v-for="(columns, i) in categories"
        :key="i"
        :data="data"
        :columns="columns"
        :selectedColumns="selectedColumns"
        :name="i"
        :multipleSelection="validateRequired"
        :colorSelection="colorSelection"
        :validColumnsProperties="validColumnsProperties"
        v-on:columnSelected="columnSelected"
        v-on:all="all"
        v-on:none="none"
      />
    </div>
  </div>
</template>

<script>
import columnsFiltering from "@/services/statistics/columnsFiltering";
import Category from "./Category";

export default {
  components: {
    Category,
  },
  data() {
    return {
      selectedColumns: [],
      searchFilter: "",
    };
  },
  props: {
    data: { type: Object, required: true },
    title: { type: String, default: "Select multiple columns" },
    validateRequired: { type: Boolean, default: true },
    minimumSelection: { type: Number, default: 0 },
    cancelAvailable: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
    defaultSelected: { type: Array, default: undefined },
    validColumnsProperties: { type: Object, default: () => ({}) },
  },
  created() {
    if (this.defaultSelected == undefined) {
      if (this.validateRequired) {
        this.selectedColumns = this.data.columns
          .filter((col) => col.nbOccurrence > 1 && col.type !== undefined)
          .map((col) => col.index);
      }
    } else {
      this.selectedColumns = this.defaultSelected;
    }
  },
  mounted() {
    // Set focus on search bar
    this.$refs.columnsSearch.focus();
  },

  methods: {
    // Handles the selection of a column and emits the "colSelect" event with the selected column index
    columnSelected(colIndex) {
      this.$emit("colSelect", colIndex);

      if (this.validateRequired) {
        // If the column is already selected, remove it from the selectedColumns array
        if (this.selectedColumns.includes(colIndex))
          this.selectedColumns = this.selectedColumns.filter((index) => index != colIndex);
        // Otherwise, add it to the selectedColumns array
        else this.selectedColumns.push(colIndex);
      }
    },
    // Validates the selected columns and emits the "validate" event with the selectedColumns array
    validate() {
      this.$emit("validate", this.selectedColumns);
    },
    // Selects all columns in a specified category or all columns in all categories
    all(name) {
      if (this.validateRequired) {
        if (name) {
          // Select all columns in the specified category
          this.categories[name]
            .filter(
              (col) =>
                columnsFiltering.getColumnStatus(col, this.validColumnsProperties).status ===
                "valid"
            )
            .forEach((col) => {
              // Only select columns that are not already selected and have more than one occurrence
              if (!this.selectedColumns.includes(col.index) && col.nbOccurrence > 1)
                this.selectedColumns.push(col.index);
            });
        } else {
          // Select all columns in all categories
          this.selectedColumns = this.data.columns
            .filter(
              (col) =>
                columnsFiltering.getColumnStatus(col, this.validColumnsProperties).status ===
                "valid"
            )
            .filter((col) => col.type !== undefined && col.nbOccurrence > 1)
            .map((col) => col.index);
        }
      }
    },
    // Deselects all columns in a specified category or clears the selectedColumns array
    none(name) {
      if (this.validateRequired) {
        if (name) {
          // Deselect all columns in the specified category
          this.categories[name].forEach((col) => {
            this.selectedColumns = this.selectedColumns.filter((index) => index != col.index);
          });
        } else {
          // Clear the selectedColumns array
          this.selectedColumns = [];
        }
      }
    },
  },
  computed: {
    categories() {
      const categoriesMap = {};
      this.data.columns.forEach((column) => {
        const category = column.category || "Uncategorized";
        if (!categoriesMap[category]) categoriesMap[category] = [];
        if (column.label.toLowerCase().includes(this.searchFilter.toLowerCase()))
          categoriesMap[category].push(column);
      });
      return categoriesMap;
    },
  },
  watch: {
    defaultSelected() {
      if (this.defaultSelected) this.selectedColumns = this.defaultSelected;
    },
  },
};
</script>

<style lang="scss" scoped>
#ColumnSelection {
  .title {
    justify-content: space-between;
    background-color: var(--greyLight);
    gap: 10px;

    .selectedColumns > div {
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: center;
    }
  }
  #searchBar {
    display: flex;
    gap: 3px;
    font-weight: bold;
    align-items: center;
    background-color: var(--greyLight);
    padding: 3px 13px 10px;
  }
  #searchBar input {
    margin: 0px 10px;
  }
  #columns {
    display: flex;
    justify-content: center;
    align-items: top;
    flex-wrap: wrap;
    overflow-y: auto;
  }

  .dataGroup .data .value {
    padding: 7px;
  }
}
</style>
