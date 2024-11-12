<template>
  <div class="input">
    <!-- Title and description -->
    <div class="top">
      <h4>
        {{ input.name }}
      </h4>

      <!-- Input type -->
      <span
        class="inputType tag"
        v-if="input.type == 'array'"
        >Array of {{ input.arrayType }}s</span
      >
      <span
        class="inputType tag"
        v-else
        >{{ input.type }}</span
      >

      <!-- Description -->
      <div class="description">{{ input.description }}</div>
    </div>

    <!-- Input method selection & input value form -->
    <div class="middle">
      <!-- Values -->
      <div
        v-if="input.type === 'number' || input.type === 'string'"
        title="Value of the input that will be sent to the Algo Provider"
      >
        Select a value:

        <input
          :type="input.type"
          v-model="value"
          :readonly="isProjectId"
          @input="valueChanged"
        />
      </div>

      <!-- Suggestions: -->
      <div
        v-if="input.availableValues && input.availableValues.length > 0"
        title="Values suggested by the Algo Provider"
      >
        <select
          v-model="value"
          @change="valueChanged"
        >
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
        v-if="input.type === 'number' && input.min !== null && input.min !== undefined"
        title="Minimum value accepted by the Algo Provider"
        :class="'tag ' + (value < input.min ? 'error' : 'success')"
      >
        {{ ">=" }} {{ input.min }}
      </div>
      <div
        v-if="input.type === 'number' && input.max !== null && input.max !== undefined"
        title="Maximum value accepted by the Algo Provider"
        :class="'tag ' + (value > input.max ? 'error' : 'success')"
      >
        &lt; {{ input.max }}
        <!-- &lt; is <= -->
      </div>

      <!-- Array input type, select how to input the array values -->
      <div
        v-if="input.type === 'array' && !isIdList"
        class="arrayInputType"
      >
        <span style="display: flex; align-items: center; padding-right: 10px">
          Array input methods
          <documentationBlock>
            Select how you want to input the array values.
            <br />
            <br />
            <b>Manual</b>: <br />Input the values manually, separated by commas.
            <br />
            <br />
            <b>Complete Column data</b>: <br />Select a column from the data to use as input.
            <br />
            <br />
            <b>Selected Column data</b>:<br />
            Select a column from the data and only use the selected values as input. </documentationBlock
          >:
        </span>

        <!-- input options -->
        <button
          :class="'radioBtn ' + (selectedArrayInputOption == 'manual' ? 'selected' : '')"
          @click="selectedArrayInputOption = 'manual'"
        >
          Manual
        </button>
        <button
          :class="'radioBtn ' + (selectedArrayInputOption == 'column' ? 'selected' : '')"
          @click="
            selectedArrayInputOption = 'column';
            columnSelected(columnIndex);
          "
        >
          Complete Column data
        </button>
        <button
          :class="
            'radioBtn ' + (selectedArrayInputOption == 'columnSelectedData' ? 'selected' : '')
          "
          @click="
            selectedArrayInputOption = 'columnSelectedData';
            columnSelected(columnIndex);
          "
        >
          Selected Column data
        </button>
      </div>

      <!-- Array input type for idList -->
      <div
        v-if="input.type === 'array' && isIdList"
        class="arrayInputType"
      >
        <!-- input options -->
        <button
          :class="'radioBtn ' + (selectedArrayInputOption == 'column' ? 'selected' : '')"
          @click="
            selectedArrayInputOption = 'column';
            idListInputTypeSelected('column');
          "
        >
          Complete project Id List
        </button>
        <button
          :class="
            'radioBtn ' + (selectedArrayInputOption == 'columnSelectedData' ? 'selected' : '')
          "
          @click="
            selectedArrayInputOption = 'columnSelectedData';
            idListInputTypeSelected('columnSelectedData');
          "
        >
          Selected Id List
        </button>
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
          placeholder="1,2,3"
          v-model="manualValue"
          @input="valueChanged"
        />
      </div>

      <!-- Column selection -->
      <div
        v-if="
          input.type === 'array' &&
          ['column', 'columnSelectedData'].includes(selectedArrayInputOption)
        "
      >
        <div class="arrayInput">
          <div v-if="!isIdList">
            <ColumnSelectionButton
              :data="data"
              :defaultColumnIndex="columnIndex"
              :title="'Select a column to use as input for ' + input.name"
              :colorSelection="false"
              v-on:selected="columnSelected"
            />
          </div>
          <div
            class="nbValues"
            v-if="value !== null && value !== undefined"
          >
            {{ value.length }} values
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// components
import ColumnSelectionButton from "../common/ColumnSelectionButton.vue";

