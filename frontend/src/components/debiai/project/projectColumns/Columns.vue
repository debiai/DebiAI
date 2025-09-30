<template>
  <div class="columns">
    <div
      class="column"
      v-for="column in columns"
      :key="column.name"
    >
      <div class="columnInfo">
        <span class="columnName">
          {{ column.name }}
        </span>

        <span
          v-if="column.metrics && column.metrics.nbUniqueValues !== undefined"
          class="tag"
        >
          {{ column.metrics.nbUniqueValues }}
          <span class="columnType">
            {{ column.type !== undefined ? column.type : "auto" }}
          </span>
        </span>
        <span
          v-else
          class="columnType"
        >
          {{ column.type !== undefined ? column.type : "auto" }}
        </span>
        <span
          v-if="column.tags && column.tags.length"
          class="tags"
        >
          <span
            v-for="tag in column.tags"
            :key="tag"
            class="tag"
            >{{ tag }}</span
          >
        </span>

        <div style="flex: 1"></div>

        <documentationBlock v-if="column.metrics">
          <div class="metrics-info">
            <div><strong>Unique values:</strong> {{ column.metrics.nbUniqueValues }}</div>
            <div><strong>Null values:</strong> {{ column.metrics.nbNullValues }}</div>
            <div v-if="column.type === 'number' && column.metrics.average !== null">
              <strong>Average:</strong> {{ formatNumber(column.metrics.average) }}
            </div>
            <div v-if="column.type === 'number' && column.metrics.min !== null">
              <strong>Min:</strong> {{ formatNumber(column.metrics.min) }}
            </div>
            <div v-if="column.type === 'number' && column.metrics.max !== null">
              <strong>Max:</strong> {{ formatNumber(column.metrics.max) }}
            </div>
            <div v-if="column.metadata && column.metadata.category">
              <strong>Category:</strong> {{ column.metadata.category }}
            </div>
          </div>
        </documentationBlock>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Columns",
  components: {},
  props: { columns: { type: Array, required: true } },
  data: () => {
    return {};
  },
  created() {},
  methods: {
    formatNumber(value) {
      if (value === null || value === undefined) return "N/A";
      if (typeof value === "object" && value.parsedValue !== undefined) {
        return Number(value.parsedValue).toFixed(2);
      }
      return Number(value).toFixed(2);
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
    align-items: flex-start;
    padding: 10px;
    margin: 3px;
    border: 1px solid var(--greyDark);
    border-radius: 4px;

    .columnInfo {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 4px;

      .columnName {
        font-weight: 500;
        margin-right: 4px;
      }
    }
  }

  .columnType {
    font-size: 0.9em;
    opacity: 0.7;
    font-style: italic;
  }

  .tags {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
    max-width: 300px;

    .tag {
      background-color: #e1f5fe;
      padding: 1px 4px;
      border-radius: 8px;
      font-size: 0.75em;
      color: #0277bd;
    }
  }

  .metrics-info {
    font-size: 0.9em;
    line-height: 1.4;

    div {
      margin: 2px 0;
    }

    strong {
      color: var(--fontColor);
    }
  }
}
</style>
