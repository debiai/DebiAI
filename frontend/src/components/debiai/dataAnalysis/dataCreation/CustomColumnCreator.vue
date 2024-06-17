<template>
  <div id="virtualColumnCreator">
    <!-- Rule selection Modal -->
    <modal
      v-if="ruleSelection"
      @close="ruleSelection = false"
    >
      <h2 class="aligned spaced marged">
        Select an operation
        <button
          @click="ruleSelection = false"
          class="red"
        >
          Cancel
        </button>
      </h2>
      <button
        v-for="(operator, operatorName) in operators"
        :key="operatorName"
        @click="selectRule(operatorName)"
      >
        {{ operator.display }}
      </button>
    </modal>

    <!-- title -->
    <h2
      id="title"
      class="aligned spaced marged"
    >
      <div style="display: flex">
        Custom column creation
        <DocumentationBlock>
          Create a new column based on the analysis columns and some simple arithmetic operations.
        </DocumentationBlock>
      </div>
      <div>
        <button
          @click="rules = []"
          class="red"
        >
          Clear columns
        </button>
        <button
          @click="$emit('cancel')"
          class="red"
        >
          Cancel
        </button>
      </div>
    </h2>

    <!-- column name & rules -->
    <div id="content">
      <!-- new column name input -->
      <div class="dataGroup">
        <div class="data">
          <div class="name">Virtual column name</div>
          <div class="value">
            <input
              type="text"
              placeholder="New column"
              v-model="colName"
            />
          </div>
        </div>
        <div class="data">
          <button
            @click="create"
            :disabled="!columnOk"
          >
            Create the virtual column
          </button>
        </div>
      </div>

      <!-- Operations list -->
      <div id="colList">
        <ColumnSelectionButton
          :data="data"
          :validColumnsProperties="validColumnsProperties"
          :defaultColumnIndex="firstColumnIndex"
          title="Select a column"
          v-on:selected="selectFirstCol"
        />

        <div
          class="rule"
          v-for="(rule, ruleNb) in rules"
          :key="ruleNb"
        >
          <button
            @click="
              ruleSelection = true;
              ruleSelectionIndex = ruleNb;
            "
          >
            {{ rule.operator.display }}
          </button>

          <ColumnSelectionButton
            :data="data"
            :validColumnsProperties="validColumnsProperties"
            :defaultColumnIndex="rule.colIndex"
            title="Select a column"
            openOnCreation
            canBeRemoved
            v-on:selected="(index) => setColumnForRule(index, ruleNb)"
            v-on:removed="removeRule(ruleNb)"
          />
        </div>

        <button
          @click="addRule"
          v-if="firstColumnIndex !== null"
        >
          Add column
        </button>
      </div>

      <!-- Display the warning messages -->
      <transition name="fade">
        <div
          v-if="!colNameAvailable"
          class="warning"
        >
          The column name already exists
        </div>
        <div
          v-else-if="!columnOk"
          class="warning"
        >
          The column name must be between 1 and 30 characters
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
// services
import customColumnCreator from "@/services/statistics/customColumnCreator";

// components
import ColumnSelectionButton from "../common/ColumnSelectionButton";

export default {
  components: {
    ColumnSelectionButton,
  },

  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      colName: "New column",

      firstColumnIndex: null,

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

      validColumnsProperties: {
        types: ["Class", "Num", "Bool"],
      },
    };
  },
  methods: {
    selectFirstCol(colIndex) {
      this.firstColumnIndex = colIndex;
    },
    setColumnForRule(colIndex, ruleNb) {
      this.rules[ruleNb].colIndex = colIndex;
    },
    addRule() {
      this.rules.push({
        colIndex: null,
        operator: this.operators.plus,
      });
    },
    selectRule(operatorName) {
      this.rules[this.ruleSelectionIndex].operator = this.operators[operatorName];
      this.ruleSelection = false;
    },
    removeRule(ruleNb) {
      this.rules = this.rules.filter((r, i) => i != ruleNb);
    },
    create() {
      // Create the new column
      if (this.columnOk) {
        try {
          // Remove all the columns that aren't selected
          this.rules = this.rules.filter((r) => this.data.columnExists(r.colIndex));

          const customColumn = customColumnCreator.customColumnCreation(
            this.data,
            this.colName,
            this.firstColumnIndex,
            this.rules
          );

          this.data.addColumn(customColumn);
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Column created successfully",
          });
        } catch (e) {
          console.error(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "Couldn't create the new column",
          });
        }
      }
    },
  },
  computed: {
    colNameAvailable() {
      return !this.data.columns.some((col) => col.label === this.colName);
    },
    columnOk() {
      return this.colNameAvailable && this.colName.length > 0 && this.colName.length < 30;
    },
  },
};
</script>

<style scoped>
#virtualColumnCreator {
  display: flex;
  flex-direction: column;
  height: 40vh;
  width: 70vw;
}
#content {
  display: flex;
  flex-direction: column;
}
#colList {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex-direction: column;
  flex: 1;

  border: 1px solid black;
  padding: 3px;
  margin: 3px;
  background-color: var(--greyLight);
}

.rule {
  display: flex;
  align-items: center;
}

.warning {
  color: var(--danger);
  font-weight: bold;
  border: 1px solid var(--danger);
  border-radius: 5px;
  padding: 5px;
  margin: 5px;
}
</style>
