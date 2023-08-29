<template>
  <div class="columns">
    <div
      :class="getColumnClass(column)"
      v-for="column in columns"
      :key="column.index"
      @click="selectColumn(column)"
    >
      <div class="columnName">
        {{ column.name }}
      </div>
      <div class="columnType">
        {{ column.type !== undefined ? column.type : "auto" }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Columns",
  components: {},
  props: {
    columns: { type: Array, required: true },
    selectable: { type: Boolean, default: false },
    selectedColumns: { type: Array, default: () => [] },
  },
  data: () => {
    return {};
  },
  created() {},
  methods: {
    selectColumn(column) {
      this.$emit("selectColumn", column.index);
    },
    getColumnClass(column) {
      return {
        column: true,
        selectable: this.selectable,
        selected: this.selectedColumns.includes(column.index),
      };
    },
  },
  computed: {},
};
</script>

<style scoped lang="scss">
.columns {
  display: flex;
  flex-direction: column;

  .column {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 10px;
    margin: 3px;
    border: 1px solid var(--greyDark);
    border-radius: 4px;
  }

  .columnType {
    width: 50px;
    text-align: right;
    opacity: 0.5;
  }
}
</style>
