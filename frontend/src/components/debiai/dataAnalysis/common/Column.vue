<template>
  <div id="column">
    <!-- Label button -->
    <button
      id="labelButton"
      :class="getColumnClass()"
      @click="select"
      @contextmenu.prevent="handleRightClick"
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
      :class="'nbOccurrence ' + (column.unfolded || column.unfoldedHorizontally ? 'color' : '')"
      :title="'Fold or unfold the ' + column.typeText + ' column'"
      @click="unfoldColumn"
    >
      <inline-svg
        v-if="column.arrayColumnSizeNumber && !column.unfoldedHorizontally && !column.unfolded"
        :src="require('@/assets/svg/expand.svg')"
        height="14"
        width="14"
      />
      <inline-svg
        v-else-if="column.typeText === 'Dict' || column.unfoldedHorizontally"
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

    <!-- Nb null values pie chart -->
    <div
      class="nbNullValues"
      v-if="column.nbNullValues > 0"
      :title="column.nbNullValues + ' null values'"
    >
      <div
        class="pie"
        :style="{ '--p': (column.nbNullValues / column.originalValues.length) * 100 }"
      />
      {{ Math.ceil((column.nbNullValues / column.originalValues.length) * 100) }}%
    </div>

    <!-- Menu -->
    <transition name="fade">
      <dropdown-menu
        v-if="showMenu"
        :menu="getColumnMenu()"
        :position="{ x: this.mousePos.x, y: this.mousePos.y }"
        @close="showMenu = false"
      />
    </transition>
  </div>
</template>

<script>
import columnsFiltering from "@/services/statistics/columnsFiltering";
import DropdownMenu from "@/components/common/DropdownMenu";

export default {
  components: {
    DropdownMenu,
  },
  props: {
    column: { type: Object, required: true },
    selected: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
    validColumnsProperties: { type: Object, default: () => ({}) }, // Valid properties for the column
  },
  data() {
    return {
      // Menu
      showMenu: false,
      mousePos: { x: 0, y: 0 },

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
    getUnfoldIcon() {
      if (
        this.column.arrayColumnSizeNumber &&
        !this.column.unfoldedHorizontally &&
        !this.column.unfolded
      )
        return "expand";
      else if (this.column.typeText === "Dict" || this.column.unfoldedHorizontally)
        return "expandSide";
      else return "expandUp";
    },
    select(event) {
      event.stopPropagation();
      if (this.columnValidStatus["status"] !== "invalid") this.$emit("selected", this.column.index);
    },
    selectAsColor(event) {
      event?.stopPropagation();
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
    unfoldColumn(event) {
      event?.stopPropagation();
      this.$store.commit("unfoldColumn", this.column.index);
    },
    deleteColumn() {
      this.column.delete();
    },
    addArrayLength() {
      this.column.addArrayLength();
    },

    // Column menu
    getColumnMenu() {
      const menu = [];

      // Select as color
      if (this.canDisplayNbOccurrence)
        menu.push({
          name: this.selectedAsColor ? "Unselect as color" : "Select as color",
          action: this.selectAsColor,
        });

      // Unfold column vertically
      if (this.column.typeText === "Dict" || this.column.typeText === "Array")
        menu.push({
          name: this.column.unfolded || this.column.unfoldedHorizontally ? "Fold" : "Unfold",
          action: this.unfoldColumn,
          icon: this.getUnfoldIcon(),
        });

      // Add array metrics
      if (this.column.typeText === "Array" && this.column.canAddArrayLength())
        menu.push({
          name: "Add values length",
          action: this.addArrayLength,
          icon: "gear",
        });

      // Add the delete column button
      if (this.column.canBeDeleted())
        menu.push({
          name: "Delete column",
          action: this.deleteColumn,
          icon: "close",
        });

      return menu;
    },
    handleRightClick(event) {
      // Get the widget position x and y on screen
      let widgetX = this.$el.getBoundingClientRect().x;
      let widgetY = this.$el.getBoundingClientRect().y;

      // Get the mouse position relative to the widget
      this.mousePos.x = event.clientX - widgetX;
      this.mousePos.y = event.clientY - widgetY;

      this.showMenu = true;

      // Store the data for the menu
      this.$store.commit("setOpenedColumnMenuId", this.column.index);
      event.stopPropagation();
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
    // Dropdown menu
    openedColumnMenuId() {
      return this.$store.state.StatisticalAnalysis.openedColumnMenuId;
    },
  },

  watch: {
    openedColumnMenuId() {
      if (this.openedColumnMenuId !== this.column.index) this.showMenu = false;
    },
  },
};
</script>

<style lang="scss" scoped>
#column {
  position: relative;
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

    /* Colored column */
    &.color {
      color: white;
      background-color: var(--secondary);
      font-weight: bold;
      svg {
        stroke: white;
      }
    }
  }

  div.nbOccurrence {
    margin-left: 3px;
    padding: 2px;
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

  /* Pie chart */
  .nbNullValues {
    display: flex;
    align-items: center;
    gap: 2px;
    font-size: 0.8em;
    color: var(--greyDarker);
    font-weight: bold;

    .pie {
      position: relative;
      width: 20px;
      height: 20px;
      display: inline-grid;
      place-content: center;
      border-radius: 50%;
      background: var(--greyLight);
    }
    .pie:before {
      content: "";
      position: absolute;
      border-radius: 50%;
      inset: 0;
      background: conic-gradient(var(--greyDarker) calc(var(--p) * 1%), #0000 0);
    }
  }
}
</style>
