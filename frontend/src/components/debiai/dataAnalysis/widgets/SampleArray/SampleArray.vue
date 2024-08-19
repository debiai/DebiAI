<template>
  <div
    :id="'SampleArray' + index"
    class="sampleArray dataVisualizationWidget"
  >
    <!-- Columns selection Modals -->
    <ColumnSelection
      v-show="settings"
      title="Select the columns to display in the array"
      :data="data"
      :validateRequired="true"
      :colorSelection="true"
      :defaultSelected="selectedColumnsIds"
      :minimumSelection="1"
      v-on:cancel="settings = false"
      v-on:validate="columnsSelect"
    />

    <!-- Array -->
    <div
      class="array"
      v-if="arrayData !== null"
    >
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

      <!-- Pagination -->
      <div class="pagination">
        <span style="width: 70px">
          <button
            v-if="currentPage > 0"
            @click="pageDown"
          >
            ◀
          </button>
        </span>
        <span class="pageDisplayer">{{ currentPage + 1 }} / {{ maxPage + 1 }}</span>
        <span style="width: 70px">
          <button
            v-if="currentPage < maxPage"
            @click="pageUp"
          >
            ▶
          </button>
        </span>
      </div>
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
      currentSamplePosition: 0,
      dataPerPage: 0,
      maxPage: 0,
    };
  },
  created() {
    // Select the 3 firsts columns
    this.selectedColumnsIds = this.data.columns.slice(0, 10).map((c) => c.index);

    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });
    this.$parent.$on("redraw", this.updateArray);
    this.$parent.$parent.$on("GridStack_resizestop", () => {
      this.updateArray();
    });
  },
  methods: {
    updateArray() {
      if (this.data.selectedData.length === 0 || this.settings) return;

      // Get the number of rows to display and the height of the div
      const d = document.getElementById("SampleArray" + this.index) || null;
      if (!d) return;
      const rowHeight = 27;
      this.dataPerPage = Math.floor((d.clientHeight * 0.95) / rowHeight) - 3; // Number of rows to display

      // Calculate the number of pages
      this.maxPage = Math.ceil(this.data.selectedData.length / this.dataPerPage) - 1;

      // Get the labels of the columns
      this.selectedColumnsIds = this.selectedColumnsIds.filter((i) => this.data.columnExists(i));
      this.arrayLabels = this.selectedColumnsIds.map((i) => this.data.getColumn(i).label);

      // Get the data to display
      this.adjustPagination();

      const selectedData = this.data.selectedData.slice(
        this.currentSamplePosition,
        this.currentSamplePosition + this.dataPerPage
      );

      // Create the array of data
      const nbRows = Math.min(selectedData.length, this.dataPerPage); // Number of rows to display
      const data = new Array(nbRows);
      for (let i = 0; i < data.length; i++) data[i] = new Array(this.selectedColumnsIds.length);
      this.selectedColumnsIds.forEach((columnIndex, i) => {
        const col = this.data.getColumn(columnIndex);
        selectedData.map((j, indRow) => (data[indRow][i] = col.values[j]));
      });

      this.arrayData = data;

      this.settings = false;
      this.$parent.$emit("drawn");
    },
    columnsSelect(columnIndexes) {
      this.selectedColumnsIds = columnIndexes;

      if (this.selectedColumnsIds.length > 0) {
        this.settings = false;
        this.updateArray();
      }
    },
    pageUp() {
      this.currentSamplePosition += this.dataPerPage;
      this.updateArray();
    },
    pageDown() {
      if (this.currentSamplePosition > this.dataPerPage) {
        this.currentSamplePosition -= this.dataPerPage;
        this.updateArray();
      } else {
        this.currentSamplePosition = 0;
        this.updateArray();
      }
    },
    adjustPagination() {
      // If the currentSamplePosition is greater than the number of rows
      if (this.currentSamplePosition >= this.data.selectedData.length)
        this.currentSamplePosition = this.data.selectedData.length - this.dataPerPage;

      // After a resize, adjust the pagination to have the currentSamplePosition
      // In the start of the page
      this.currentSamplePosition = this.currentPage * this.dataPerPage;
      if (this.currentSamplePosition >= this.data.selectedData.length)
        this.currentSamplePosition = this.data.selectedData.length - this.dataPerPage;
    },
  },
  computed: {
    selectedDataUpdate() {
      return this.data.selectedData;
    },
    currentPage() {
      if (this.dataPerPage === 0) return 0;
      return Math.ceil(this.currentSamplePosition / this.dataPerPage);
    },
  },
  watch: {
    selectedDataUpdate() {
      this.$parent.selectedDataWarning = true;
    },
    settings() {
      // If the settings are closed, update the array
      setTimeout(() => {
        if (!this.settings) this.updateArray();
      }, 30);
    },
  },
};
</script>

<style scoped lang="scss">
.array {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;

  table {
    width: 100%;
    border-collapse: collapse;

    th,
    td {
      border: 1px solid #ddd;
      text-align: left;
      max-width: 200px;
      height: 25px;
      padding-left: 3px;
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

  .pagination {
    display: flex;
    justify-content: center;
    margin: 10px 0px;

    button {
      background-color: #f2f2f2;
      border: none;
      color: black;
      padding: 8px 16px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      cursor: pointer;
    }

    .pageDisplayer {
      padding: 8px 16px;
      font-size: 16px;
    }
  }
}
</style>
