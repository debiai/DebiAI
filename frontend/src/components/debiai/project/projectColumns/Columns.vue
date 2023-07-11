<template>
  <div class="columns">
    <div
      class="column"
      v-for="column in columns"
      :key="column.name"
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
  props: { columns: { type: Array, required: true } },
  // Expected project columns example :
  //  [
  //      { "name": "storage", "category": "other" },
  //      { "name": "age", "category": "context" },
  //      { "name": "path", "category": "input" },
  //      { "name": "label", "category": "groundtruth" },
  //      { "name": "type" }, # category is not specified, it will be "other"
  //  ]

  // Expected project results columns example :
  // [
  //   { name: "Model prediction", type: "number" },
  //   { name: "Model error", type: "number" },
  // ];
  data: () => {
    return {};
  },
  created() {},
  methods: {},
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
    border: 1px solid #00000027;
    border-radius: 10px;
  }

  .columnType {
    width: 50px;
    text-align: right;
    opacity: 0.5;
  }
}
</style>
