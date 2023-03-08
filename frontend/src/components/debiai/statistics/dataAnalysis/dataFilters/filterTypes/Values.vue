<template>
  <div id="values">
    <!-- Add values modal -->
    <modal
      v-if="addValuePannel"
      class="aligned"
      @close="addValuePannel = false"
    >
      <h4>
        Add a value filter on the
        <span
          id="columnLabel"
          class="margedSide"
        >
          {{ filter.column.label }}
        </span>
        {{ filter.column.typeText }} column
      </h4>

      <!-- Controls -->
      <div
        class="controls aligned"
        style="margin: 20px"
      >
        <!-- 'Number' column input -->
        <div v-if="filter.column.typeText == 'Number'">
          <input
            type="number"
            v-model="newValue"
            placeholder="Value"
          />
        </div>
        <!-- 'text' and other column input -->
        <div v-else>
          <input
            type="text"
            v-model="newValue"
            placeholder="Value"
          />
        </div>

        <select
          v-model="newValue"
          v-if="filter.column.uniques"
        >
          <option
            v-for="unValues in filter.column.uniques"
            :key="unValues"
          >
            {{ unValues }}
          </option>
        </select>
      </div>

      <!-- #controls -->
      <div class="aligned centered">
        <button
          @click="addValue(false)"
          :disabled="newValue === null || newValue === ''"
        >
          Add
        </button>
        <button
          @click="addValue(true)"
          :disabled="newValue === null || newValue === ''"
        >
          Add and close
        </button>
        <button
          class="red"
          @click="addValuePannel = false"
        >
          Close
        </button>
      </div>
    </modal>

    <!-- Display values -->
    <div
      class="value"
      v-for="(value, j) in filter.values"
      :key="j"
      @click="removeValue(value)"
      title="Remove the value form the filter"
    >
      {{ value }}
    </div>
    <button @click="addValuePannel = true">Add values</button>
  </div>
</template>

<script>
export default {
  name: "Values",
  props: {
    filter: { type: Object, required: true },
  },
  data() {
    return {
      addValuePannel: false,
      newValue: null,
    };
  },
  methods: {
    addValue(closeAfter) {
      // Convert the value to the right type
      const valueToAdd =
        this.filter.column.typeText === "Num" ? parseFloat(this.newValue) : this.newValue;

      // Add the value to the filter in the store
      this.$store.commit("addValueToFilter", {
        filterId: this.filter.id,
        value: valueToAdd,
      });

      this.$emit("valueAdded", { value: valueToAdd, id: this.filter.id });
      this.newValue = null;
      if (closeAfter) this.addValuePannel = false;
    },
    removeValue(value) {
      this.$store.commit("removeValueFromFilter", {
        filterId: this.filter.id,
        value,
      });
      this.$emit("valueRemoved", { value, id: this.filter.id });
    },
  },
};
</script>

<style scoped>
#values {
  display: flex;
  padding: 10px;
  max-width: 420px;
  overflow: auto;
  margin: 0 20px 0 20px;
}

.value {
  cursor: pointer;
  display: flex;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);
  padding: 5px 10px 5px 10px;
  margin: 0 5px 0 5px;
  border-radius: 5px;
  transition: all 0.1s;
}

.value:hover {
  background: var(--danger);
  color: white;
}
</style>
