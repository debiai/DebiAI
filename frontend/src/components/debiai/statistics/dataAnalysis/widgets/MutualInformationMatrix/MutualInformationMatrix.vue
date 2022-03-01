<template>
  <div id="mutualInformation" class="dataVisualisationWidget">
    <!-- Axis selection Modal -->
    <modal v-if="axisSelection">
      <ColumnSelection
        title="Select the columns to compute"
        :data="data"
        :minimunSelection="2"
        :cancelAvailable="true"
        :colorSelection="true"
        :defaultSelected="selectedColumns.map((c) => c.index)"
        v-on:cancel="cancelAxiesSettings"
        v-on:validate="axiesSelect"
      />
    </modal>

    <!-- Controls -->
    <div id="axisControls" v-if="settings">
      <!-- Axis btns -->
      <div id="columnAxisSelection" class="dataGroup">
        <div class="data">
          <div class="name">Columns selection</div>
          <div class="value">
            <button @click="selectAxis">Select columns</button>
          </div>
        </div>
        <!-- Base -->
        <div class="data">
          <div class="name">Base</div>
          <div class="value">
            <button
              :class="selectedBase == 2 ? 'radioBtn selected' : 'radioBtn'"
              @click="selectedBase = 2"
            >
              2 (bits)
            </button>
            <button
              :class="selectedBase == 10 ? 'radioBtn selected' : 'radioBtn'"
              @click="selectedBase = 10"
            >
              10 (nats)
            </button>
          </div>
        </div>
        <!-- k -->
        <div class="data">
          <div class="name">Number of neighbors</div>
          <div class="value" id="neighborsInput">
            <input
              type="number"
              v-model="k"
              min="1"
              :max="selectedColumns.length"
            />
          </div>
        </div>
        <!-- normalise -->
        <div class="data">
          <div class="name">Normalise</div>
          <div class="value">
            <button
              :class="normaliseType == 'max' ? 'radioBtn selected' : 'radioBtn'"
              @click="normaliseType = 'max'"
            >
              max
            </button>
            <button
              :class="normaliseType == 'min' ? 'radioBtn selected' : 'radioBtn'"
              @click="normaliseType = 'min'"
            >
              min
            </button>
            <button
              :class="
                normaliseType == 'square root'
                  ? 'radioBtn selected'
                  : 'radioBtn'
              "
              @click="normaliseType = 'square root'"
            >
              square root
            </button>
            <button
              :class="
                normaliseType == 'mean' ? 'radioBtn selected' : 'radioBtn'
              "
              @click="normaliseType = 'mean'"
            >
              mean
            </button>
            <button
              :class="
                normaliseType == 'none' ? 'radioBtn selected' : 'radioBtn'
              "
              @click="normaliseType = 'none'"
            >
              none
            </button>
          </div>
        </div>
      </div>

      <!-- Selection beween continuous or discrete variable -->
      <div id="contDiscSelect" v-if="selectedColumns.length">
        Select if variable is considered discrete or continuous
        <div id="colList">
          <div class="col" v-for="(col, i) in selectedColumns" :key="col.index">
            <Column :column="col" colorSelection disabled />
            <div class="select dataGroup">
              <!-- Continuous btn -->
              <button
                :class="
                  'radioBtn' +
                  (selectedColumnsType[i] == 'c' ? ' selected' : '')
                "
                @click="$set(selectedColumnsType, i, 'c')"
              >
                Continuous
              </button>
              <!-- Discrete btn -->
              <button
                :class="
                  'radioBtn' +
                  (selectedColumnsType[i] == 'd' ? ' selected' : '')
                "
                @click="$set(selectedColumnsType, i, 'd')"
              >
                Discrete
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-if="selectedColumns.length > 1">
        <button @click="calculate" :disabled="loading">Calculate</button>
      </div>
    </div>

    <!-- Results display -->
    <div v-if="mutualInformation" class="dataGroup">
      <div class="data">
        <div class="name">MutualInformation</div>
        <div class="value">
          {{ mutualInformation }}
        </div>
      </div>
    </div>

    <div class="plot" :id="'matrix' + index"></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

