<template>
  <div
    v-if="columns.length"
    id="category"
    class="card"
  >
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
    <div class="content">
      <div
        class="group"
        v-for="(cols, group) in groupedColumns"
        :key="group"
      >
        <!-- Grouped columns -->
        <div
          v-if="group"
          class="group-title"
        >
          <Collapsible style="margin: 3px; width: 320px">
            <template v-slot:header>
              <h4>
                {{ group }}
                <!-- Nb selected columns in group: -->
                <span
                  class="nbItem blue"
                  v-if="getNbSelectedColumns(cols)"
                >
                  {{ getNbSelectedColumns(cols) }}
                </span>

                <span v-if="getNbSelectedColumns(cols)"> / </span>
                <!-- Nb columns in group: -->
                <span class="nbItem">
                  {{ cols.length }}
                </span>
              </h4>
            </template>
            <template v-slot:body>
              <div class="columns">
                <Column
                  v-for="col in cols"
                  :key="col.label"
                  :column="col"
                  :selected="selectedColumns.includes(col.index)"
                  :colorSelection="colorSelection"
                  v-on:selected="columnSelect"
                />
              </div>
            </template>
          </Collapsible>
        </div>
        <!-- Ungrouped columns -->
        <div
          v-else
          class="group-title"
        >
          <Column
            v-for="col in cols"
            :key="col.label"
            :column="col"
            :selected="selectedColumns.includes(col.index)"
            :colorSelection="colorSelection"
            v-on:selected="columnSelect"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Column from "./Column";
export default {
  components: {
    Column,
  },
  props: {
    name: { type: String, required: true },
    columns: { type: Array, required: true },
    selectedColumns: { type: Array },
    multipleSelection: { type: Boolean, default: true },
    colorSelection: { type: Boolean, default: false },
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
      const groups = { "": [] };

      this.columns.forEach((col) => {
        if (col.group) {
          if (!groups[col.group]) {
            groups[col.group] = [];
          }
          groups[col.group].push(col);
        } else {
          groups[""].push(col);
        }
      });

      return groups;
    },
  },
};
</script>

<style scoped>
</style>
