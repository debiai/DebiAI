<template>
  <div id="ColumnSelectionButton">
    <!-- Column selected -->
    <Column
      v-if="selectedColumnIndex !== null"
      :column="data.getColumn(selectedColumnIndex)"
      :colorSelection="colorSelection"
      v-on:selected="columnSelectionModal = true"
    />

    <!-- No column selected, click to select -->
    <button
      v-else
      id="labelButton"
      @click="columnSelectionModal = true"
      :title="tooltip"
    >
      {{ title }}
    </button>

    <!-- Remove button -->
    <button
      v-if="canBeRemoved && selectedColumnIndex !== null"
      class="red"
      @click="columnRemoved"
    >
      Remove
    </button>

    <!-- Column selection modal -->
    <modal
      v-if="columnSelectionModal"
      @close="columnSelectionModal = false"
    >
      <ColumnSelection
        :title="modalTitle ? modalTitle : title"
        :data="data"
        :defaultSelected="defaultSelectedColumns"
        :validColumnsProperties="validColumnsProperties"
        :validateRequired="false"
        :colorSelection="true"
        v-on:cancel="columnSelectionModal = false"
        v-on:colSelect="columnSelected"
      />
    </modal>
  </div>
</template>

<script>
import ColumnSelection from "./ColumnSelection";
import Column from "./Column";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  props: {
    data: { type: Object, required: true },
    title: { type: String, default: "Select a column" },
    modalTitle: { type: String, default: null },
    tooltip: { type: String, default: null },
    defaultColumnIndex: { type: String, default: null },
    validColumnsProperties: { type: Object, default: () => ({}) },
    canBeRemoved: { type: Boolean, default: false },
    colorSelection: { type: Boolean, default: false },
    openOnCreation: { type: Boolean, default: false },
  },
  data() {
    return {
      selectedColumnIndex: null,
      columnSelectionModal: false,
    };
  },
  created() {
    // Set the default column index
    // Check if the default column index is valid
    if (this.defaultColumnIndex !== null && this.data.columnExists(this.defaultColumnIndex))
      this.selectedColumnIndex = this.defaultColumnIndex;

    // Open the modal on creation
    if (this.openOnCreation) this.columnSelectionModal = true;
  },
  mounted() {},
  methods: {
    columnSelected(columnIndex) {
      this.selectedColumnIndex = columnIndex;
      this.columnSelectionModal = false;
      this.$emit("selected", columnIndex);
    },
    columnRemoved() {
      this.$emit("removed");
    },
  },
  computed: {
    defaultSelectedColumns() {
      return this.defaultColumnIndex !== null ? [this.defaultColumnIndex] : [];
    },
    dataColumns() {
      return this.data.columns;
    },
  },
  watch: {
    defaultColumnIndex() {
      // Check if the default column index is valid
      if (this.defaultColumnIndex !== null && this.data.columnExists(this.defaultColumnIndex)) {
        // Set the column as the new selected column
        this.selectedColumnIndex = this.defaultColumnIndex;
      } else {
        this.selectedColumnIndex = null;
      }
    },
    dataColumns() {
      // Check if the selected column still exists
      if (this.selectedColumnIndex !== null && !this.data.columnExists(this.selectedColumnIndex)) {
        this.selectedColumnIndex = null;
        this.$emit("selected", null);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#ColumnSelectionButton {
  display: flex;
  align-items: center;

  #labelButton {
    min-width: 30px;
    margin: 6px; // To match the column height
    white-space: nowrap;
  }
}
</style>
