<template>
  <div
    id="confusionMatrix"
    class="dataVisualizationWidget"
  >
    <!-- Axis selection Modals -->
    <modal
      v-if="trueAxisSelection"
      @close="cancelXaxiesSettings"
    >
      <ColumnSelection
        title="Select the True axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="[columnTindex]"
        v-on:cancel="cancelXaxiesSettings"
        v-on:colSelect="xAxiesSelect"
      />
    </modal>
    <modal
      v-if="predAxisSelection"
      @close="cancelYaxiesSettings"
    >
      <ColumnSelection
        title="Select the Predicted axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="[columnPindex]"
        v-on:cancel="cancelYaxiesSettings"
        v-on:colSelect="yAxiesSelect"
      />
    </modal>

    <div
      id="settings"
      v-if="settings"
    >
      <div id="axisControls">
        <!-- Axis btns -->
        <div
          class="dataGroup"
          id="left"
        >
          <div id="axisSelection">
            <div class="data">
              <div class="name">Truth</div>
              <div class="value">
                <Column
                  :column="data.columns.find((c) => c.index == columnTindex)"
                  :colorSelection="true"
                  v-on:selected="trueAxisSelection = true"
                />
              </div>
            </div>
            <button
              style="margin: 3px;"
              @click="swap"
            >
              &#8593; Swap &#8595;
            </button>
            <div class="data">
              <div class="name">Prediction</div>
              <div class="value">
                <Column
                  :column="data.columns.find((c) => c.index == columnPindex)"
                  :colorSelection="true"
                  v-on:selected="predAxisSelection = true"
                />
              </div>
            </div>
          </div>
          <!-- Groub by color -->
          <div
            class="data"
            id="groupByColor"
            v-if="coloredColumnIndex != null"
          >
            <span class="name">Groub by color</span>
            <div class="value">
              <input
                type="checkbox"
                :id="'dividePerColorCbxConfMatrix' + index"
                class="customCbx"
                v-model="dividePerColor"
                style="display: none"
              />
              <label
                :for="'dividePerColorCbxConfMatrix' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
        </div>
        <!-- Draw -->
        <button
          id="drawBtn"
          @click="checkMatrix"
          :disabled="plotDrawn"
          class="blue"
        >
          Draw
        </button>
      </div>
    </div>

    <div
      class="plot"
      :id="'CFM' + index"
    ></div>
  </div>
</template>

<script>
import dataOperations from "@/services/statistics/dataOperations";
import { plotlyToImage } from "@/services/statistics/analysisExport";
import Plotly from "plotly.js/dist/plotly";

