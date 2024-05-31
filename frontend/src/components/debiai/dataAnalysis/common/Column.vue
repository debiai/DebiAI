<template>
  <div id="column">
    <!-- Label -->
    <button
      v-if="columnValidStatus['status'] !== 'invalid'"
      :class="getColumnClass()"
      @click="select"
      :title="getColumnLabelTitle()"
    >
      {{ column.label }}
    </button>
    <button
      v-else
      class="label disabled"
      :title="columnValidStatus['reason']"
    >
      {{ column.label }}
    </button>

    <!-- Number of uniques values -->
    <!-- Clickable -->
    <button
      v-if="canDisplayNbOccurrence && colorSelection"
      :class="selectedAsColor ? 'nbOccurrence color btn' : 'nbOccurrence btn'"
      title="Number of uniques values
Click to set column as the main color"
      @click="selectAsColor"
    >
      {{ column.nbOccurrence }}
    </button>

    <!-- Un-clickable -->
    <div
      v-else-if="canDisplayNbOccurrence"
      class="nbOccurrence"
      title="Number of uniques values"
    >
      {{ column.nbOccurrence }}
    </div>
    <!-- Expand column button -->
    <button
      v-else
      class="nbOccurrence btn"
      title="Unfold the column"
      @click="unfoldColumn"
    >
      <inline-svg
        :src="require('@/assets/svg/expand.svg')"
        height="14"
        width="14"
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
        label: true,
        selected: this.selected,
        long: this.column.label.length > 20,
      };
    },
    getColumnLabelTitle() {
      if (this.columnValidStatus["status"] === "warning") return this.columnValidStatus["reason"];
      else if (this.selected) return "Unselect " + this.column.label;
      else return "Select " + this.column.label;
    },
    select() {
      this.$emit("selected", this.column.index);
    },
    selectAsColor() {
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
    unfoldColumn() {
      this.$emit("unfold", this.column.index);
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
      // Verify if the column is valid from the validColumnsProperties
      // Example of validColoredColumnProperties: {
      //   // Valid properties details
      //   types: [String, Number, Boolean],
      //   maxUniqueValues: 10,
      //   // Warning properties details
      //   warningTypes: ["Dict", "Array"]
      //   warningMaxUniqueValues: 5,
      //   // Everything else is invalid
      // },
      // Return "valid", "warning" or "invalid" and the reason

      // If validColumnsProperties is empty, return valid
      if (Object.keys(this.validColumnsProperties).length === 0)
        return { status: "valid", reason: "" };

      // Errors
      // Check if the column type is valid
      if (
        this.validColumnsProperties.types &&
        !this.validColumnsProperties.types.includes(this.column.typeText)
      ) {
        return {
          status: "invalid",
          reason:
            "The column type is not supported for the action that you want to perform, valid column types are: " +
            this.validColumnsProperties.types.join(", "),
        };
      }
      // Check if the number of unique values is valid
      if (
        this.validColumnsProperties.maxUniqueValues &&
        this.column.nbOccurrence > this.validColumnsProperties.maxUniqueValues
      )
        return {
          status: "invalid",
          reason:
            "The number of unique values of the column is too high, it should be bellow " +
            this.validColumnsProperties.maxUniqueValues,
        };

      // Warnings
      // Check if the type is a warning
      if (
        this.validColumnsProperties.warningTypes &&
        this.validColumnsProperties.warningTypes.includes(this.column.typeText)
      )
        return {
          status: "warning",
          reason:
            "The column type may not be supported, recommended types are: " +
            this.validColumnsProperties.types.join(", "),
        };

      // Check if the number of unique values is a warning
      if (
        this.validColumnsProperties.warningMaxUniqueValues &&
        this.column.nbOccurrence > this.validColumnsProperties.warningMaxUniqueValues
      )
        return {
          status: "warning",
          reason:
            "The number of unique values of the column may be too high, it should be bellow " +
            this.validColumnsProperties.warningMaxUniqueValues,
        };

      return { status: "valid", reason: "" };
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
  .label {
    width: 200px;
    justify-content: center;
    align-items: center;

    border: none;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--fontColorLight);
  }

  .long {
    font-size: 0.75em;
  }

  button {
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
        white 10px,
        white 20px
      );
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
    color: var(--secondary);
    font-weight: bold;
  }

  /* Type  */
  .type {
    display: flex;
    justify-content: center;
    align-items: center;

    margin: 5px;
    padding-left: 7px;
    padding-right: 7px;
    border-radius: 5px;

    color: black;

    &.Num {
      border: solid var(--number) 2px;
      color: var(--number);
    }

    &.Class {
      border: solid var(--class) 2px;
      color: var(--class);
    }

    &.Array {
      border: solid var(--array) 2px;
      color: var(--array);
    }

    &.Dict {
      border: solid var(--dict) 2px;
      color: var(--dict);
    }

    &.undefined {
      border: solid var(--undefined) 2px;
      color: var(--undefined);
    }
  }
}
</style>
