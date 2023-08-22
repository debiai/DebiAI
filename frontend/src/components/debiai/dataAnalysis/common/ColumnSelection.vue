<template>
  <div
    id="ColumnSelection"
    class="card"
  >
    <div class="title">
      <h3>{{ title }}</h3>
      <div
        id="controls"
        v-if="validateRequired"
      >
        <button @click="none('')">None</button>
        <button @click="all('')">All</button>
      </div>
      <div class="dataGroup">
        <div
          class="data"
          v-if="validateRequired"
        >
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
        :multipleSelection="validateRequired"
        :colorSelection="colorSelection"
        v-on:columnSelected="columnSelected"
        v-on:all="all"
        v-on:none="none"
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
  },
  created() {
    if (this.defaultSelected == undefined) {
      if (this.validateRequired) {
        this.selectedColumns = this.data.columns
          .filter((col) => col.nbOccu > 1 && col.type !== undefined)
          .map((col) => col.index);
      }
    } else {
      this.selectedColumns = this.defaultSelected;
    }
    document.addEventListener("keydown", this.keyHandler);
  },
  mounted() {
    // Set focus on search bar
    this.$refs.columnsSearch.focus();
  },

  methods: {
    keyHandler(k) {
      if (k.key == "Escape") {
        this.$emit("cancel");
      }
    },
    columnSelected(colIndex) {
      this.$emit("colSelect", colIndex);

      if (this.validateRequired) {
        if (this.selectedColumns.includes(colIndex)) {
          this.selectedColumns = this.selectedColumns.filter((index) => index != colIndex);
        } else {
          this.selectedColumns.push(colIndex);
        }
      }
    },
    validate() {
      this.$emit("validate", this.selectedColumns);
    },
    all(name) {
      if (this.validateRequired) {
        if (name) {
          this.categories[name].forEach((col) => {
            if (!this.selectedColumns.includes(col.index) && col.nbOccu > 1)
              this.selectedColumns.push(col.index);
          });
        } else {
          this.selectedColumns = this.data.columns
            .filter((col) => col.type !== undefined && col.nbOccu > 1)
            .map((col) => col.index);
        }
      }
    },
    none(name) {
      if (this.validateRequired) {
        if (name) {
          this.categories[name].forEach((col) => {
            this.selectedColumns = this.selectedColumns.filter((index) => index != col.index);
          });
        } else {
          this.selectedColumns = [];
        }
      }
    },
  },
  computed: {
    categories: function () {
      return {
        Others: this.data.columns.filter(
          (c) =>
            c.category === "other" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Contexts: this.data.columns.filter(
          (c) =>
            c.category === "context" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Inputs: this.data.columns.filter(
          (c) =>
            c.category === "input" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        GroundTruth: this.data.columns.filter(
          (c) =>
            c.category === "groundtruth" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Results: this.data.columns.filter(
          (c) =>
            c.category === "results" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Virtual: this.data.columns.filter(
          (c) =>
            c.category === "virtual" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        Tag: this.data.columns.filter(
          (c) =>
            c.category === "tag" && c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
        ),
        AlgorithmOutput: this.data.columns.filter(
          (c) =>
            c.category === "Algorithm output" &&
            c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
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
#ColumnSelection {
  height: 95%;
  width: 98%;
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
