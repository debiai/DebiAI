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
        <button
          class="warning"
          @click="none"
        >
          None
        </button>
        <button
          class="info"
          @click="all"
        >
          All
        </button>
      </div>
    </div>
    <div class="content">
      <Column
        v-for="col in columns"
        :key="col.label"
        :column="col"
        :selected="selectedColumns.includes(col.index)"
        :colorSelection="colorSelection"
        v-on:selected="columnSelect"
      />
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
  },
};
</script>

<style scoped>
#Others {
  background: var(--other);
}
#Contexts {
  background: var(--context);
}
#Inputs {
  background: var(--input);
}
#GroundTruth {
  background: var(--groundthruth);
}
#Results {
  background: var(--results);
}
#Virtual {
  background: var(--virtual);
}
#Tag {
  background: var(--tag);
}

/* Controls  */
button {
  padding: 3px;
}
button + button {
  margin-left: 5px;
}
</style>
