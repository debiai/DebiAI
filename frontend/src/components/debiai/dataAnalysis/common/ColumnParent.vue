<template>
  <div id="ColumnParent">
    <Collapsible
      open
      simple
    >
      <!-- Display a column as the header -->
      <template v-slot:header>
        <Column
          :column="column"
          :selected="selectedColumns.includes(column.index)"
          :colorSelection="colorSelection"
          :validColumnsProperties="validColumnsProperties"
          v-on:selected="columnSelect(column.index)"
        />
      </template>
      <!-- Display the child columns in the collapsible body -->
      <template v-slot:body>
        <Column
          v-for="col in childColumns"
          :key="col.index"
          :column="col"
          :selected="selectedColumns.includes(col.index)"
          :colorSelection="colorSelection"
          :validColumnsProperties="validColumnsProperties"
          v-on:selected="columnSelect(col.index)"
        />
      </template>
    </Collapsible>
  </div>
</template>

<script>
import Column from "./Column";
export default {
  name: "ColumnParent",
  components: {
    Column,
  },
  props: {
    data: { type: Object, required: true },
    column: { type: Object, required: true },
    selectedColumns: { type: Array },
    colorSelection: { type: Boolean, default: false },
    validColumnsProperties: { type: Object, default: () => ({}) },
  },
  methods: {
    columnSelect(columnIndex) {
      this.$emit("selected", columnIndex);
    },
  },
  computed: {
    childColumns() {
      return this.column.getChildrenColumns();
    },
  },
};
</script>

<style scoped></style>
