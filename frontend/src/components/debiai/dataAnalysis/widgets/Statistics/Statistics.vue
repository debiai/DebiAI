<template>
  <div
    :id="'SimpleStatistics' + index"
    class="dataVisualizationWidget"
  >
    <!-- Column & settings -->
    <div
      id="settings"
      class="dataGroup gapped"
      style="align-items: center; justify-content: space-evenly"
      v-if="settings"
    >
      <div class="data">
        <div class="name">Select the column to display statistics</div>
        <div class="value">
          <ColumnSelectionButton
            :data="data"
            :validColumnsProperties="validColumnsProperties"
            :defaultColumnIndex="selectedColumn ? selectedColumn.index : null"
            title="Select a column"
            v-on:selected="selectCol"
          />
        </div>
        <!-- abs value option -->
      </div>
      <div
        class="data"
        v-if="absoluteOption"
      >
        <span class="name"> Absolute value </span>
        <span class="value">
          <input
            type="checkbox"
            :id="'absolute' + index"
            class="customCbx"
            v-model="absolute"
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

    <div
      id="columnStat"
      v-if="selectedColumn !== null"
    >
      <!-- Title -->
      <span>
        <b>
          {{ selectedColumn.label }}
        </b>
        statistics
      </span>

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
            <th v-if="nbNullValues">Missing values</th>
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
            <td v-if="nbNullValues">
              {{ nbNullValues }} ({{
                Math.round((nbNullValues / nbSelectedSamplesAtUpdate) * 100)
              }}%)
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Statistics for each color -->

    <div v-if="toMuchUniqueValues">To much unique values in the selected colored column</div>
    <div
      id="groupStat"
      v-else-if="statByColor !== null && selectedColumn !== null"
    >
      <!-- Title 2 -->
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
            <th v-if="nbNullValues">Missing values</th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="colorVal data"
            v-for="colVal in statByColor"
            :key="colVal.colValue"
          >
            <td class="colName">
              <div v-if="colVal.colValue !== null">
                {{ colVal.colValue }}
              </div>
              <div
                v-else
                style="opacity: 0.7"
              >
                Missing value
              </div>

              <!-- Repartition -->
              <div>
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
              <div v-if="colVal.top !== null">
                {{ colVal.top }}
              </div>
              <div
                v-else
                style="opacity: 0.7"
              >
                Missing value
              </div>
            </td>
            <!-- frequency-->
            <td v-if="colVal.frequency !== undefined">
              {{ colVal.frequency }}
              <span v-if="colVal.repartition">
                ({{ Math.round((colVal.frequency / colVal.repartition) * 100) }}%)
              </span>
            </td>
            <!-- Null values -->
            <td v-if="nbNullValues">
              {{ colVal.nbNullValues }} ({{
                Math.round((colVal.nbNullValues / colVal.repartition) * 100)
              }}%)
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// Components
import ColumnSelectionButton from "../../common/ColumnSelectionButton";

// Services
import dataOperations from "@/services/statistics/dataOperations";
import { std, variance } from "mathjs";

export default {
  components: {
    ColumnSelectionButton,
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
  },
  data() {
    return {
      // Settings
      settings: true,
      selectedColumn: null,
      absoluteOption: false,
      absolute: false,

      // Statistics
      nbSelectedSamplesAtUpdate: null,
      nbNullValues: null,

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

      validColumnsProperties: {
        types: ["Num", "Class", "Bool"],
      },
    };
  },
  created() {
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });
  },
  mounted() {
    this.$parent.$on("redraw", this.updateStatistics);
  },
  methods: {
    selectCol(index) {
      this.selectedColumn = this.data.getColumn(index);
      this.absoluteOption = this.selectedColumn.type !== String && this.selectedColumn.min < 0;
      this.absolute = false;

      this.updateStatistics();
    },
    updateStatistics() {
      let values;
      let valuesOriginal; // With null values
      let valuesText;
      this.nbNullValues = 0;
      if (this.selectedColumn.type === String) {
        values = this.data.selectedData.map((sId) => this.selectedColumn.valuesIndex[sId]);
        valuesOriginal = values;
        valuesText = this.data.selectedData.map((sId) => this.selectedColumn.values[sId]);
        this.nbNullValues = valuesText.filter((v) => v === null).length;
      } else {
        valuesOriginal = this.data.selectedData.map((sId) => this.selectedColumn.values[sId]);
        values = valuesOriginal.filter((v) => v !== null);
        if (this.absolute) values = values.map((v) => Math.abs(v));
        this.nbNullValues = this.data.selectedData.length - values.length;
      }
      this.nbSelectedSamplesAtUpdate = this.data.selectedData.length;

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
        this.min = dataOperations.humanize(dataOperations.getMin(values));

      // Max
      this.max = null;
      if (this.selectedColumn.type !== String)
        this.max = dataOperations.humanize(dataOperations.getMax(values));

      // Std & variance
      this.std = null;
      this.variance = null;
      if (this.selectedColumn.type !== String && values.length > 0) {
        this.std = dataOperations.humanize(std(values));
        this.variance = dataOperations.humanize(variance(values));
      }

      // Average by color
      if (this.data.columnExists(this.coloredColumnIndex)) {
        let colColor = this.data.getColumn(this.coloredColumnIndex);
        if (colColor.nbOccurrence <= 100) {
          this.toMuchUniqueValues = false;
          let selectedColors;
          if (colColor.type === String)
            selectedColors = this.data.selectedData.map((i) => colColor.valuesIndex[i]);
          else selectedColors = this.data.selectedData.map((i) => colColor.values[i]);

          let groupedValues = dataOperations.groupBy(
            selectedColors,
            colColor.type === String ? colColor.valuesIndexUniques : colColor.uniques
          );

          this.statByColor = groupedValues.map((sampleIds, i) => {
            const gpValues = sampleIds.map((sId) => valuesOriginal[sId]);
            const gpValuesNonNull = gpValues.filter((v) => v !== null);

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

            if (gpValuesNonNull.length) {
              if (this.selectedColumn.type === String) {
                let mode = dataOperations.mode(gpValuesNonNull);
                top = this.selectedColumn.uniques[mode.top];
                frequency = mode.frequency;
              } else {
                average = dataOperations.humanize(dataOperations.mean(gpValuesNonNull));

                // Std & variance
                colStd = dataOperations.humanize(std(gpValuesNonNull));
                colVariance = dataOperations.humanize(variance(gpValuesNonNull));
                min = dataOperations.humanize(dataOperations.getMin(gpValuesNonNull));
                max = dataOperations.humanize(dataOperations.getMax(gpValuesNonNull));
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
              nbNullValues: gpValues.length - gpValuesNonNull.length,
            };
          });

          this.colColorName = colColor.label;
        } else this.toMuchUniqueValues = true;

        this.colColorDisplayed = this.coloredColumnIndex;
      } else {
        this.statByColor = null;
        this.colColorDisplayed = null;
      }

      this.$parent.$emit("drawn");
      this.$parent.colorWarning = false;
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    selectedDataUpdate() {
      this.$parent.selectedDataWarning = true;
    },
    coloredColumnIndex(n) {
      this.$parent.colorWarning = this.colColorDisplayed !== n;
    },
    absolute() {
      this.updateStatistics();
    },
  },
};
</script>

<style scoped>
#columnStat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px;
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
  background-color: var(--grey);
}
#columns .colName {
  background-color: var(--greyDark);
  display: flex;
  justify-content: space-between;
  font-weight: bold;
}
#columns td {
  border-bottom: 1px solid #d8d8d8;
  padding: 3px 0 3px 10px;
}
</style>
