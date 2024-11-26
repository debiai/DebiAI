<template>
  <div>
    <!-- Add values modal -->
    <modal
      v-if="addValuePanel"
      class="aligned"
      @close="addValuePanel = false"
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
          v-if="filter.column.uniques && filter.column.uniques.length < 30"
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
        <button @click="addValue(false)">Add</button>
        <button @click="addValue(true)">Add and close</button>
        <button
          class="red"
          @click="addValuePanel = false"
        >
          Close
        </button>
      </div>
    </modal>

    <!-- Display values -->

    <span
      v-if="!readOnly"
      id="values"
    >
      <button
        class="value removable"
        v-for="(value, j) in filter.values"
        :key="j"
        @click="removeValue(value)"
        title="Remove the value form the filter"
      >
        <span v-if="value !== null">
          {{ value }}
        </span>
        <span
          v-else
          style="opacity: 0.7"
        >
          Null
        </span>
      </button>
      <button
        @click="addValuePanel = true"
        v-if="!readOnly"
      >
        Add values
      </button>
    </span>
    <span
      v-else
      id="values"
    >
      <div
        class="value"
        v-for="(value, j) in filter.values"
        :key="j"
      >
        {{ value }}
      </div>
    </span>
  </div>
</template>

<script>
export default {
  name: "Values",
  props: {
    filter: { type: Object, required: true },
    readOnly: { type: Boolean, default: false },
  },
  data() {
    return {
      addValuePanel: false,
      newValue: null,
    };
  },
  methods: {
    addValue(closeAfter) {
      // Convert the value to the right type
      let valueToAdd = this.newValue;
      if (this.filter.column.typeText === "Num") {
        valueToAdd = parseFloat(this.newValue);
        if (isNaN(valueToAdd)) valueToAdd = null;
      } else {
        if (valueToAdd === "") valueToAdd = null;
      }

      // Add the value to the filter in the store
      this.$store.commit("addValueToFilter", {
        filterId: this.filter.id,
        value: valueToAdd,
      });

      this.$emit("valueAdded", { value: valueToAdd, id: this.filter.id });
      this.newValue = null;
      if (closeAfter) this.addValuePanel = false;
    },
    removeValue(value) {
      if (this.readOnly) return;

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
  max-width: 420px;
  overflow: auto;
  margin: 0 20px;
  gap: 5px;
}

.value {
  display: flex;
  border: solid var(--greyDarker) 1px;
  padding: 5px;
  border-radius: 3px;
}

.removable:hover {
  cursor: pointer;
  border-color: var(--danger);
  color: var(--danger);
}
</style>