// components
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";
import swal from "sweetalert";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      // Cofigurations
      columnTindex: 0,
      columnPindex: 0,
      dividePerColor: true,

      // Settings
      settings: true,
      plotDrawn: false,
      trueAxisSelection: false,
      predAxisSelection: false,
      currentDrawnColorIndex: null,
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
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.checkMatrix);
  },
  mounted() {
    this.divConfusionMatrix = document.getElementById("CFM" + this.index);
    this.xAxiesSelect(0);
    this.yAxiesSelect(1);

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    async checkMatrix() {
      // Check that there isn't too many unique values in the selected columns
      let uniquesGDT = this.data.columns[this.columnTindex].uniques;
      let uniquesPred = this.data.columns[this.columnPindex].uniques;

      if (uniquesGDT.length > 30 || uniquesPred.length > 30) {
        let rep = await swal({
          title: "Long calculation: do you want to proceed ?",
          text: "Confusion Matrix: You have selected a truth or a prediction column\
           with more than 30 uniques values. This will create a very big matrix and\
           have an impact on the performaces",
          icon: "warning",
          buttons: {
            continue: { text: "continue", className: "warning" },
            cancel: "cancel",
          },
          dangerMode: true,
        });

        if (rep == "continue") {
          this.createMatrix();
          return;
        } else return;
      }

      // Same with the colored column
      if (this.coloredColumnIndex != null && this.dividePerColor) {
        let uniquesColor = this.data.columns[this.coloredColumnIndex].uniques;
        if (uniquesColor.length > 30) {
          let rep = await swal({
            title: "Long calculation: do you want to proceed ?",
            text: "Confusion Matrix: The selected colored column has\
           more than 30 uniques values and you have chosen to group by color.\
           This will create a large number matrix and have an impact on the performaces",
            icon: "warning",
            buttons: {
              continue: { text: "continue", className: "warning" },
              continueWithoutColor: "continue without grouping by color",
              cancel: "cancel",
            },
            dangerMode: true,
          });
          if (rep == "continue") {
            this.createMatrix();
            return;
          } else if (rep == "continueWithoutColor") {
            this.dividePerColor = false;
            this.createMatrix();
            return;
          } else return;
        }
      }

      this.createMatrix();
    },

    createMatrix() {
      console.time("ConfusionMatrix");
      // Load values
      let truthColumnValues = this.data.columns[this.columnTindex].values;
      let predictedColumnValues = this.data.columns[this.columnPindex].values;
      let selectedTruth = this.selectedData.map((i) => truthColumnValues[i]);
      let selectedPred = this.selectedData.map((i) => predictedColumnValues[i]);

      // Find all the unique values in the selected columns
      let allUniques = [
        ...new Set([
          ...this.data.columns[this.columnTindex].uniques,
          ...this.data.columns[this.columnPindex].uniques,
        ]),
      ];

      // First we create the matrix for all the selected data
      let matrixList = [this.fillMatrix(allUniques, selectedTruth, selectedPred)];

      // Then, if we have a colored column, we create the matrix for each unique value
      if (this.coloredColumnIndex != null && this.dividePerColor) {
        let colColor = this.data.columns[this.coloredColumnIndex];

        let selectedColorsValues =
          colColor.type == String
            ? this.selectedData.map((i) => colColor.valuesIndex[i])
            : this.selectedData.map((i) => colColor.values[i]);
        let selectorUniques =
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques;

        let groupedValues = dataOperations.groupBy(selectedColorsValues, selectorUniques);

        groupedValues.forEach((idValues) => {
          let colorTruth = idValues.map((i) => selectedTruth[i]);
          let colorPred = idValues.map((i) => selectedPred[i]);

          // Finnaly, we create and add the matrix
          matrixList.push(this.fillMatrix(allUniques, colorTruth, colorPred));
        });

        this.currentDrawnColorIndex = this.coloredColumnIndex;
      }
      this.drawMatrix(matrixList, allUniques);
      console.timeEnd("ConfusionMatrix");
    },
    fillMatrix(allUniques, truth, pred) {
      let indexer = {};
      let count = {};

      // Initialize indexer
      allUniques.forEach((uniqueValue) => {
        indexer[uniqueValue] = {};
        count[uniqueValue] = 0;

        allUniques.forEach((uniqueValue2) => (indexer[uniqueValue][uniqueValue2] = 0));
      });

      // Count number of value predicted for each truth
      truth.forEach((v, i) => {
        indexer[v][pred[i]] += 1;
        count[v] += 1;
      });

      // Fill matrix according to indexer
      let matrix = [];
      let uniquesGDT = this.data.columns[this.columnTindex].uniques;
      uniquesGDT.forEach((uniqueValue) => {
        let row = [];
        allUniques.forEach((uniqueValue2) => {
          row.push(
            count[uniqueValue] > 0 ? indexer[uniqueValue][uniqueValue2] / count[uniqueValue] : null
          );
        });
        matrix.push(row);
      });

      return matrix;
    },

    drawMatrix(matrixList, allUniques) {
      const colorscale = [
        [0, "rgb(255,255,255)"],
        [1, "rgb(255,0,0)"],
      ];

      let uniquesGDT = this.data.columns[this.columnTindex].uniques;
      let data = [];
      for (let i = 0; i < matrixList.length; i++) {
        // Find the subplot title
        let uniqueValue;
        if (i >= 1) {
          uniqueValue = this.data.columns[this.coloredColumnIndex].uniques[i - 1];
        }

        data.push({
          z: matrixList[i],
          x: allUniques.map((e) => "&nbsp;" + e + "&nbsp;"),
          y: uniquesGDT.map((e) => "&nbsp;" + e + "&nbsp;"),
          zmin: 0,
          zmax: 1,
          type: "heatmap",
          colorscale: colorscale,
          xgap: allUniques.length > 15 ? 2 : 5,
          ygap: allUniques.length > 15 ? 2 : 5,
          colorbar: { ticklen: 3 },
          xaxis: "x" + (i + 1),
          yaxis: "y" + (i + 1),
          name: i == 0 ? "All data" : uniqueValue,
        });
      }

      var layout = {
        grid: {
          rows: Math.ceil(matrixList.length / 2),
          columns: matrixList.length > 1 ? 2 : 1,
          pattern: "independent",
        },

        // add the axies title
        yaxis: {
          // Truth axis
          dtick: 1,
          type: "category",
          title: this.data.columns[this.columnTindex].label + " (Truth)",
          autorange: "reversed",
        },
        xaxis: {
          // Predicted axis
          dtick: 1,
          type: "category",
          title: this.data.columns[this.columnPindex].label + " (Predicted)",
          side: "top",
        },
        margin: {
          l: 120,
          r: 10,
          b: 30,
          t: 70,
        },

        // Empty annotations list, will be filled later
        annotations: [],
      };
      // Add the annotations
      matrixList.forEach((matrix, matrixNumber) => {
        // Add the values for each tile of each matrix
        for (let i = 0; i < matrix.length; i++) {
          for (let j = 0; j < matrix[i].length; j++) {
            let value = Math.round(matrix[i][j] * 100) / 100;

            layout.annotations.push({
              text: matrix[i][j] > 0 ? value : "",
              x: j,
              y: i,
              showarrow: false,
              font: { color: value > 50 ? "white" : "black" },
              xref: "x" + (matrixNumber + 1),
              yref: "y" + (matrixNumber + 1),
            });
          }
        }
        // Add the title of each subplot
        let uniqueValue;
        if (matrixNumber >= 1)
          uniqueValue = this.data.columns[this.coloredColumnIndex].uniques[matrixNumber - 1];
        if (this.coloredColumnIndex != null && this.dividePerColor) {
          layout.annotations.push({
            text: matrixNumber >= 1 ? uniqueValue : "All data",
            font: { size: 16 },
            x: (matrix[0].length - 1) / 2,
            y: -0.7,
            showarrow: false,
            xref: "x" + (matrixNumber + 1),
            yref: "y" + (matrixNumber + 1),
          });
        }
        // Add the conf for each subplot axis
        if (matrixNumber >= 1) {
          layout["yaxis" + (matrixNumber + 1)] = {
            dtick: 1,
            type: "category",
            autorange: "reversed",
          };
          layout["xaxis" + (matrixNumber + 1)] = {
            dtick: 1,
            type: "category",
            side: "top",
          };
        }
      });

      // Display the matrix
      Plotly.react(this.divConfusionMatrix, data, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.matrixDrawn = true;
      this.$parent.$emit("drawn");

      // Set the filter events
      this.divConfusionMatrix.removeListener("plotly_click", this.selectDataOnPlot);
      this.divConfusionMatrix.on("plotly_click", this.selectDataOnPlot);
    },
    // axies selection
    cancelXaxiesSettings() {
      this.trueAxisSelection = false;
    },
    cancelYaxiesSettings() {
      this.predAxisSelection = false;
    },
    xAxiesSelect(index) {
      this.columnTindex = index;
      this.trueAxisSelection = false;
      this.plotDrawn = false;
    },
    yAxiesSelect(index) {
      this.columnPindex = index;
      this.predAxisSelection = false;
      this.plotDrawn = false;
    },
    swap() {
      let temp = this.columnPindex;
      this.columnPindex = this.columnTindex;
      this.columnTindex = temp;
      this.checkMatrix();
    },

    // Conf
    getConf() {
      let conf = {
        // Axis
        columnTindex: this.data.columns[this.columnTindex].label,
        columnPindex: this.data.columns[this.columnPindex].label,
      };

      return conf;
    },
    setConf(conf) {
      if (!conf) return;
      if ("columnTindex" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnTindex);
        if (c) this.columnTindex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnTindex + " hasn't been found",
          });
      }
      if ("columnPindex" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnPindex);
        if (c) this.columnPindex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnPindex + " hasn't been found",
          });
      }
      this.checkMatrix();
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (vm.columnTindex, vm.columnPindex, Date.now()),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      return (
        this.data.columns[this.columnTindex].label +
        " and " +
        this.data.columns[this.columnPindex].label
      );
    },

    // Filters
    selectDataOnPlot(event) {
      if (
        this.$parent.startFiltering &&
        event &&
        "points" in event &&
        event.points.length > 0 &&
        "pointIndex" in event.points[0]
      ) {
        let filters = [];
        let colTruth = this.data.columns[this.columnTindex];
        let colPred = this.data.columns[this.columnPindex];
        let selectedSquareCoordinates = event.points[0].pointIndex;

        let selectedTruth = colTruth.uniques[selectedSquareCoordinates[0]];
        let selectedPred = colPred.uniques[selectedSquareCoordinates[1]];

        filters.push({
          type: "values",
          values: ["" + selectedTruth],
          columnIndex: colTruth.index,
        });

        filters.push({
          type: "values",
          values: ["" + selectedPred],
          columnIndex: colPred.index,
        });

        // Apply color
        if (this.coloredColumnIndex != null && this.dividePerColor) {
          let colColor = this.data.columns[this.coloredColumnIndex];
          let selectedColor = colColor.uniques[event.points[0].curveNumber - 1];

          filters.push({
            type: "values",
            values: ["" + selectedColor],
            columnIndex: colColor.index,
          });
        }

        // Commit
        this.$store.commit("addFilters", {
          filters,
          from: {
            widgetType: this.$parent.type,
            widgetName: this.$parent.name,
            widgetIndex: this.index,
          },
          removeExisting: true,
        });
      }
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divConfusionMatrix);
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    redrawRequired() {
      return !(this.dividePerColor && this.currentDrawnColorIndex !== this.coloredColumnIndex);
    },
  },
  watch: {
    dividePerColor() {
      this.checkMatrix();
    },
    selectedData() {
      if (!this.$parent.startFiltering) this.$parent.selectedDataWarning = true;
    },
    redrawRequired(o, n) {
      this.$parent.colorWarning = n;
    },
  },
};
</script>

<style scoped>
#confusionMatrix {
  display: flex;
  flex-direction: column;
}

/* Controls */
#axisControls {
  display: flex;
}
.dataGroup {
  margin: 10px;
  margin-bottom: 0px;
}
#left {
  flex: 1;
  align-items: center;
}
#axisSelection {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.value {
  flex: 1;
}
#groupByColor {
  flex-direction: column;
  margin: 10px;
}
#drawBtn {
  margin: 10px;
  width: 80px;
  margin-left: 0px;
  margin-bottom: 0px;
}
</style>
