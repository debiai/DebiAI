<template>
  <div>
    <table>
      <thead>
        <tr>
          <th
            v-for="key in keys"
            :key="key"
          >
            {{ key }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in data.slice(0, max_length_to_show)"
          :key="index"
        >
          <td
            v-for="key in keys"
            :key="key"
          >
            {{ item[key] }}
          </td>
        </tr>
        <tr v-if="data.length > max_length_to_show">
          <td :colspan="keys.length">
            <span>
              <b>And {{ data.length - max_length_to_show }} more...</b>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "DataTable",
  data() {
    return {
      max_length_to_show: 20,
    };
  },
  props: {
    data: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  computed: {
    keys() {
      if (this.data.length === 0) return [];
      return Object.keys(this.data[0]);
    },
  },
};
</script>

<style scoped lang="scss">
table {
  width: 100%;
  border-collapse: collapse;

  th,
  td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
  }
}
</style>