export default {
  name: "UseAlgo",
  components: {
    ColumnSelectionButton,
  },
  props: {
    input: { type: Object, required: true },
    data: { type: Object, required: true },
  },
  data: () => {
    return {
      value: null,
      manualValue: null,
      projectId: null,

      // Array input
      selectedArrayInputOption: "manual",
      columnIndex: null,
    };
  },
  mounted() {
    // Default values setup
    // Set the projectId as the default value if the input is projectId
    if (this.isProjectId) this.value = this.$store.state.ProjectPage.projectId;

    // Set the idList as the default value if the input is idList
    if (this.isIdList && this.data.columnExists("Data ID")) {
      const idColumn = this.data.getColumnByLabel("Data ID");
      this.idColumnsIndex = idColumn.index;
      this.selectedArrayInputOption = "column";
      this.value = this.data.getColumn(this.idColumnsIndex).values;
    }

    // Set the default value if it exists
    if (this.input.default !== null && this.input.default !== undefined)
      this.value = this.input.default;
    // Else, set the first available value as the default value
    else if (this.input.availableValues && this.input.availableValues.length > 0)
      this.value = this.input.availableValues[0];

    this.$emit("inputValueUpdate", { value: this.value, columnLabel: null });
  },
  methods: {
    valueChanged() {
      // This function is called when the value of the input changes
      // For manual input for array, we convert the string to an array of numbers
      if (this.input.type === "array" && this.selectedArrayInputOption === "manual")
        this.value = this.manualValue.split(",");

      // Check if the value is correct and send it to the parent
      if (!this.valueMatchInputType) return;

      this.$emit("inputValueUpdate", { value: this.getGoodType(this.value), columnLabel: null });
    },
    columnSelected(index) {
      // This function is called when the user selects a column to use as input
      if (index === null) return;

      this.columnIndex = index;

      if (!this.data.columnExists(index)) return;

      const column = this.data.getColumn(index);
      const dataValues = column.values;

      // Convert to the good type and send to parent
      let value = null;
      if (this.selectedArrayInputOption === "columnSelectedData")
        value = this.getGoodType(this.data.selectedData.map((id) => dataValues[id]));
      else value = this.getGoodType(dataValues);

      this.$emit("inputValueUpdate", { value: value, columnLabel: column.label });
    },
    idListInputTypeSelected(type) {
      // This function is called when the user selects the type of input for the idList
      // Set the value of the idList according to the selected type
      const idColumn = this.data.getColumn(this.idColumnsIndex);
      if (!idColumn) return;

      let dataIdValues = null;
      if (type == "column") dataIdValues = idColumn.values;
      else dataIdValues = this.data.selectedData.map((id) => dataIdValues[id]);

      this.$emit("inputValueUpdate", { value: dataIdValues, columnLabel: idColumn.label });
    },
    getGoodType(value) {
      if (this.input.type === "number") {
        return Number(value);
      }
      if (this.input.type === "array" && value !== null) {
        if (this.input.arrayType === "number") {
          if (this.selectedArrayInputOption === "columnSelectedData") {
            return value;
          } else if (this.selectedArrayInputOption === "column") {
            return value;
          } else if (this.selectedArrayInputOption === "manual") {
            return value.map((v) => Number(v));
          }
        } else {
          // we don't need to convert the values
          return value;
        }
      }
      return value;
    },
  },
  computed: {
    valueMatchInputType() {
      if (this.input.type === "number") return !isNaN(this.value);
      else if (this.input.type === "string") return typeof this.value === "string";
      else if (this.input.type === "array") return Array.isArray(this.value);
      else return true;
    },
    isIdList: function () {
      return this.input.type === "array" && this.input.name === "idList";
    },
    isProjectId: function () {
      return this.input.type === "string" && this.input.name === "projectId";
    },
  },
  watch: {},
};
</script>

<style scoped lang="scss">
.input {
  border-bottom: 1px solid var(--greyDark);
  padding: 30px 10px;
  display: flex;
  justify-content: flex-start;
  flex-direction: column;
  transition: 0.2s;
  gap: 10px;

  .top {
    display: flex;
    align-items: center;
    gap: 7px;
    .description {
      text-align: left;
      color: var(--fontColorLight);
    }
  }

  .middle {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;

    .arrayInputType {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      gap: 5px;
    }
  }

  .bot {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 5px;

    .arrayInput {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      gap: 10px;

      input {
        flex: 1;
      }
    }
  }

  input,
  select {
    border: 1px solid var(--greyDark);
    border-radius: 4px;
    padding: 2px 4px;
    font-size: 1em;
    width: 100px;
  }
}
</style>
