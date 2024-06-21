<template>
  <div id="ColumnUnfoldingMenu">
    <!-- Vertical or horizontal unfolding menu -->
    <Modal
      @close="columnIndexToUnfoldVerticallyOrHorizontally = null"
      v-if="columnIndexToUnfoldVerticallyOrHorizontally"
    >
      <div id="verticalOrHorizontalUnfoldingMenu">
        <h3>How do you want to unfold the column?</h3>

        <p>
          You are about to unfold a column containing arrays with
          <br />
          a constant size of length
          <b class="tag">
            {{
              data.getColumn(columnIndexToUnfoldVerticallyOrHorizontally).arrayColumnSizeNumber
            }} </b
          >.
        </p>

        <p>Do you want to unfold it vertically or horizontally?</p>

        <div
          id="verticalUnfold"
          class="unfoldMethod"
        >
          Unfolding the column vertically will <br />
          add as many lines as the size of the array.
          <button @click="unfoldVertically(columnIndexToUnfoldVerticallyOrHorizontally)">
            Unfold vertically
          </button>
        </div>
        <div
          id="horizontalUnfold"
          class="unfoldMethod"
        >
          Unfolding the column horizontally will <br />
          add as many columns as the size of the array.
          <button @click="unfoldHorizontally(columnIndexToUnfoldVerticallyOrHorizontally)">
            Unfold horizontally
          </button>
        </div>
      </div>
    </Modal>

    <!-- Horizontal unfolding error message-->
    <Modal
      @close="horizontalUnfoldErrorMessage = ''"
      v-if="horizontalUnfoldErrorMessage"
    >
      <div id="horizontalUnfoldErrorMessage">
        <h3>Error</h3>
        <p>The column cannot be unfolded horizontally.</p>
        <p>{{ horizontalUnfoldErrorMessage }}</p>
      </div>

      <button @click="horizontalUnfoldErrorMessage = ''">Close</button>
    </Modal>

    <!-- Select columns to unfold -->
    <Modal
      @close="columnIndexToSelectHorizontalColumns = null"
      v-if="columnIndexToSelectHorizontalColumns"
    >
      <div id="selectColumnsToUnfold">
        <h3>Select columns to unfold</h3>
        <p>
          You are about to unfold a column containing a dictionary.
          <br />
          Please select the columns you want to unfold.
        </p>

        <div id="columnsToUnfold">
          <div
            v-for="(column, index) in newPossibleColumns"
            :key="index"
            class="columnToUnfold"
          >
            <input
              type="checkbox"
              :id="column"
              v-model="column.selected"
            />
            <label :for="column">{{ column.key }}</label>
          </div>
        </div>

        <button @click="unfoldHorizontally(columnIndexToSelectHorizontalColumns)">
          Unfold horizontally
        </button>
      </div>
    </Modal>
  </div>
</template>

<script>
export default {
  name: "ColumnUnfoldingMenu",
  data() {
    return {
      // Array columns
      columnIndexToUnfoldVerticallyOrHorizontally: null,

      // Dict columns
      columnIndexToSelectHorizontalColumns: null,
      newPossibleColumns: [],
      horizontalUnfoldErrorMessage: "",
    };
  },
  props: {
    data: { type: Object, required: true },
  },
  created() {},
  methods: {
    unfoldColumn(columnIndex) {
      const column = this.data.getColumn(columnIndex);
      if (!column) return;

      if (column.arrayColumnSizeNumber) {
        if (column.unfolded) {
          // Fold if the column is already unfolded
          this.data.unfoldVertically(columnIndex);
          return;
        }

        // Ask if we unfold vertically or horizontally
        this.columnIndexToUnfoldVerticallyOrHorizontally = columnIndex;
      } else if (column.typeText === "Dict") {
        if (column.unfoldedVertically) {
          // Fold if the column is already unfolded
          this.data.unfoldHorizontally(columnIndex);
          return;
        }

        // Ask what columns to select
        const newPossibleColumns = column.getPossibleColumnsToUnfold();
        if (newPossibleColumns.error) this.horizontalUnfoldErrorMessage = newPossibleColumns.error;
        else {
          this.newPossibleColumns = newPossibleColumns.keys.map((key) => {
            return {
              selected: true,
              key: key,
            };
          });
          console.log(this.newPossibleColumns);
          this.columnIndexToSelectHorizontalColumns = columnIndex;
        }
      } else if (column.typeText === "Array") this.data.unfoldVertically(columnIndex);
    },
    unfoldVertically(columnIndex) {
      this.data.unfoldVertically(columnIndex);
      this.columnIndexToUnfoldVerticallyOrHorizontally = null;
    },
    unfoldHorizontally(columnIndex) {
      const columnsToUnfold = this.newPossibleColumns
        .filter((column) => column.selected)
        .map((column) => column.key);
      this.data.unfoldHorizontally(columnIndex, columnsToUnfold);
      this.columnIndexToSelectHorizontalColumns = null;
      this.newPossibleColumns = [];
    },
  },
  computed: {
    unfoldCounter() {
      return this.$store.state.StatisticalAnalysis.unfoldCounter;
    },
  },
  watch: {
    unfoldCounter() {
      // Update the unfolded column
      const columnIndex = this.$store.state.StatisticalAnalysis.unfoldedColumnIndex;
      this.unfoldColumn(columnIndex);
    },
  },
};
</script>

<style scoped lang="scss">
#ColumnUnfoldingMenu {
  #verticalOrHorizontalUnfoldingMenu {
    text-align: left;
    .unfoldMethod {
      margin-bottom: 10px;
      padding: 10px;
      border: 1px solid var(--greyDark);
      border-radius: 5px;
    }
  }

  #selectColumnsToUnfold {
    text-align: left;
    #columnsToUnfold {
      display: flex;
      flex-wrap: wrap;
      .columnToUnfold {
        display: flex;
        align-items: center;
        margin: 5px;
      }
    }
  }
}
</style>
