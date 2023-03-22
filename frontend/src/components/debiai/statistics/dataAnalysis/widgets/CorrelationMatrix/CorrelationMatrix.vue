<template>
  <div
    id="CorrelationMatrix"
    class="dataVisualisationWidget"
  >
    <!-- Axis selection Modal -->
    <modal
      v-if="axisSelection"
      @close="cancelAxiesSettings"
    >
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
    <div
      id="axisControls"
      v-if="settings"
    >
      <!-- Axis btns -->
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
        <div class="data">
          <div class="name">Significativ only</div>
          <div class="value">
            <input
              type="checkbox"
              :id="'significativOnly' + index"
              class="customCbx"
              v-model="significativOnly"
              style="display: none"
            />
            <label
              :for="'significativOnly' + index"
              class="toggle"
            >
              <span></span>
            </label>
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
      matrix: [],

      // Settings
      settings: true,
      significativOnly: false,
      matrixDrawed: false,
      axisSelection: false,
      selectedMatrixType: "pearson",
      error: false,
      loading: false,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
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
    // axies selection
    selectAxis() {
      this.axisSelection = true;
    },
    cancelAxiesSettings() {
      this.axisSelection = false;
    },
    axiesSelect(selectedColumns) {
      this.selectedColumns = selectedColumns
        .map((colId) => this.data.columns.find((col) => col.index == colId))
        .filter((c) => c.nbOccu > 1);

      this.axisSelection = false;
      this.matrixDrawed = false;

      this.calculate();
    },
    async fillMatrix() {
      // Loading handling
      this.loading = true;

      // Creating data to send
      var columnsData = [];
      this.selectedColumns.forEach((c) => {
        if (c.type == String) columnsData.push(this.selectedData.map((i) => c.valuesIndex[i]));
        else columnsData.push(this.selectedData.map((i) => c.values[i]));
      });

      // Sending request
      return this.$backendDialog
        .correlationMatrix(columnsData, this.selectedMatrixType)
        .finally(() => {
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
          this.error = true;
          setTimeout(() => {
            this.error = false;
          }, 5000);
        })
        .then((data) => {
          return data;
        });
    },
    calculate() {
      this.fillMatrix().then((matrix) => {
        this.matrix = matrix;
        if (typeof this.matrix === "object") {
          this.drawMatrix();
          // Might change data description
        } else {
          console.error("Unexpected backend matrix type " + typeof this.matrix);
          this.error = true;
          setTimeout(() => {
            this.error = false;
          }, 5000);
        }
      });
    },
    drawMatrix() {
      var colorscale = [
        [0, "rgb(0,0,255)"],
        [0.5, "rgb(255,255,255)"],
        [1, "rgb(255,0,0)"],
      ];
      if (this.significativOnly) {
        colorscale = [
          [0, "rgb(0,0,255)"],
          [0.1, "rgb(0,0,255)"],
          [0.1, "rgb(255,255,255)"],
          [0.9, "rgb(255,255,255)"],
          [0.9, "rgb(255,0,0)"],
          [1, "rgb(255,0,0)"],
        ];
      }
      var data = [
        {
          z: this.matrix.map((r) => r.map((c) => c[0])),
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

      for (let i = 0; i < this.matrix.length; i++) {
        for (let j = 0; j < this.matrix[i].length; j++) {
          let value = this.matrix[i][j][0];
          layout.annotations.push({
            text: this.significativOnly
              ? Math.abs(value) > 0.8
                ? Math.round(value * 100) / 100 + "<br>" + "&#9733;".repeat(this.matrix[i][j][1])
                : ""
              : Math.round(value * 100) / 100 + "<br>" + "&#9733;".repeat(this.matrix[i][j][1]),
            x: i,
            y: j,
            showarrow: false,
            font: {
              color: this.matrix[i][j][0] < -0.5 ? "white" : "black",
            },
          });
        }
      }

      Plotly.react(this.divHeatMapPlot, data, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.$parent.$emit("drawed");
      this.matrixDrawed = true;
    },
  },
  watch: {
    loading() {
      this.$parent.$emit("loading", this.loading);
    },
    selectedData() {
      this.matrixDrawed = false;
      this.$parent.selectedDataWarning = true;
    },
    significativOnly() {
      this.drawMatrix();
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
/* Axies Selection */
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
