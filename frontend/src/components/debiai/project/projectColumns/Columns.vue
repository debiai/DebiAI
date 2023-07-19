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
    padding: 13px;
    margin: 0 3px;
    border: 1px solid #00000027;

    &:first-child {
      margin-top: 0;
      border-radius: 10px 10px 0 0;
    }

    &:last-child {
      margin-bottom: 0;
      border-radius: 0 0 10px 10px;
    }

    &.selectable {
      cursor: pointer;
      transition: all 0.1s ease-in-out;

      // Add a 3D effect
      &:hover {
        box-shadow: 0 0 3px #00000027;
        background-color: #0000000d;
      }

      &:active {
        box-shadow: 0 0 3px #00000027 inset;
      }
      &.selected {
        background-color: var(--primary);
        color: white;
        font-weight: bold;
      }
    }
  }

  .columnType {
    width: 50px;
    text-align: right;
    opacity: 0.5;
  }
}
</style>
