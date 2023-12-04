<template>
  <div class="input">
    <div class="top">
      <p>
        {{ input.name }}
      </p>

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
          :readonly="isProjectId"
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
        {{ "<=" }} {{ input.max }}
      </div>

      <!-- Array input type-->
      <div
        v-if="input.type === 'array' && !isIdList"
        class="arrayInputType"
      >
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
            columnSelection = true;
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
            columnSelection = true;
          "
        >
          Selected Column data
        </button>
      </div>
      <div
        v-if="input.type === 'array' && isIdList"
        class="arrayInputType"
      >
        <!-- input options -->
        <button
          :class="'radioBtn ' + (selectedArrayInputOption == 'column' ? 'selected' : '')"
          @click="
            selectedArrayInputOption = 'column';
            idListSelected('column');
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
            idListSelected('columnSelectedData');
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
          v-model="value"
          placeholder="1,2,3"
        />
      </div>

      <!-- Column selection Modal -->
      <modal
        v-if="columnSelection"
        @close="columnSelection = false"
      >
        <ColumnSelection
          :title="'Select a column to use as input for ' + input.name"
          :data="data"
          :validateRequired="false"
          :colorSelection="false"
          :defaultSelected="[columnIndex]"
          v-on:cancel="columnSelection = false"
          v-on:colSelect="columnSelected"
        />
      </modal>
      <div
        v-if="
          input.type === 'array' &&
          ['column', 'columnSelectedData'].includes(selectedArrayInputOption)
        "
      >
        <div class="arrayInput">
          <div v-if="!isIdList">
            <Column
              v-if="columnIndex !== null"
              :column="data.columns.find((c) => c.index == columnIndex)"
              :colorSelection="false"
              v-on:selected="columnSelection = true"
            />
            <button
              v-else
              @click="columnSelection = true"
            >
              Select a column
            </button>
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
import ColumnSelection from "../common/ColumnSelection.vue";
import Column from "../common/Column";

export default {
  name: "UseAlgo",
  components: {
    ColumnSelection,
    Column,
  },
  props: {
    input: { type: Object, required: true },
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  data: () => {
    return {
      value: null,
      projectId: null,

      // Array input
      selectedArrayInputOption: "manual",
      columnIndex: null,
      columnSelection: false,
    };
  },
  mounted() {
    if (this.isProjectId) this.value = this.$store.state.ProjectPage.projectId;
    if (this.isIdList) {
      this.idColumnsIndex = this.data.columns.findIndex((c) => c.label === "Data ID");
      this.selectedArrayInputOption = "column";
      this.value = this.data.columns[this.idColumnsIndex].values;
    }

    if (this.input.default !== null && this.input.default !== undefined)
      this.value = this.input.default;
    else if (this.input.availableValues && this.input.availableValues.length > 0)
      this.value = this.input.availableValues[0];
    this.$emit("inputValueUpdate", this.value);
  },
  methods: {
    columnSelected(index) {
      if (index === null) return;

      this.columnSelection = false;
      this.columnIndex = index;
      if (this.selectedArrayInputOption === "columnSelectedData") {
        this.value = this.selectedData.map((id) => {
          return this.data.columns[index].values[id];
        });
      } else {
        this.value = this.data.columns[index].values;
      }
      this.$emit("inputValueUpdate", this.value);
    },
    idListSelected(type) {
      if (type == "column") {
        this.value = this.data.columns[this.idColumnsIndex].values;
      } else {
        const selectedValues = this.selectedData.map((id) => {
          return this.data.columns[this.idColumnsIndex].values[id];
        });
        this.value = selectedValues;
      }
      this.$emit("inputValueUpdate", this.value);
    },
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
        if (this.input.arrayType === "number") {
          if (this.selectedArrayInputOption === "columnSelectedData") return this.value;
          else if (this.selectedArrayInputOption === "column") return this.value;
          else if (this.selectedArrayInputOption === "manual") {
            return this.value.split(",").map((v) => Number(v));
          }
        } else {
          // we don't need to convert the values
          return this.value;
        }
      } else return this.value;
    },
    isIdList: function () {
      return this.input.type === "array" && this.input.name === "idList";
    },
    isProjectId: function () {
      return this.input.type === "string" && this.input.name === "projectId";
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
  border: 1px solid var(--greyDark);
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
.description {
  color: var(--fontColorLight);
  padding-right: 30px;
}

input,
select {
  border: 1px solid var(--greyDark);
  border-radius: 4px;
  padding: 2px 4px;
  font-size: 1em;
  width: 100px;
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
