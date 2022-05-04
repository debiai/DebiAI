<template>
  <div id="virtualColumnCreator">
    <!-- Col selection Modal -->
    <modal v-if="selectedColToChange !== null">
      <ColumnSelection
        title="Select a column"
        :data="data"
        :validateRequiered="false"
        :defaultSelected="[
          selectedColToChange == 0
            ? firstColumn
            : rules[selectedColToChange - 1].colIndex,
        ]"
        v-on:cancel="selectedColToChange = null"
        v-on:colSelect="selectCol"
      />
    </modal>

    <!-- Rule selection Modal -->
    <modal v-if="ruleSelection">
      <h2 class="aligned spaced marged">
        Select an operation
        <button @click="ruleSelection = false" class="red">Cancel</button>
      </h2>
      <button
        v-for="(operator, operatorName) in operators"
        :key="operatorName"
        @click="selectRule(operatorName)"
      >
        {{ operator.display }}
      </button>
    </modal>

    <!-- modal title -->
    <h2 id="title" class="aligned spaced marged">
      <div style="display: flex">
        Custom column creation
        <DocumentationBlock>
          Create a new column based on the analysis columns and some simple
          arythmetic operations.
        </DocumentationBlock>
      </div>
      <div>
        <button @click="rules = []" class="red">Clear columns</button>
        <button @click="$emit('cancel')" class="red">Cancel</button>
      </div>
    </h2>

    <!-- column name & rules -->
    <div id="content">
      <!-- new column name input -->
      <div class="dataGroup">
        <div class="data">
          <div class="name">Virtual column name</div>
          <div class="value">
            <input type="text" placeholder="New column" v-model="colName" />
          </div>
        </div>
      </div>

      <!-- Operations list -->
      <div id="colList">
        <Column
          :column="data.columns.find((c) => c.index == firstColumn)"
          v-on:selected="selectedColToChange = 0"
        />

        <div class="rule" v-for="(rule, index) in rules" :key="index">
          <button
            @click="
              ruleSelection = true;
              ruleSelectionIndex = index;
            "
          >
            {{ rule.operator.display }}
          </button>
          <Column
            :column="data.columns.find((c) => c.index == rule.colIndex)"
            v-on:selected="selectedColToChange = index + 1"
          />
        </div>

        <button @click="addRule">Add column</button>
      </div>

      <button @click="create" :disabled="!columnOk">Create column</button>
    </div>
  </div>
</template>

<script>
// services
import customColumnCreator from "../../../../../services/statistics/customColumnCreator";

// components
import ColumnSelection from "../common/ColumnSelection";
import Column from "../common/Column";

export default {
  components: {
    ColumnSelection,
    Column,
  },

  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      colName: "New column",

      firstColumn: 0,
      selectedColToChange: null,

      ruleSelection: false,
      ruleSelectionIndex: null,

      rules: [],

      operators: {
        plus: { code: "+", display: "+" },
        minus: { code: "-", display: "-" },
        div: { code: "/", display: "/" },
        mult: { code: "*", display: "x" },
        and: { code: "&&", display: "and" },
        or: { code: "||", display: "or" },
        sup: { code: ">", display: ">" },
        inf: { code: "<", display: "<" },
        equal: { code: "==", display: "equal" },
      },
    };
  },
  created() {},
  methods: {
    create() {
      if (this.columnOk) {
        try {
          let cuCol = customColumnCreator.customColumnCreation(
            this.data,
            this.colName,
            this.firstColumn,
            this.rules
          );
          this.$emit("create", cuCol);
        } catch (e) {
          console.error(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't create the new column",
          });
        }
      }
    },
    selectCol(colIndex) {
      if (this.selectedColToChange == 0) this.firstColumn = colIndex;
      else this.rules[this.selectedColToChange - 1].colIndex = colIndex;

      this.selectedColToChange = null;
    },
    addRule() {
      this.rules.push({
        colIndex: 0,
        operator:  this.operators.plus,
      });
      this.selectedColToChange = this.rules.length;
    },
    selectRule(operatorName) {
      this.rules[this.ruleSelectionIndex].operator = this.operators[operatorName];
      this.ruleSelection = false;
    },
  },
  computed: {
    colNameAvailable() {
      return this.data.labels.find((l) => l == this.colName) == undefined;
    },
    columnOk() {
      return (
        this.colNameAvailable &&
        this.colName.length > 0 &&
        this.colName.length < 30
      );
    },
  },
};
</script>

<style scoped>
#virtualColumnCreator {
  display: flex;
  flex-direction: column;
  height: 20vh;
  width: 70vw;
}
#content {
  display: flex;
  flex-direction: column;
}
#colList {
  padding: 10px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  flex: 1;

  overflow-y: auto;

  border: 1px dotted black;
  border-radius: 10px;
}

.rule {
  display: flex;
}
</style>