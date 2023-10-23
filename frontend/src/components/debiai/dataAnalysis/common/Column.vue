<template>
  <div id="column">
    <!-- Label display -->
    <button
      v-if="column.type !== undefined && !disabled"
      :class="(selected ? 'label selected ' : 'label ') + (column.label.length > 20 ? 'long' : '')"
      @click="select"
      :title="selected ? 'Unselect ' + column.label : 'Select ' + column.label"
    >
      {{ column.label }}
    </button>
    <div
      v-else-if="column.type == undefined"
      class="label disabled"
    >
      {{ column.label }}
    </div>
    <div
      v-else
      class="label"
    >
      {{ column.label }}
    </div>

    <!-- Number of uniques values display -->
    <div
      v-if="disabled || (!reduced && (!colorSelection || column.type == undefined))"
      :class="selectedAsColor ? 'nbOccurrence color' : 'nbOccurrence'"
      title="Number of uniques values"
    >
      {{ column.nbOccurrence }}
    </div>
    <button
      v-else-if="!reduced"
      :class="selectedAsColor ? 'nbOccurrence color btn' : 'nbOccurrence btn'"
      title="Number of uniques values
Click to set column as the main color"
      @click="selectAsColor"
    >
      {{ column.nbOccurrence }}
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
    reduced: { type: Boolean, default: false },
    colorSelection: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
  methods: {
    select() {
      this.$emit("selected", this.column.index);
    },
    selectAsColor() {
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
  },
  computed: {
    selectedAsColor: function () {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex == this.column.index;
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
    text-overflow: "...";

    color: var(--fontColorLight);
  }

  .long {
    font-size: 0.75em;
  }

  button.selected {
    background-color: var(--secondary);
    color: white;
  }

  .disabled {
    cursor: not-allowed;
    width: 120px;

    background-color: var(--undefined);
    color: rgb(27, 27, 27);
  }

  /* Occurrence */
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
    &.undefined {
      border: solid var(--undefined) 2px;
      color: var(--undefined);
    }
  }
}
</style>
