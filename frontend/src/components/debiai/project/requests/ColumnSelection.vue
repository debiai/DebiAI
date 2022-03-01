<template>
  <div id="columnSelection">
    <div id="head">
      <h3>{{ title }}</h3>
      <button class="red" style="margin-left: 20px" @click="$emit('cancel')">
        Cancel
      </button>
    </div>
    <div class="column" v-for="(column, i) in columns" :key="i">
      <button
        @click="$emit('colSelect', column.name)"
        :class="column.isId ? 'info' : ''"
      >
        {{ column.name }}
      </button>
      {{ column.type }}
    </div>
  </div>
</template>

<script>
export default {
  props: { title: { type: String, default: "Select a column" } },
  computed: {
    columns() {
      return this.$store.state.ProjectPage.columns;
    },
  },
};
</script>

<style>
#head {
  display: flex;
  justify-content: space-between;
  padding: 10px;
}
</style>