// components
import ColumnSelection from "../../common/ColumnSelection";
import timer from "../../../../../../services/statistics/timer";
import Column from "../../common/Column";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      settings: true,
      axisSelection: false,
      loading: false,

      // Parameters
      k: 2,
      selectedBase: 2,
      normaliseType: "max",
      selectedColumns: [],
      selectedColumnsType: [],

      // Results
      mutualInformation: null,
      mutualInformationMatrix: null,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required : true },
    selectedData: { type: Array, required: true },
  },
  created() {
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawMatrix);
  },
  mounted() {
    this.domMatrixPlot = document.getElementById("matrix" + this.index);
  },
  methods: {
    // axies selection
    selectAxis() {
      this.axisSelection = true;
    },
    cancelAxiesSettings() {
      this.axisSelection = false;
    },
    axiesSelect(selectedColumns) {
      this.selectedColumnsType = [];
      this.selectedColumns = selectedColumns.map((colId) => {
        // Find col in data
        let dataCol = this.data.columns.find((col) => col.index == colId);

        // Set if continuous or discrete from the col type
        this.selectedColumnsType.push(
          dataCol.type == Number ? "c" : "d"
          // 'c' for continuous and 'd' for discrete
        );
        return dataCol;
      });

      this.axisSelection = false;
      // Set k boundaries
      if (this.k >= this.selectedColumns.length)
        this.k = this.selectedColumns.length - 1;
    },

    // Matrix and mutual information calculation
    calculate() {
      var t0 = performance.now();

      this.getContinuousAndHigherDimensionMutualInformation()
        .then((ret) => {
          this.mutualInformation = ret.higherDimensionMutualInformation;
          this.mutualInformationMatrix = ret.mutualInformation;
          this.drawMatrix();

          // Might change data description
          var data_log = (this.selectedColumns.length) + " columns";
          timer.logTime(
            t0, "MutualInformationMatrix",
            this.selectedData.length,
            this.$store.state.ProjectPage.projectId,
            data_log);
        })
        .catch((error) => {
          console.log(error);
          this.$parent.$emit("errorMessage", error.message);
        });
    },
    async getContinuousAndHigherDimensionMutualInformation() {
      // Creating data to send
      var list_continuous = [];
      var list_discrete = [];
      this.selectedColumns.forEach((c, i) => {
        let listToAdd = [];
        if (c.type == String)
          listToAdd = this.selectedData.map((i) => c.valuesIndex[i]);
        else
          listToAdd = this.selectedData.map((i) => c.values[i]);

        if (this.selectedColumnsType[i] == "c") list_continuous.push(listToAdd);
        else list_discrete.push(listToAdd);
      });

      // Set k boundaries
      if (this.k >= this.selectedColumns.length)
        this.k = this.selectedColumns.length - 1;

      this.loading = true;

      // Sending request
      var t0 = performance.now();

      return this.$backendDialog
        .continuousAndHigherDimensionMutualInformation(
          list_continuous,
          list_discrete,
          parseInt(this.k),
          this.selectedBase,
          this.normaliseType
        )
        .finally(() => {
          this.loading = false;
        })
        .then((data) => {
          // Might change data description
          timer.logTime(
            t0, "MutualInformationMatrix-Backend",
            this.selectedData.length,
            this.$store.state.ProjectPage.projectId);
          return data;
        });
    },

    drawMatrix() {
      var colorscale = [
        [0, "rgb(0,0,255)"],
        [0.5, "rgb(255,255,255)"],
        [1, "rgb(255,0,0)"],
      ];

      var data = [
        {
          z: this.mutualInformationMatrix,
          x: this.selectedColumns.map((col) => col.label),
          y: this.selectedColumns.map((col) => col.label),
          zmin: -1,
          zmax: 1,
          type: "heatmap",
          colorscale: colorscale,
          xgap: 5,
          ygap: 5,
          colorbar: {
            ticklen: 3,
          },
        },
      ];

      var layout = {
        zaxis: {
          range: [-1, 1],
        },
        margin: {
          l: 120,
          r: 10,
          b: 70,
          t: 10,
        },

        annotations: [],
      };

      for (let i = 0; i < this.mutualInformationMatrix.length; i++) {
        for (let j = 0; j < this.mutualInformationMatrix[i].length; j++) {
          let value = this.mutualInformationMatrix[i][j];
          layout.annotations.push({
            text: Math.round(value * 100) / 100,
            x: i,
            y: j,
            showarrow: false,
            font: {
              color: Math.abs(value) > 0.7 ? "white" : "black",
            },
          });
        }
      }

      Plotly.react(this.domMatrixPlot, data, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.$parent.selectedDataWarning = false;

    },
  },
  watch: {
    loading() {
      this.$parent.$emit("loading", this.loading);
    },
    selectedData() {
      this.$parent.selectedDataWarning = true;
    },
  },
};
</script>

<style scoped>
#mutualInformation {
  display: flex;
  flex-direction: column;
}
input {
  width: 50px;
}
#colList {
  max-height: 200px;
  overflow: auto;
}

.col {
  display: flex;
}
.select {
  align-items: center;
  justify-content: center;
  flex: 1;
}
</style>