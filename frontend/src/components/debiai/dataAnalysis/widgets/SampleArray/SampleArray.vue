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
        <span class="buttons">
          <button
            :disabled="!(currentPage > 0)"
            @click="
              currentSamplePosition = 0;
              updateArray();
            "
          >
            ◀◀
          </button>
        </span>
        <span class="buttons">
          <button
            :disabled="!(currentPage > 0)"
            @click="pageDown"
          >
            ◀
          </button>
        </span>
        <span
          class="pageDisplayer"
          title="Jump to page"
          @click="pageToJumpTo = currentPage + 1"
          >{{ currentPage + 1 }} / {{ maxPage + 1 }}
        </span>
        <span class="buttons">
          <button
            :disabled="!(currentPage < maxPage)"
            @click="pageUp"
          >
            ▶
          </button>
        </span>
        <span class="buttons">
          <button
            :disabled="!(currentPage < maxPage)"
            @click="
              currentSamplePosition = maxPage * dataPerPage;
              updateArray();
            "
          >
            ▶▶
          </button>
        </span>
      </div>
    </div>

    <!-- Page selection modal -->
    <modal
      v-if="pageToJumpTo !== null"
      @close="pageToJumpTo = null"
    >
      <div>
        <h3 style="margin-bottom: 10px; display: flex; justify-content: space-between; gap: 10px">
          Jump to page
          <button
            @click="pageToJumpTo = null"
            class="red"
          >
            Cancel
          </button>
        </h3>
        <form @submit.prevent="jumpToPage">
          <input
            type="number"
            v-model="pageToJumpTo"
            min="1"
            max="maxPage + 1"
            style="padding: 5px"
          />
          <button type="submit">Jump</button>
        </form>
      </div>
    </modal>
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
      selectedDataIds: [],
      settings: true,
      columnsSelection: false,

      arrayLabels: [],
      arrayData: null,
      currentSamplePosition: 0,
      dataPerPage: 0,
      maxPage: 0,

      pageToJumpTo: null,
    };
  },
  created() {
    // Select the 3 firsts columns
    this.selectedColumnsIds = this.data.columns.slice(0, 10).map((c) => c.index);

    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });
    this.$parent.$on("redraw", this.drawArray);
    this.$parent.$parent.$on("GridStack_resizestop", () => {
      this.updateArray();
    });
  },
  methods: {
    drawArray() {
      // Copy the selected data array
      this.selectedDataIds = this.data.selectedData.slice();
      this.updateArray();
      this.settings = false;
      this.$parent.$emit("drawn");
    },
    updateArray() {
      if (this.selectedDataIds.length === 0 || this.settings) return;

      // Get the number of rows to display and the height of the div
      const d = document.getElementById("SampleArray" + this.index) || null;
      if (!d) return;
      const rowHeight = 27;
      this.dataPerPage = Math.floor((d.clientHeight * 0.95) / rowHeight) - 3; // Number of rows to display

      // Calculate the number of pages
      this.maxPage = Math.ceil(this.selectedDataIds.length / this.dataPerPage) - 1;

      // Get the labels of the columns
      this.selectedColumnsIds = this.selectedColumnsIds.filter((i) => this.data.columnExists(i));
      this.arrayLabels = this.selectedColumnsIds.map((i) => this.data.getColumn(i).label);

      // Get the data to display
      this.adjustPagination();

      const selectedData = this.selectedDataIds.slice(
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
    },
    columnsSelect(columnIndexes) {
      this.selectedColumnsIds = columnIndexes;

      if (this.selectedColumnsIds.length > 0) {
        this.settings = false;
        this.drawArray();
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
      if (this.currentSamplePosition >= this.selectedDataIds.length)
        this.currentSamplePosition = this.selectedDataIds.length - this.dataPerPage;

      // After a resize, adjust the pagination to have the currentSamplePosition
      // In the start of the page
      this.currentSamplePosition = this.currentPage * this.dataPerPage;
      if (this.currentSamplePosition >= this.selectedDataIds.length)
        this.currentSamplePosition = this.selectedDataIds.length - this.dataPerPage;
    },
    jumpToPage() {
      if (this.pageToJumpTo <= 1) this.pageToJumpTo = 1;
      if (this.pageToJumpTo > this.maxPage + 1) this.pageToJumpTo = this.maxPage + 1;

      this.currentSamplePosition = (this.pageToJumpTo - 1) * this.dataPerPage;
      this.updateArray();
      this.pageToJumpTo = null;
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
    margin-bottom: 10px;
    gap: 3px;

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
      width: 80px;
      padding: 8px 16px;
      font-size: 16px;
      cursor: pointer;

      &:hover {
        background-color: #f2f2f2;
        border-radius: 5px;
      }
    }

    .buttons {
      display: flex;
      justify-content: center;
      align-items: center;

      width: 50px;
      button {
        width: 100%;
        &:hover {
          background-color: #f2f2f2;
          border-radius: 5px;
        }
      }
    }
  }
}
</style>
