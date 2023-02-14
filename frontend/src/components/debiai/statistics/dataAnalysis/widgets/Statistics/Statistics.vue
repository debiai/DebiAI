<template>
  <div
    :id="'SimpleStatistics' + index"
    class="dataVisualisationWidget"
  >
    <!-- Column selection Modal -->
    <modal
      v-if="columnSelection"
      @close="columnSelection = false"
    >
      <ColumnSelection
        title="Select a column"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        :defaultSelected="[selectedColumn.index]"
        v-on:cancel="columnSelection = false"
        v-on:colSelect="selectCol"
      />
    </modal>

    <div id="columnStat">
      <!-- Column & settings -->
      <div style="display: flex">
        <Column
          :column="selectedColumn"
          :colorSelection="true"
          v-on:selected="columnSelection = true"
        />
        <!-- abs value option -->
        <div
          class="dataGroup"
          style="flex: 1"
          v-if="absolueOption"
        >
          <div
            class="data"
            style="width: 100%"
          >
            <span class="name"> Absolute value </span>
            <span
              class="value"
              style="width: 100%"
            >
              <input
                type="checkbox"
                :id="'absolute' + index"
                class="customCbx"
                v-model="absolue"
                style="display: none"
              />
              <label
                :for="'absolute' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </span>
          </div>
        </div>
      </div>

      <!-- Column statistics -->
      <table id="columns">
        <thead>
          <tr>
            <th v-if="selectedColumn.type == String">Top</th>
            <th v-if="selectedColumn.type == String">Frequency</th>
            <th v-if="selectedColumn.type !== String">Min</th>
            <th v-if="selectedColumn.type !== String">Max</th>
            <th v-if="selectedColumn.type !== String">Average</th>
            <th v-if="selectedColumn.type !== String">Std</th>
            <th v-if="selectedColumn.type !== String">Variance</th>
          </tr>
        </thead>
        <tbody>
          <tr class="colorVal data">
            <td v-if="selectedColumn.type == String">{{ top }}</td>
            <td v-if="selectedColumn.type == String">
              {{ frequency }}
              <span
                v-if="nbSelectedSamplesAtUpdate"
                style="padding-left: 7px; opacity: 0.7"
              >
                ({{ Math.round((frequency / nbSelectedSamplesAtUpdate) * 100) }}%)
              </span>
            </td>
            <td v-if="selectedColumn.type !== String">{{ min }}</td>
            <td v-if="selectedColumn.type !== String">{{ max }}</td>
            <td v-if="selectedColumn.type !== String">{{ average }}</td>
            <td v-if="selectedColumn.type !== String">{{ std }}</td>
            <td v-if="selectedColumn.type !== String">{{ variance }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Statistics for each color -->

    <div v-if="toMuchUniqueValues">To much unique values in the selected colored column</div>
    <div
      id="groupStat"
      v-else-if="statByColor !== null"
    >
      <!-- Title -->
      <b>
        {{ selectedColumn.label }}
      </b>
      statistics for each
      <b>
        {{ colColorName }}
      </b>

      <!-- Column list -->
      <table id="columns">
        <thead>
          <tr v-if="statByColor && statByColor.length">
            <th>{{ colColorName }}</th>
            <th v-if="selectedColumn.type == String">Top</th>
            <th v-if="selectedColumn.type == String">Frequency</th>
            <th v-if="selectedColumn.type !== String">Min</th>
            <th v-if="selectedColumn.type !== String">Max</th>
            <th v-if="selectedColumn.type !== String">Average</th>
            <th v-if="selectedColumn.type !== String">Std</th>
            <th v-if="selectedColumn.type !== String">Variance</th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="colorVal data"
            v-for="colVal in statByColor"
            :key="colVal.colValue"
          >
            <td class="colName">
              {{ colVal.colValue }}
              <!-- Repartition -->
              <div class="repartion">
                <span>
                  {{ colVal.repartition }}
                </span>

                <span
                  v-if="nbSelectedSamplesAtUpdate"
                  style="padding-left: 7px; opacity: 0.7"
                >
                  ({{ Math.round((colVal.repartition / nbSelectedSamplesAtUpdate) * 100) }}%)
                </span>
              </div>
            </td>
            <!-- Min -->
            <td v-if="colVal.min !== undefined">
              {{ colVal.min }}
            </td>
            <!-- Max -->
            <td v-if="colVal.max !== undefined">
              {{ colVal.max }}
            </td>
            <!-- Average -->
            <td v-if="colVal.average !== undefined">
              {{ colVal.average }}
            </td>
            <!-- Std-->
            <td v-if="colVal.std !== undefined">
              {{ colVal.std }}
            </td>
            <!-- Variance-->
            <td v-if="colVal.variance !== undefined">
              {{ colVal.variance }}
            </td>
            <!-- top-->
            <td v-if="colVal.top !== undefined">
              {{ colVal.top }}
            </td>
            <!-- frequency-->
            <td v-if="colVal.frequency !== undefined">
              {{ colVal.frequency }}
              <span v-if="colVal.repartition">
                ({{ Math.round((colVal.frequency / colVal.repartition) * 100) }}%)
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// Components
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";

// Services
import dataOperations from "../../../../../../services/statistics/dataOperations";
import { std, variance } from "mathjs";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  data() {
    return {
      // Settings
      selectedColumn: null,
      columnSelection: false,
      absolueOption: false,
      absolue: false,

      // Statistics
      nbSelectedSamplesAtUpdate: null,

      // Class
      top: null,
      frequency: null,

      // Float
      average: null,
      min: null,
      max: null,
      std: null,

      // Per color
      statByColor: null,

      // Other
      toMuchUniqueValues: false,
      colColorName: null,
      colColorDisplayed: null,
    };
  },
  created() {
    // Select the 3 firsts columns
    if (this.data.nbColumns > 0) this.selectCol(0);
  },
  mounted() {
    this.$parent.$on("redraw", this.updateStatistics);
  },
  methods: {
    selectCol(index) {
      this.selectedColumn = this.data.columns.find((c) => c.index === index);
      this.columnSelection = false;
      this.absolueOption = this.selectedColumn.type !== String && this.selectedColumn.min < 0;
      this.absolue = false;

      this.updateStatistics();
    },
    updateStatistics() {
      let values;
      let valuesText;
      if (this.selectedColumn.type === String) {
        values = this.selectedData.map((sId) => this.selectedColumn.valuesIndex[sId]);
        valuesText = this.selectedData.map((sId) => this.selectedColumn.values[sId]);
      } else {
        values = this.selectedData.map((sId) => this.selectedColumn.values[sId]);
        if (this.absolue) values = values.map((v) => Math.abs(v));
      }
      this.nbSelectedSamplesAtUpdate = values.length;

      // Average or frequency
      if (this.selectedColumn.type === String) {
        let { top, frequency } = dataOperations.mode(values);
        this.top = valuesText[top];
        this.frequency = frequency;
        this.average = null;
      } else {
        this.average = dataOperations.humanize(dataOperations.mean(values));
        this.frequency = null;
        this.top = null;
      }

      // Min
      this.min = null;
      if (this.selectedColumn.type !== String)
        if (!this.absolue) this.min = dataOperations.humanize(this.selectedColumn.min);
        else this.min = dataOperations.humanize(dataOperations.getMin(values));

      // Max
      this.max = null;
      if (this.selectedColumn.type !== String)
        if (!this.absolue) this.max = dataOperations.humanize(this.selectedColumn.max);
        else this.max = dataOperations.humanize(dataOperations.getMax(values));

      // Std & variance
      this.std = null;
      this.variance = null;
      if (this.selectedColumn.type !== String && values.length > 0) {
        this.std = dataOperations.humanize(std(values));
        this.variance = dataOperations.humanize(variance(values));
      }

      // Average by color
      if (this.coloredColumnIndex != null) {
        let colColor = this.data.columns[this.coloredColumnIndex];
        if (colColor.nbOccu <= 100) {
          this.toMuchUniqueValues = false;
          let selectedColors;
          if (colColor.type === String)
            selectedColors = this.selectedData.map((i) => colColor.valuesIndex[i]);
          else selectedColors = this.selectedData.map((i) => colColor.values[i]);

          let groupedValues = dataOperations.groupBy(
            selectedColors,
            colColor.type === String ? colColor.valuesIndexUniques : colColor.uniques
          );

          this.statByColor = groupedValues.map((sampleIds, i) => {
            let gpValues = sampleIds.map((sId) => values[sId]);

            // Stats
            //  Numbers
            let average;
            let colStd;
            let colVariance;
            let min;
            let max;
            //  Class
            let top;
            let frequency;

            if (gpValues.length) {
              if (this.selectedColumn.type === String) {
                let mode = dataOperations.mode(gpValues);
                top = this.selectedColumn.uniques[mode.top];
                frequency = mode.frequency;
              } else {
                average = dataOperations.humanize(dataOperations.mean(gpValues));

                // Std & variance
                colStd = dataOperations.humanize(std(gpValues));
                colVariance = dataOperations.humanize(variance(gpValues));
                min = dataOperations.humanize(dataOperations.getMin(gpValues));
                max = dataOperations.humanize(dataOperations.getMax(gpValues));
              }
            }
            return {
              colValue: colColor.uniques[i],
              // Numbers
              average,
              min,
              max,
              top,
              frequency,
              std: colStd,
              variance: colVariance,
              repartition: gpValues.length,
            };
          });

          this.colColorName = colColor.label;
        } else this.toMuchUniqueValues = true;

        this.colColorDisplayed = this.coloredColumnIndex;
      } else {
        this.statByColor = null;
        this.colColorDisplayed = null;
      }

      this.$parent.selectedDataWarning = false;
      this.$parent.colorWarning = false;
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.SatisticalAnasysis.coloredColumnIndex;
    },
  },
  watch: {
    selectedData() {
      this.$parent.selectedDataWarning = true;
    },
    coloredColumnIndex(n) {
      this.$parent.colorWarning = this.colColorDisplayed !== n;
    },
    absolue() {
      this.updateStatistics();
    },
  },
};
</script>

<style scoped>
.dataVisualisationWidget {
  display: flex;
  flex-direction: column;
}

#columnStat {
  display: flex;
  flex-direction: column;
}
#columnStat #top {
  display: flex;
}

#columnStat .data {
  flex: 1;
}
#columnStat .data .value {
  flex: 1;
}
#groupStat {
  flex: 1;
  overflow: auto;
  text-align: left;
  padding: 10px;
}
#columns {
  width: 100%;
  overflow-wrap: break-word;
  border-collapse: collapse;
  text-align: left;
  padding-bottom: 20px;
}
#columns thead th {
  padding: 10px 0 10px 10px;
  background-color: var(--primary);
  color: white;
}
#columns .colName {
  background-color: var(--primaryDark);
  display: flex;
  justify-content: space-between;
  color: white;
}
#columns td {
  border-bottom: 1px solid #d8d8d8;
  padding: 3px 0 3px 10px;
}
</style>
