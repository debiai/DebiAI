<template>
  <div
    v-if="columns.length"
    id="category"
    class="card"
  >
    <!-- Title -->
    <div
      class="title"
      :id="name"
    >
      <h2>{{ name }}</h2>
      <div style="flex: 1"></div>
      <div
        id="controls"
        v-if="multipleSelection"
      >
        <button @click="none">None</button>
        <button @click="all">All</button>
      </div>
    </div>
    <!-- Column list -->
    <div class="content">
      <!-- Column groups -->
      <div
        class="group"
        v-for="(cols, group) in groupedColumns"
        :key="group"
      >
        <Collapsible style="margin: 3px; width: 300px">
          <template v-slot:header>
            {{ group }}
            <!-- Nb selected columns in group: -->
            <NbItem
              v-if="multipleSelection && cols.length > 1"
              :nbSelected="getNbSelectedColumns(cols)"
              :nbTotal="cols.length"
            />
          </template>
          <template v-slot:body>
            <div class="columns">
              <Column
                v-for="col in cols"
                :key="col.label"
                :column="col"
                :selected="selectedColumns.includes(col.index)"
                :colorSelection="colorSelection"
                :validColumnsProperties="validColumnsProperties"
                v-on:selected="columnSelect"
              />
            </div>
          </template>
        </Collapsible>
      </div>

      <!-- Ungrouped columns  -->
      <div
        id="ungrouped"
        v-for="col in ungroupedColumns"
        :key="col.index"
      >
        <!-- Without child -->
        <Column
          v-if="!col.hasChildren()"
          :column="col"
          :selected="selectedColumns.includes(col.index)"
          :colorSelection="colorSelection"
          :validColumnsProperties="validColumnsProperties"
          v-on:selected="columnSelect"
        />

        <!-- With child -->
        <ColumnParent
          v-else
          :data="data"
          :column="col"
          :selectedColumns="selectedColumns"
          :colorSelection="colorSelection"
          :validColumnsProperties="validColumnsProperties"
          v-on:selected="columnSelect"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Column from "./Column";
import ColumnParent from "./ColumnParent";
export default {
  components: {
    Column,
    ColumnParent,
  },
  props: {
    data: { type: Object, required: true },
    name: { type: String, required: true },
    columns: { type: Array, required: true },
    selectedColumns: { type: Array },
    multipleSelection: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
    validColumnsProperties: { type: Object, default: () => ({}) },
  },
  methods: {
    columnSelect(colIndex) {
      this.$emit("columnSelected", colIndex);
    },
    all() {
      this.$emit("all", this.name);
    },
    none() {
      this.$emit("none", this.name);
    },
    getNbSelectedColumns(columns) {
      return columns.filter((col) => this.selectedColumns.includes(col.index)).length;
    },
  },
  computed: {
    groupedColumns() {
      // Group columns by group
      const groups = {
        // "Group name": [column, column, ...],
      };

      this.columns.forEach((col) => {
        // Ignore columns that have a parentColumnIndex
        if (col.parentColumnIndex) return;

        if (col.group) {
          if (!groups[col.group]) {
            groups[col.group] = [];
          }
          groups[col.group].push(col);
        }
      });

      return groups;
    },

    ungroupedColumns() {
      return this.columns.filter((col) => !col.group & !col.parentColumnIndex);
    },
  },
};
</script>

<style scoped>
#category {
  min-width: 250px;
}
</style>
