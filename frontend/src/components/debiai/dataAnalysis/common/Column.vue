<template>
  <div id="column">
    <!-- Label button -->
    <!-- TODO: have a 'select column' if index is null -->
    <button
      id="labelButton"
      :class="getColumnClass()"
      @click="select"
      :title="getColumnLabelTitle()"
    >
      <span v-if="columnValidStatus.status === 'warning'"> ⚠️ </span>

      {{ column.label }}
    </button>

    <!-- Number of uniques values -->
    <!-- Clickable -->
    <button
      v-if="canDisplayNbOccurrence && colorSelection"
      :class="selectedAsColor ? 'nbOccurrence color' : 'nbOccurrence'"
      title="Number of uniques values
Click to set column as the main color"
      @click="selectAsColor"
    >
      {{ column.nbOccurrence }}
    </button>

    <!-- Un-clickable -->
    <div
      v-else-if="canDisplayNbOccurrence"
      :class="selectedAsColor ? 'nbOccurrence color' : 'nbOccurrence'"
      class="nbOccurrence"
      title="Number of uniques values"
    >
      {{ column.nbOccurrence }}
    </div>
    <!-- Expand column button -->
    <button
      v-else-if="column.typeText === 'Dict' || column.typeText === 'Array'"
      :class="'nbOccurrence ' + (column.unfolded ? 'color' : '')"
      :title="'Unfold the ' + column.typeText + ' column'"
      @click="unfoldColumn"
    >
      <inline-svg
        v-if="column.typeText === 'Dict'"
        :src="require('@/assets/svg/expandSide.svg')"
        height="18"
        width="18"
      />
      <inline-svg
        v-else
        :src="require('@/assets/svg/expandUp.svg')"
        height="18"
        width="18"
      />
    </button>

    <!-- Type display -->
    <div
      :class="'type ' + column.typeText"
      title="Column type"
    >
      {{ column.typeText }}
    </div>
  </div>
</template>

<script>
import columnsFiltering from "@/services/statistics/columnsFiltering";

export default {
  props: {
    column: { type: Object, required: true },
    selected: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
    validColumnsProperties: { type: Object, default: () => ({}) }, // Valid properties for the column
  },
  data() {
    return {
      columnTypesWithNoNbOccurrence: ["undefined", "Dict", "Array"],
    };
  },
  methods: {
    getColumnClass() {
      return {
        warning: this.columnValidStatus["status"] === "warning",
        selected: this.selected,
        long: this.column.label.length > 20,
        disabled: this.columnValidStatus["status"] === "invalid",
      };
    },
    getColumnLabelTitle() {
      if (
        this.columnValidStatus["status"] === "warning" ||
        this.columnValidStatus["status"] === "invalid"
      )
        return this.columnValidStatus["reason"];
      else if (this.selected) return "Unselect " + this.column.label;
      else return "Select " + this.column.label;
    },
    select() {
      if (this.columnValidStatus["status"] !== "invalid") this.$emit("selected", this.column.index);
    },
    selectAsColor() {
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
    unfoldColumn() {
      this.$store.commit("unfoldColumn", this.column.index);
    },
  },
  computed: {
    selectedAsColor: function () {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex == this.column.index;
    },
    canDisplayNbOccurrence: function () {
      return !this.columnTypesWithNoNbOccurrence.includes(this.column.typeText);
    },
    columnValidStatus: function () {
      return columnsFiltering.getColumnStatus(this.column, this.validColumnsProperties);
    },
  },
};
</script>

<style lang="scss" scoped>
#column {
  display: flex;
  margin: 5px;
  transition: all 0.3s;
  background-color: white;
  padding: 2px;
  border-radius: 4px;

  /* Label  */

  #labelButton {
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
    border: none;
    font-weight: bold;
    white-space: nowrap;
    width: 180px;
    text-overflow: ellipsis;
    color: var(--fontColorLight);

    &.long {
      .label {
        font-size: 0.75em;
      }
    }

    &.selected {
      background-color: var(--secondary);
      color: white;
    }

    &.warning {
      // Striped background
      background: repeating-linear-gradient(
        125deg,
        var(--greyLight),
        var(--greyLight) 10px,
        #f6f6f6 10px,
        #f6f6f6 20px
      );
      color: var(--fontColorLight);
    }
  }

  .nbOccurrence {
    min-width: 40px;
    padding: 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
  }

  /* Colored column */
  .nbOccurrence.color {
    border: solid 2px var(--secondary);
    color: white;
    background-color: var(--secondary);
    font-weight: bold;
    svg {
      stroke: white;
    }
  }

  /* Type  */
  .type {
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 5px;
    padding-left: 7px;
    padding-right: 7px;

    color: black;

    &.Num {
      color: var(--number);
    }

    &.Class {
      color: var(--class);
    }

    &.Array {
      color: var(--array);
    }

    &.Dict {
      color: var(--dict);
    }

    &.undefined {
      color: var(--undefined);
    }
  }
}
</style>
