<template>
  <div
    id="ColumnsConfiguration"
    class="card"
  >
    <div class="title">
      <h3>Select the columns used by the exploration mode</h3>
      <div class="dataGroup">
        <div class="data">
          <div class="name">Selected columns</div>
          <div class="value">{{ selectedColumns.length }} / {{ data.nbColumns }}</div>
        </div>
        <div
          class="data"
          v-if="minimumSelection > 0"
        >
          <div class="name">Minimum required columns</div>
          <div class="value">{{ minimumSelection }}</div>
        </div>
      </div>
      <div class="buttons">
        <button
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
        fill="white"
      />
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
        v-on:columnSelected="columnSelected"
        multipleSelection
        colorSelection
      />

      <!-- Special global metrics category -->
      <Category
        v-if="data.globalMetrics.length"
        :columns="data.globalMetrics"
        :selectedColumns="selectedMetrics"
        v-on:columnSelected="metricSelected"
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
      searchFilter: "",
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
    columnSelected(colIndex) {
      this.$emit("colSelect", colIndex);

      if (this.selectedColumns.includes(colIndex)) {
        this.selectedColumns = this.selectedColumns.filter((index) => index != colIndex);
      } else {
        this.selectedColumns.push(colIndex);
      }
    },
    metricSelected(colIndex) {
      console.log("metricSelected", colIndex);
      this.$emit("metricSelect", colIndex);

      if (this.selectedMetrics.includes(colIndex)) {
        this.selectedMetrics = this.selectedMetrics.filter((index) => index != colIndex);
      } else {
        this.selectedMetrics.push(colIndex);
      }
    },
    validate() {
      this.$emit("validate", this.selectedColumns);
    },
  },
  computed: {
    categories: function () {
      return {
        Others: this.data.columns.filter(
          (c) =>
            c.category === "other" && c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Contexts: this.data.columns.filter(
          (c) =>
            c.category === "context" &&
            c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Inputs: this.data.columns.filter(
          (c) =>
            c.category === "input" && c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        GroundTruth: this.data.columns.filter(
          (c) =>
            c.category === "groundtruth" &&
            c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Results: this.data.columns.filter(
          (c) =>
            c.category === "results" &&
            c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Virtual: this.data.columns.filter(
          (c) =>
            c.category === "virtual" &&
            c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Tag: this.data.columns.filter(
          (c) =>
            c.category === "tag" && c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        AlgorithmOutput: this.data.columns.filter(
          (c) =>
            c.category === "Algorithm output" &&
            c.name.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
      };
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
    justify-content: space-between;
  }
  #searchBar {
    display: flex;
    gap: 3px;
    color: white;
    font-weight: bold;
    align-items: center;
    background-color: var(--greyDark);
    padding: 5px;
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
