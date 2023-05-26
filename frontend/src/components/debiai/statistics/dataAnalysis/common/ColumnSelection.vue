<template>
  <div
    id="ColumnSelection"
    class="card"
  >
    <div class="title">
      <h3>{{ title }}</h3>
      <div
        id="controls"
        v-if="validateRequiered"
      >
        <button
          class="warning"
          @click="none('')"
        >
          None
        </button>
        <button
          class="info"
          @click="all('')"
        >
          All
        </button>
      </div>
      <div class="dataGroup">
        <div
          class="data"
          v-if="validateRequiered"
        >
          <div class="name">Selected columns</div>
          <div class="value">{{ selectedColumns.length }} / {{ data.nbColumns }}</div>
        </div>
        <div
          class="data"
          v-if="minimunSelection > 0"
        >
          <div class="name">Minimum required columns</div>
          <div class="value">{{ minimunSelection }}</div>
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
          v-if="validateRequiered"
          class="green"
          @click="validate"
          :disabled="selectedColumns.length < minimunSelection"
        >
          Validate
        </button>
      </div>
    </div>
    <div id="searchBar">
      Filter :
      <input
        ref="columnsSearch"
        v-model="searchFilter"
        type="text"
      />
      <svg
        stroke="currentColor"
        fill="currentColor"
        stroke-width="0"
        viewBox="0 0 1024 1024"
        height="1em"
        width="1em"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M909.6 854.5L649.9 594.8C690.2 542.7 712 479 712 412c0-80.2-31.3-155.4-87.9-212.1-56.6-56.7-132-87.9-212.1-87.9s-155.5 31.3-212.1 87.9C143.2 256.5 112 331.8 112 412c0 80.1 31.3 155.5 87.9 212.1C256.5 680.8 331.8 712 412 712c67 0 130.6-21.8 182.7-62l259.7 259.6a8.2 8.2 0 0 0 11.6 0l43.6-43.5a8.2 8.2 0 0 0 0-11.6zM570.4 570.4C528 612.7 471.8 636 412 636s-116-23.3-158.4-65.6C211.3 528 188 471.8 188 412s23.3-116.1 65.6-158.4C296 211.3 352.2 188 412 188s116.1 23.2 158.4 65.6S636 352.2 636 412s-23.3 116.1-65.6 158.4z"
        ></path>
      </svg>
    </div>
    <div
      id="columns"
      v-if="selectedColumns"
    >
      <Category
        v-for="(columns, i) in categorys"
        :key="i"
        :columns="columns"
        :selectedColumns="selectedColumns"
        :name="i"
        :multipleSelection="validateRequiered"
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
    validateRequiered: { type: Boolean, default: true },
    minimunSelection: { type: Number, default: 0 },
    cancelAvailable: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
    defaultSelected: { type: Array, default: undefined },
  },
  created() {
    if (this.defaultSelected == undefined) {
      if (this.validateRequiered) {
        this.selectedColumns = this.data.columns
          .filter((col) => col.nbOccu > 1 && col.type !== undefined)
          .map((col) => col.index);
      }
    } else {
      this.selectedColumns = this.defaultSelected;
    }
    document.addEventListener("keydown", this.keyAndler);
  },
  mounted() {
    // Set focus on search bar
    this.$refs.columnsSearch.focus();
  },

  methods: {
    keyAndler(k) {
      if (k.key == "Escape") {
        this.$emit("cancel");
      }
    },
    columnSelected(colIndex) {
      this.$emit("colSelect", colIndex);

      if (this.validateRequiered) {
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
      if (this.validateRequiered) {
        if (name) {
          this.categorys[name].forEach((col) => {
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
      if (this.validateRequiered) {
        if (name) {
          this.categorys[name].forEach((col) => {
            this.selectedColumns = this.selectedColumns.filter((index) => index != col.index);
          });
        } else {
          this.selectedColumns = [];
        }
      }
    },
  },
  computed: {
    categorys: function () {
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
            c.category === "Algorithm output" && c.label.toLowerCase().includes(this.searchFilter.toLowerCase())
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
    document.removeEventListener("keydown", this.keyAndler);
  },
};
</script>

<style scoped>
.title {
  justify-content: space-between;
}
#ColumnSelection {
  height: 95%;
}
.title {
  justify-content: space-between;
}
#searchBar {
  display: flex;
  color: white;
  align-items: center;
  background-color: #868686;
  padding: 5px;
}
#searchBar input {
  margin: 0px 5px 0px 5px;
  height: 7px;
  padding: 0px;
}
#columns {
  display: flex;
  justify-content: center;
  align-items: top;
  flex-wrap: wrap;
  overflow-y: auto;
}
button {
  margin-left: 10px;
}
.dataGroup .data + .data {
  padding-left: 10px;
}
.dataGroup .data .value {
  padding-left: 5px;
  padding-right: 5px;
}
</style>
