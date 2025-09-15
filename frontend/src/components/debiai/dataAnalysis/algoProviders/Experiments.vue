<template>
  <div id="experiments">
    <!-- column creation modal -->
    <modal
      v-if="columnCreationModal"
      @close="columnCreationModal = false"
      :errorMessages="[
        columnName === '' ? 'The column name is empty' : '',
        columnNameAvailable ? '' : 'The column name already used.',
        selectedOutputNeedsDefault && !defaultValueAcceptable
          ? 'The default value is missing.'
          : '',
      ]"
    >
      <form
        id="columnCreationModal"
        v-on:submit.prevent
      >
        <h3 class="spaced aligned">
          New column
          <button
            @click="columnCreationModal = false"
            class="red"
          >
            Cancel
          </button>
        </h3>
        <div
          class="dataGroup"
          style="flex-direction: column; gap: 10px"
        >
          <div class="data">
            <span class="name"> Column name </span>
            <span class="value">
              <input
                type="text"
                v-model="columnName"
                style="flex: 2"
              />
            </span>
          </div>
          <div
            class="data"
            v-if="selectedOutputNeedsDefault"
          >
            <span class="name">
              Default value

              <documentation-block>
                The experiment results will be mapped
                <br />to the data that where selected <br />when the experiment was created.
                <br />
                <br />
                Because only a subset of the data was used,
                <br />you need to specify a default value <br />for the other data.
              </documentation-block>
            </span>
            <span class="value">
              <input
                type="text"
                v-model="defaultValue"
                style="flex: 2"
              />
            </span>
          </div>
        </div>
        <button
          type="submit"
          @click="createColumn"
          :disabled="
            columnName === '' ||
            !columnNameAvailable ||
            (selectedOutputNeedsDefault && !defaultValueAcceptable)
          "
        >
          <!-- :disabled="!tagNameOk || !tagValueOk" -->
          Create the column
        </button>
      </form>
    </modal>

    <!-- Info -->
    <div
      id="info"
      class="aligned spaced"
    >
      <div
        id="title"
        :title="'Id: ' + algorithm.id"
      >
        <span>Experiments of the algorithm:</span>
        <inline-svg
          :src="require('@/assets/svg/algorithm.svg')"
          width="20"
          height="20"
          style="margin: 0 5px 0 15px"
        />
        <span
          id="algoName"
          class="tag"
        >
          {{
            algorithm.name !== null && algorithm.name !== undefined ? algorithm.name : algorithm.id
          }}
        </span>
        <span style="padding: 0 10px"> from </span>
        <span class="tag">{{ algoProvider.name }}</span>
      </div>

      <button
        class="red"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </div>
    <div id="description">
      {{ algorithm.description }}
    </div>

    <!-- Experiments -->
    <div id="content">
      <transition-group name="fade">
        <div
          v-for="experiment in experiments"
          :key="experiment.id"
          class="experiment"
        >
          <div class="top">
            <h4 class="experiment-title">Experiment {{ experiment.nb }}</h4>

            <div class="controls">
              <button
                v-if="experiment.inputs.length > 0"
                class="blue"
                @click="showInputs(experiment)"
              >
                Inputs
              </button>

              <!-- inputs modal -->
              <modal
                v-if="inputsModal"
                @close="inputsModal = false"
              >
                <span v-if="experiment.selectedData">
                  On {{ experiment.selectedData.length }} selected data.
                </span>
                <h3>Experiment {{ experiment.nb }} inputs:</h3>
                <div class="inputs">
                  <div
                    class="input"
                    v-for="input in experiment.inputs"
                    :key="input.name"
                  >
                    <div class="name">{{ input.name }}:</div>
                    <div
                      class="value"
                      v-if="input.columnLabel"
                    >
                      {{ input.columnLabel }}
                    </div>
                    <div
                      class="value"
                      v-else-if="Array.isArray(input.value)"
                    >
                      {{ input.value.slice(0, 10) }}
                      <span v-if="input.value.length > 10">...</span>
                    </div>
                    <div
                      class="value"
                      v-else
                    >
                      {{ input.value }}
                    </div>
                  </div>
                </div>
                <button
                  class="red"
                  @click="inputsModal = false"
                >
                  Close
                </button>
              </modal>
              <button
                class="green"
                @click="exportJson(experiment)"
              >
                Json
              </button>
              <button
                class="red"
                @click="deleteExperiment(experiment)"
              >
                Delete
              </button>
            </div>
          </div>
          <table class="results">
            <thead>
              <tr>
                <th>Algo output</th>
                <th>Experiment output</th>
                <th>Add to the analysis as a column</th>
              </tr>
            </thead>
            <tbody>
              <tr
                class="result"
                v-for="result in experiment.results"
                :key="result.name"
              >
                <!-- Display Outputs -->
                <td class="name">{{ result.name }}</td>
                <td
                  class="value"
                  v-if="
                    Array.isArray(result.value) &&
                    result.value.length &&
                    typeof result.value[0] === 'object' &&
                    result.value[0] !== null
                  "
                >
                  <DataTable :data="result.value" />
                </td>
                <td
                  class="value"
                  v-else-if="Array.isArray(result.value)"
                >
                  {{ result.value.length }} elements {{ result.value.slice(0, 5) }}...
                </td>
                <td
                  class="value"
                  v-else
                >
                  {{ result.value }}
                </td>

                <td>
                  <button
                    v-if="canCreateColumnFromOutput(experiment, result) === true"
                    @click="createColumnButton(experiment, result)"
                  >
                    Create column
                  </button>
                  <div
                    v-else
                    style="color: var(--fontColorLight)"
                  >
                    {{ canCreateColumnFromOutput(experiment, result) }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
import DataTable from "@/components/debiai/dataAnalysis/common/DataTable.vue";

export default {
  name: "Experiments",
  components: {
    DataTable,
  },
  props: {
    algorithm: { type: Object, required: true },
    algoProvider: { type: Object, required: true },
    data: { type: Object, required: true },
  },
  data() {
    return {
      experiments: [],
      columnName: "",
      defaultValue: 0,
      columnCreationModal: false,
      selectedOutput: null,
      selectedOutputNeedsDefault: false,
      selectedExperiment: null,
      inputsModal: false,
    };
  },
  mounted() {
    this.getExperiments();
  },
  methods: {
    getExperiments() {
      this.experiments = this.$store.getters.getAlgoExperiments(
        this.algoProvider.name,
        this.algorithm.id
      );

      // Sort the experiments by nb
      this.experiments.sort((a, b) => a.nb - b.nb);
    },
    showInputs(experiment) {
      this.inputsModal = true;
    },
    deleteExperiment(experiment) {
      this.$store.commit("deleteExperiment", experiment.id);
      this.getExperiments();
    },
    exportJson(experiment) {
      const experimentCopy = JSON.parse(JSON.stringify(experiment));
      // Remove the id
      delete experimentCopy.id;
      // Remove the nb
      delete experimentCopy.nb;
      // Remove the selectedData
      delete experimentCopy.selectedData;

      // Add the algorithm
      experimentCopy.algorithm = this.algorithm;
      // Add the algoProvider
      experimentCopy.algoProvider = JSON.parse(JSON.stringify(this.algoProvider));
      delete experimentCopy.algoProvider.algorithms;
      delete experimentCopy.algoProvider.status;

      // Create the filename
      let name =
        this.algorithm.name !== null && this.algorithm.name !== undefined
          ? this.algorithm.name
          : this.algorithm.id;

      name += "_experiment_" + experiment.nb;

      const json = JSON.stringify(experimentCopy, null, 2);
      const blob = new Blob([json], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = name + ".json";
      link.click();
    },
    canCreateColumnFromOutput(experiment, output) {
      // We can only create a column from an array
      if (!Array.isArray(output.value)) return "Can only create a column from an array";

      // Case one, length of the array is the same as the number of data
      if (output.value.length === this.data.nbLines) return true;

      // Case two, length of the array is the same as the number of data
      // that were selected when the algorithm was run
      if (experiment.selectedData && output.value.length === experiment.selectedData.length)
        return true;

      return "The length of the array is not the same as the number of data in the analysis \n\
      nor the number of data that were selected when the algorithm was run";
    },
    createColumnButton(experiment, output) {
      this.selectedOutput = output;
      this.selectedExperiment = experiment;
      this.columnName = output.name;
      this.columnCreationModal = true;
      if (experiment.selectedData && output.value.length === experiment.selectedData.length)
        this.selectedOutputNeedsDefault = true;
      else this.selectedOutputNeedsDefault = false;
    },
    createColumn() {
      const output = this.selectedOutput;
      if (output === null) return;

      let values;
      if (
        this.selectedExperiment.selectedData &&
        output.value.length === this.selectedExperiment.selectedData.length
      ) {
        // Create an array of the default value
        values = Array(this.data.nbLines).fill(this.defaultValue);
        // Replace the default value by the output value
        for (let i = 0; i < this.selectedExperiment.selectedData.length; i++)
          values[this.selectedExperiment.selectedData[i]] = output.value[i];
      } else {
        values = output.value;
      }

      // Create column
      this.data.addColumn({
        label: this.columnName,
        values: values,
        category: "Algorithm output",
      });

      this.$store.commit("sendMessage", {
        title: "success",
        msg: "Column added successfully",
      });

      this.defaultValue = 0;
      this.columnCreationModal = false;
    },
  },
  computed: {
    columnNameAvailable() {
      return this.data.columns.filter((col) => col.label === this.columnName).length === 0;
    },
    defaultValueAcceptable() {
      return (
        this.defaultValue !== null && this.defaultValue !== undefined && this.defaultValue !== ""
      );
    },
  },
};
</script>

<style lang="scss" scoped>
#experiments {
  width: 75vw;
  height: 75vh;
  display: flex;
  flex-direction: column;
}

#info {
  font-size: 1.3em;

  #title {
    display: flex;
    align-items: center;
  }
}

