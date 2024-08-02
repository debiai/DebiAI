<template>
  <div
    :id="'SampleArray' + index"
    class="dataVisualizationWidget"
  >
    <!-- Columns selection Modals -->
    <ColumnSelection
      v-show="settings"
      title="Select the columns to display in the array"
      :data="data"
      :validateRequired="true"
      :colorSelection="true"
      :defaultSelected="selectedColumnsIds"
      v-on:cancel="settings = false"
      v-on:validate="columnsSelect"
    />

    <!-- Array -->
    <div v-if="arrayData !== null">
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th
              v-for="(column, index) in arrayLabels"
              :key="index"
            >
              {{ column }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, index) in arrayData"
            :key="index"
          >
            <td
              v-for="(cell, index) in row"
              :key="index"
            >
              {{ cell }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// components
import ColumnSelection from "../../common/ColumnSelection";

export default {
  components: {
    ColumnSelection,
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
  },
  data() {
    return {
      selectedColumnsIds: [],
      settings: true,
      columnsSelection: false,

      arrayLabels: [],
      arrayData: null,
    };
  },
  created() {
    // Select the 3 firsts columns
    for (let i = 0; i < 3; i++) if (this.data.nbColumns > i) this.selectedColumnsIds.push(i);

    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });
    this.$parent.$on("redraw", this.updateArray);
  },
  mounted() {},
  methods: {
    updateArray() {
      const maxData = 10;
      this.selectedColumnsIds = this.selectedColumnsIds.filter((i) => this.data.columnExists(i));
      const selectedData = this.data.selectedData.slice(0, maxData);
      const labels = this.selectedColumnsIds.map((i) => this.data.getColumn(i).label);
      const nbRows = Math.min(selectedData.length, maxData); // Number of rows to display
      const data = new Array(nbRows);
      this.arrayLabels = labels;

      for (let i = 0; i < data.length; i++) data[i] = new Array(this.selectedColumnsIds.length); // Number of columns

      this.selectedColumnsIds.forEach((columnIndex, i) => {
        const col = this.data.getColumn(columnIndex);
        selectedData.map((j, indRow) => (data[indRow][i] = col.values[j]));
      });

      this.settings = false;
      this.arrayData = data;

      this.$parent.$emit("drawn");
    },
    columnsSelect(columnIndexes) {
      this.selectedColumnsIds = columnIndexes;

      this.settings = false;
      this.updateArray();
    },
  },
  computed: {
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    selectedDataUpdate() {
      this.$parent.selectedDataWarning = true;
    },
  },
};
</script>

<style scoped lang="scss">
table {
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    max-width: 200px;
    // make text wrap, not overflow
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th {
    background-color: #f2f2f2;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
}
</style>
