<template>
  <div
    id="ColumnsConfiguration"
    class="card"
  >
    <div class="title">
      <h3>Select the columns used by the exploration mode</h3>
      <div class="buttons">
        <button
          class="green"
          @click="validate"
          :disabled="selectedColumns.length < minimumSelection"
        >
          Compute
        </button>
      </div>
    </div>
    <div
      id="columns"
      v-if="selectedColumns"
    >
      <Category
        v-for="(columns, i) in categories"
        :key="i"
        :columns="columns"
        :selectedColumns="selectedColumns"
        :name="i"
        @columnSelected="columnSelected"
        @all="categorySelected"
        @none="categoryUnselected"
        multipleSelection
        colorSelection
      />

      <!-- Special global metrics category -->
      <Category
        v-if="data.globalMetrics.length"
        :columns="data.globalMetrics"
        :selectedColumns="selectedMetrics"
        @columnSelected="metricSelected"
        name="Global metrics"
        multipleSelection
        colorSelection
        metrics
      />
    </div>
  </div>
</template>

<script>
import Category from "./Category";

export default {
  components: {
    Category,
  },
  data() {
    return {
      selectedColumns: [],
      selectedMetrics: [0],
      searchFilter: "", // TODO: Implement or remove
    };
  },
  props: {
    data: { type: Object, required: true },
    minimumSelection: { type: Number, default: 0 },
    colorSelection: { type: Boolean, default: false },
    defaultSelected: { type: Array, default: undefined },
  },
  created() {
    if (this.defaultSelected == undefined) {
      this.selectedColumns = this.data.columns
        .filter((col) => col.nbOccurrence > 1 && col.type !== undefined)
        .map((col) => col.index);
    } else {
      this.selectedColumns = this.defaultSelected;
    }
    document.addEventListener("keydown", this.keyHandler);
  },
  mounted() {},
  methods: {
    keyHandler(k) {
      if (k.key == "Escape") {
        this.$emit("cancel");
      }
    },
    categorySelected(category) {
      this.selectedColumns = this.selectedColumns.concat(
        this.data.columns.filter((col) => col.category == category).map((col) => col.index)
      );
    },
    categoryUnselected(category) {
      this.selectedColumns = this.selectedColumns.filter(
        (col) =>
          !this.data.columns
            .filter((c) => c.category == category)
            .map((c) => c.index)
            .includes(col)
      );
    },
    columnSelected(colIndex) {
      this.$emit("colSelect", colIndex);

      if (this.selectedColumns.includes(colIndex)) {
        this.selectedColumns = this.selectedColumns.filter((index) => index != colIndex);
      } else {
        this.selectedColumns.push(colIndex);
      }
    },
    metricSelected(colIndex) {
      this.$emit("metricSelect", colIndex);

      if (colIndex == 0) {
        alert("You can't unselect the data number global metric");
        return;
      }

      if (this.selectedMetrics.includes(colIndex)) {
        this.selectedMetrics = this.selectedMetrics.filter((index) => index != colIndex);
      } else {
        this.selectedMetrics.push(colIndex);
      }
    },
    validate() {
      this.$emit("validate", {
        selectedColumns: this.selectedColumns,
        selectedMetrics: this.selectedMetrics,
      });
    },
  },
  computed: {
    categories: function () {
      const categories = {};

      for (const col of this.data.columns) {
        if (!categories[col.category]) categories[col.category] = [];

        categories[col.category].push(col);
      }

      return categories;
    },
  },
  watch: {
    defaultSelected() {
      if (this.defaultSelected) this.selectedColumns = this.defaultSelected;
    },
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.keyHandler);
  },
};
</script>

<style lang="scss" scoped>
#ColumnsConfiguration {
  margin: 0;
  .title {
    justify-content: center;
    gap: 20px;
    background-color: white;
    padding: 10px 10px 0;
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
