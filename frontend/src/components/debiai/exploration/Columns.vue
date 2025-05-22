<template>
  <div class="categories">
    <div
      v-for="(columns, category) in columnsGroupedByCategory"
      :key="category"
      class="category"
    >
      <h3>{{ category }}</h3>
      <div class="columns">
        <div
          v-for="column in columns"
          :key="column.name"
          class="column"
        >
          <button
            @click="selectColumn(column)"
            :class="{
              selected: selectedColumns.includes(column.name),
            }"
          >
            {{ column.name }}
          </button>
          <div class="nbUnique">{{ column.nbUniqueValues }}</div>
          <div
            class="type"
            :class="[column.type]"
          >
            {{ column.type }}
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="unsupportedColumns.length"
      class="category"
    >
      <h3>Unsupported Columns</h3>
      <div class="columns unsupported">
        <div
          v-for="column in unsupportedColumns"
          :key="column.name"
          class="column"
        >
          <button disabled>
            {{ column.name }}
          </button>
          <div class="nbUnique">{{ column.nbUniqueValues }}</div>
          <div
            class="type"
            :class="[column.type]"
          >
            {{ column.type }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Columns",
  props: {
    project: {
      type: Object,
      required: true,
    },
    exploration: {
      type: Object,
      required: true,
    },
    columns_statistics: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedColumns: [],
    };
  },
  methods: {
    selectColumn(column) {
      const columnName = column.name;
      if (this.selectedColumns.includes(columnName)) {
        this.selectedColumns = this.selectedColumns.filter((name) => name !== columnName);
      } else {
        this.selectedColumns.push(columnName);
      }
    },
    isUnsupported(column) {
      const unsupportedTypes = ["dict", "list", "other", "mixed"];
      return unsupportedTypes.includes(column.type);
    },
  },
  computed: {
    columnsGroupedByCategory() {
      const columns = this.columns_statistics;
      const columnsGroupedByCategory = {};

      for (const column of columns) {
        if (this.isUnsupported(column)) continue;
        const category = column.category || "Other";
        if (!columnsGroupedByCategory[category]) columnsGroupedByCategory[category] = [];
        columnsGroupedByCategory[category].push(column);
      }

      return columnsGroupedByCategory;
    },
    unsupportedColumns() {
      const columns = this.columns_statistics;
      return columns.filter((column) => this.isUnsupported(column));
    },
  },
};
</script>

<style lang="scss" scoped>
.categories {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;

  .category {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    h3 {
      margin-bottom: 0.5rem;
      border-bottom: 1px solid #ccc;
      text-align: left;
      text-transform: capitalize;
    }

    .columns {
      display: flex;
      flex-wrap: wrap;
      flex-direction: column;
      gap: 0.5rem;

      .column {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        .nbUnique {
          font-weight: bold;
        }
        .type {
          &.text {
            color: var(--class);
          }
          &.number {
            color: var(--number);
          }
          &.list {
            color: var(--array);
          }
          &.dict {
            color: var(--dict);
          }
        }
      }
    }
  }
}
</style>