#description {
  margin: 10px 0 10px 0;
  text-align: left;
  color: var(--fontColorLight);
}

#content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
  flex: 1;

  .experiment {
    display: flex;
    flex-direction: column;
    border-radius: 3px;
    margin-bottom: 10px;
    // background-color: var(--greyLight);
    border: var(--greyDark) solid 1px;
    padding: 15px;

    .experiment-title {
      display: flex;
      align-items: center;
      margin: 0;
      margin-bottom: 5px;
    }

    .top {
      padding-bottom: 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .inputs {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin: 15px 0;

      .input {
        display: flex;
        gap: 12px;
        padding: 8px 12px;
        background: var(--greyLight);
        border-radius: 4px;

        .name {
          text-align: right;
          font-weight: 500;
          min-width: 120px;
          color: var(--fontColor);
        }

        .value {
          text-align: left;
          flex: 1;
          color: var(--fontColorLight);
          word-break: break-word;
        }
      }
    }

    .results {
      width: 100%;
      border-collapse: collapse;
      text-align: left;

      th {
        color: var(--fontColorLight);
        font-weight: bold;
        border-bottom: solid 1px var(--greyDark);
        padding: 5px;
      }

      td {
        padding: 10px 5px;
        vertical-align: top;
      }

      .name {
        font-weight: bold;
      }

      .value {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
  }
}

#columnCreationModal {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#columnCreationModal .name {
  min-width: 130px;
}
</style>
