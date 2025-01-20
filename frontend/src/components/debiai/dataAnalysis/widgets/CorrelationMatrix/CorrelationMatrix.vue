<template>
  <div
    id="CorrelationMatrix"
    class="dataVisualizationWidget"
  >
    <!-- Axis selection Modal -->
    <modal
      v-if="axisSelection"
      @close="cancelAxisSettings"
    >
      <ColumnSelection
        title="Select the columns to compute"
        :data="data"
        :minimumSelection="2"
        :cancelAvailable="true"
        :colorSelection="true"
        :defaultSelected="selectedColumns.map((c) => c.index)"
        :validColumnsProperties="validColumnsProperties"
        v-on:cancel="cancelAxisSettings"
        v-on:validate="AxisSelect"
      />
    </modal>

    <!-- Controls -->
    <div
      id="axisControls"
      v-if="settings"
    >
      <!-- Axis buttons -->
      <div
        id="columnAxisSelection"
        class="dataGroup"
      >
        <div class="data">
          <div class="name">Columns selection :</div>
          <div class="value">
            <button @click="selectAxis">Select columns</button>
          </div>
        </div>
        <div class="data">
          <div class="name">Matrix type</div>
          <div class="value">
            <button
              :class="selectedMatrixType == 'pearson' ? 'radioBtn selected' : 'radioBtn'"
              @click="
                selectedMatrixType = 'pearson';
                calculate();
              "
            >
              Pearson
            </button>
            <button
              :class="selectedMatrixType == 'spearman' ? 'radioBtn selected' : 'radioBtn'"
              @click="
                selectedMatrixType = 'spearman';
                calculate();
              "
            >
              Spearman
            </button>
          </div>
        </div>
      </div>
    </div>
    <transition name="fade">
      <div
        v-if="error"
        class="error"
      >
        Error while calculating matrix
      </div>
    </transition>
    <!-- Plot -->
    <div
      class="plot"
      :id="'matrix' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";

// components
import ColumnSelection from "../../common/ColumnSelection";
// import Column from "../../common/Column";

export default {
  components: {
    ColumnSelection,
    // Column,
  },
  data() {
    return {
      selectedColumns: [],

      // Settings
      settings: true,
      matrixDrawn: false,
      axisSelection: false,
      selectedMatrixType: "pearson",
      error: false,
      loading: false,

      validColumnsProperties: {
        types: ["Class", "Num", "Bool"],
      },
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
  },
  created() {
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.calculate);
  },
  mounted() {
    this.divHeatMapPlot = document.getElementById("matrix" + this.index);
  },
  methods: {
    // axis selection
    selectAxis() {
      this.axisSelection = true;
    },
    cancelAxisSettings() {
      this.axisSelection = false;
    },
    AxisSelect(selectedColumns) {
      this.selectedColumns = selectedColumns
        .map((colId) => this.data.getColumn(colId))
        .filter((c) => c.nbOccurrence > 1);

      this.axisSelection = false;
      this.matrixDrawn = false;

      this.calculate();
    },
    async calculate() {
      this.clearMatrix();
      this.loading = true;
      // Creating data to send
      const columnsData = [];
      this.selectedColumns.forEach((c) => {
        if (!c) return;
        if (c.type == String) columnsData.push(this.data.selectedData.map((i) => c.valuesIndex[i]));
        else columnsData.push(this.data.selectedData.map((i) => c.values[i]));
      });

      // Calculating matrix
      if (this.selectedMatrixType == "spearman") {
        return this.$services.spearmanCorrelationMatrix(
          columnsData,
          this.updateMatrix,
          this.calculationEnd
        );
      } else {
        return this.$services.pearsonCorrelationMatrix(
          columnsData,
          this.updateMatrix,
          this.calculationEnd
        );
      }
    },
    calculationEnd() {
      this.loading = false;
    },
    clearMatrix() {
      this.matrixDrawn = false;
      this.loading = false;
      this.error = false;
      Plotly.purge(this.divHeatMapPlot);
    },
    updateMatrix(matrix) {
      const colorscale = [
        [0, "rgb(0,0,255)"],
        [0.5, "rgb(255,255,255)"],
        [1, "rgb(255,0,0)"],
      ];
      const data = [
        {
          z: matrix,
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

      const layout = {
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

      for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix[i].length; j++) {
          let value = matrix[i][j];
          layout.annotations.push({
            text: Math.round(value * 100) / 100,
            x: i,
            y: j,
            showarrow: false,
            font: {
              color: matrix[i][j] < -0.5 ? "white" : "black",
            },
          });
        }
      }

      Plotly.react(this.divHeatMapPlot, data, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.$parent.$emit("drawn");
      this.matrixDrawn = true;
    },
    // Conf
    getConf() {
      let conf = {
        selectedColumns: this.selectedColumns.map((c) => c.label),
        selectedMatrixType: this.selectedMatrixType,
      };

      return conf;
    },
    setConf(conf) {
      if (!conf) return;
      if ("selectedColumns" in conf) {
        this.selectedColumns = conf.selectedColumns
          .map((colLabel) => {
            const column = this.data.getColumnByLabel(colLabel);
            if (!column) {
              this.$store.commit("sendMessage", {
                title: "warning",
                msg: "The selected column " + colLabel + " hasn't been found",
              });
            }
            return column;
          })
          .filter((column) => column && column.nbOccurrence > 1);
      }
      if ("selectedMatrixType" in conf) this.selectedMatrixType = conf.selectedMatrixType;
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divHeatMapPlot);
    },
  },
  computed: {
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    loading() {
      this.$parent.$emit("loading", this.loading);
    },
    selectedDataUpdate() {
      this.matrixDrawn = false;
      this.$parent.selectedDataWarning = true;
    },
  },
};
</script>

<style scoped>
#CorrelationMatrix {
  display: flex;
  flex-direction: column;
}
/* Controls */

#axisControls {
  display: flex;
}
#statisticalControls {
  display: flex;
}
.dataGroup {
  margin: 10px;
}

.selectedRows {
  flex-wrap: wrap;
  max-height: 150px;
  overflow-y: auto;
}
/* Axis Selection */
#columnAxisSelection {
  flex: 1;
  display: flex;
  justify-content: space-evenly;
}

#drawBtn {
  margin: 10px;
  width: 80px;
  margin-left: 0px;
}
</style>
