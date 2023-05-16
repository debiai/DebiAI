<template>
  <div class="input">
    <div class="top">
      <p>
        {{ input.name }}
      </p>

      <!-- Input type -->
      <span
        class="inputType"
        v-if="input.type == 'array'"
        >Array of {{ input.arrayType }}s</span
      >
      <span
        class="inputType"
        v-else
        >{{ input.type }}</span
      >

      <!-- description -->
      <p class="description">{{ input.description }}</p>

      <!-- Values -->
      <div
        v-if="input.type === 'number' || input.type === 'string'"
        title="Value of the input that will be sent to the Algo Provider"
      >
        <input
          :type="input.type"
          v-model="value"
        />
      </div>

      <!-- Suggestions: -->
      <div
        v-if="input.availableValues && input.availableValues.length > 0"
        title="Values suggested by the Algo Provider"
      >
        <select v-model="value">
          <option
            v-for="(value, index) in input.availableValues.slice(0, 100)"
            :key="index"
            :value="value"
          >
            {{ value }}
          </option>
        </select>
      </div>

      <!-- Min and max -->
      <div
        class="min"
        v-if="input.type === 'number' && input.min !== null && input.min !== undefined"
        title="Minimum value accepted by the Algo Provider"
        :class="value < input.min ? 'error' : 'success'"
      >
        {{ ">=" }} {{ input.min }}
      </div>
      <div
        class="max"
        v-if="input.type === 'number' && input.max !== null && input.max !== undefined"
        title="Maximum value accepted by the Algo Provider"
        :class="value > input.max ? 'error' : 'success'"
      >
        {{ "<=" }} {{ input.max }}
      </div>

      <!-- Array input type-->
      <div
        v-if="input.type === 'array'"
        class="arrayInputType"
      >
        <!-- input options -->
        <div
          :class="'option ' + (selectedArrayInputOption == 'manual' ? 'selected' : '')"
          @click="selectedArrayInputOption = 'manual'"
        >
          Manual
        </div>
        <div
          :class="'option ' + (selectedArrayInputOption == 'column' ? 'selected' : '')"
          @click="selectedArrayInputOption = 'column'"
        >
          Column analysis data
        </div>
        <div
          :class="'option ' + (selectedArrayInputOption == 'columnSelectedData' ? 'selected' : '')"
          @click="selectedArrayInputOption = 'columnSelectedData'"
        >
          Column selected data
        </div>
      </div>
    </div>
    <div class="bot">
      <!-- Array input type-->
      <div
        v-if="input.type === 'array' && selectedArrayInputOption == 'manual'"
        class="arrayInput"
      >
        Manual input, separated by commas:
        <input
          type="text"
          v-model="value"
          placeholder="1,2,3"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UseAlgo",
  props: {
    input: { type: Object, required: true },
  },
  data: () => {
    return {
      value: null,

      // Array input
      selectedArrayInputOption: "manual",
    };
  },
  mounted() {
    if (this.input.default !== null && this.input.default !== undefined)
      this.value = this.input.default;
    else if (this.input.availableValues && this.input.availableValues.length > 0)
      this.value = this.input.availableValues[0];
    this.$emit("inputValueUpdate", this.value);
  },
  methods: {
    // TODO: Arrays
    // inputDetail(input) {
    //   const optionalFields = [
    //     { field: "default", name: "Default value" },
    //     { field: "min", name: "Min number" },
    //     { field: "max", name: "Max number" },
    //     { field: "availableValues", name: "Suggested values" },
    //     { field: "lengthMin", name: "Minimum length" },
    //     { field: "lengthMax", name: "Maximum length" },
    //   ];
    //   let details = "";
    //   optionalFields.forEach((field) => {
    //     if (input[field.field] !== null && input[field.field] !== undefined) {
    //       details += field.name + ": " + input[field.field] + "<br/>";
    //     }
    //   });
    //   return details;
    // },
  },
  computed: {
    valueMatchInputType() {
      if (this.input.type === "number") return !isNaN(this.value);
      else if (this.input.type === "string") return typeof this.value === "string";
      else if (this.input.type === "array") return Array.isArray(this.value);
      else return true;
    },
    valueWithGoodType() {
      if (this.input.type === "number") return Number(this.value);
      if (this.input.type === "array" && this.value !== null) {
        if (this.input.arrayType === "number") return this.value.split(",").map((v) => Number(v));
        else return this.value.split(",");
      } else return this.value;
    },
  },
  watch: {
    valueWithGoodType: function (val) {
      this.$emit("inputValueUpdate", val);
    },
  },
};
</script>

<style scoped>
.input {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0px 20px;
  font-size: 1.2em;
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  transition: 0.2s;
}
.top {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
}
.inputType {
  color: #909090;
  border: 1px solid #ccc;
  padding: 0 2px 0 2px;
  border-radius: 4px;
  font-size: 0.9em;
}
.description {
  font-size: 0.9em;
  color: #909090;
  padding-right: 30px;
}

input,
select {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 1em;
  width: 100px;
}

.min,
.max {
  font-size: 0.9em;
  padding: 2px 4px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.success {
  color: green;
  border-color: green;
}
.error {
  color: var(--danger);
  border-color: var(--danger);
  background-color: transparent;
}

/* arrayInputType */
.arrayInputType {
  display: flex;
  gap: 5px;
}
.arrayInputType .option {
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 0.9em;
  background-color: #eee;
}

.arrayInputType .option:hover {
  background-color: #ddd;
}
.arrayInputType .option.selected {
  color: white;
  background-color: var(--primary);
  border-color: var(--primary);
}

.bot {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
}
.arrayInput {
  flex: 1;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
}
.arrayInput input {
  flex: 1;
}
</style>
