<template>
  <div class="input">
    <!-- {{ input }} -->
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

    <!-- Length min and max -->
    <div
      v-if="input.type === 'array'"
      title="Range of the length of the input value that will be sent to the Algo Provider"
    >
      <input
        type="number"
        v-model.number="value"
        :min="input.lengthMin"
        :max="input.lengthMax"
      />
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
    };
  },
  mounted() {
    if (this.input.default !== null && this.input.default !== undefined)
      this.value = this.input.default;
    else if (this.input.availableValues && this.input.availableValues.length > 0)
      this.value = this.input.availableValues[0];
  },
  methods: {
    inputDetail(input) {
      const optionalFields = [
        { field: "default", name: "Default value" },
        { field: "min", name: "Min number" },
        { field: "max", name: "Max number" },
        { field: "availableValues", name: "Suggested values" },
        { field: "lengthMin", name: "Minimum length" },
        { field: "lengthMax", name: "Maximum length" },
      ];
      let details = "";

      optionalFields.forEach((field) => {
        if (input[field.field] !== null && input[field.field] !== undefined) {
          details += field.name + ": " + input[field.field] + "<br/>";
        }
      });

      return details;
    },
  },
  computed: {
    valueWithGoodType() {
      if (this.input.type === "number") return Number(this.value);
      else return this.value;
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
  align-items: center;
  justify-content: flex-start;
  gap: 5px;
}
.top p {
  margin: 4px;
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
  color: red;
  border-color: red;
  background-color: transparent;
}
</style>
