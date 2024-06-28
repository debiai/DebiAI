<template>
  <div
    id="confusionMatrix"
    class="dataVisualizationWidget"
  >
    <!-- Settings-->
    <div
      id="settings"
      v-if="settings"
    >
      <div id="axisControls">
        <!-- Axis buttons -->
        <div
          class="dataGroup"
          id="left"
        >
          <div id="axisSelection">
            <div class="data">
              <div class="name">Truth</div>
              <div class="value">
                <ColumnSelectionButton
                  :data="data"
                  :validColumnsProperties="validColumnsProperties"
                  :defaultColumnIndex="columnTIndex"
                  title="Select the True axis"
                  v-on:selected="xAxisSelect"
                />
              </div>
            </div>
            <button
              style="margin: 3px"
              @click="swap"
            >
              &#8593; Swap &#8595;
            </button>
            <div class="data">
              <div class="name">Prediction</div>
              <div class="value">
                <ColumnSelectionButton
                  :data="data"
                  :validColumnsProperties="validColumnsProperties"
                  :defaultColumnIndex="columnPIndex"
                  title="Select the Predicted axis"
                  v-on:selected="yAxisSelect"
                />
              </div>
            </div>
          </div>
          <!-- Group by color -->
          <div
            class="data"
            id="groupByColor"
            v-if="coloredColumnIndex != null"
          >
            <span class="name">Group by color</span>
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
          :disabled="plotDrawn || !canDraw"
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
import ColumnSelectionButton from "../../common/ColumnSelectionButton";
import swal from "sweetalert";

export default {
  components: {
    ColumnSelectionButton,
  },
  data() {
    return {
      // Configurations
      columnTIndex: null,
      columnPIndex: null,
      dividePerColor: true,

      // Settings
      settings: true,
      plotDrawn: false,
      currentDrawnColorIndex: null,

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
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.checkMatrix);
  },
  mounted() {
    this.divConfusionMatrix = document.getElementById("CFM" + this.index);

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    async checkMatrix() {
      // Check that there isn't too many unique values in the selected columns
      let colGDT = this.data.getColumn(this.columnTIndex);
      let colPred = this.data.getColumn(this.columnPIndex);

      if (!colGDT || !colPred) return;

      const uniquesGDT = colGDT.uniques;
      const uniquesPred = colPred.uniques;

      if (uniquesGDT.length > 30 || uniquesPred.length > 30) {
        let rep = await swal({
          title: "Long calculation: do you want to proceed ?",
          text: "Confusion Matrix: You have selected a truth or a prediction column\
           with more than 30 uniques values. This will create a very big matrix and\
           have an impact on the performances",
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
        let uniquesColor = this.data.getColumn(this.coloredColumnIndex).uniques;
        if (uniquesColor.length > 30) {
          let rep = await swal({
            title: "Long calculation: do you want to proceed ?",
            text: "Confusion Matrix: The selected colored column has\
           more than 30 uniques values and you have chosen to group by color.\
           This will create a large number matrix and have an impact on the performances",
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
      let truthColumnValues = this.data.getColumn(this.columnTIndex).values;
      let predictedColumnValues = this.data.getColumn(this.columnPIndex).values;
      let selectedTruth = this.data.selectedData.map((i) => truthColumnValues[i]);
      let selectedPred = this.data.selectedData.map((i) => predictedColumnValues[i]);

      // Find all the unique values in the selected columns
      let allUniques = [
        ...new Set([
          ...this.data.getColumn(this.columnTIndex).uniques,
          ...this.data.getColumn(this.columnPIndex).uniques,
        ]),
      ];

      // First we create the matrix for all the selected data
      let matrixList = [this.fillMatrix(allUniques, selectedTruth, selectedPred)];

      // Then, if we have a colored column, we create the matrix for each unique value
      if (this.coloredColumnIndex != null && this.dividePerColor) {
        let colColor = this.data.getColumn(this.coloredColumnIndex);

        let selectedColorsValues =
          colColor.type == String
            ? this.data.selectedData.map((i) => colColor.valuesIndex[i])
            : this.data.selectedData.map((i) => colColor.values[i]);
        let selectorUniques =
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques;

        let groupedValues = dataOperations.groupBy(selectedColorsValues, selectorUniques);

        groupedValues.forEach((idValues) => {
          let colorTruth = idValues.map((i) => selectedTruth[i]);
          let colorPred = idValues.map((i) => selectedPred[i]);

          // Finally, we create and add the matrix
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
      let uniquesGDT = this.data.getColumn(this.columnTIndex).uniques;
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

      let uniquesGDT = this.data.getColumn(this.columnTIndex).uniques;
      let data = [];
      for (let i = 0; i < matrixList.length; i++) {
        // Find the subplot title
        let uniqueValue;
        if (i >= 1) {
          uniqueValue = this.data.getColumn(this.coloredColumnIndex).uniques[i - 1];
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

        // add the axis title
        yaxis: {
          // Truth axis
          dtick: 1,
          type: "category",
          title: this.data.getColumn(this.columnTIndex).label + " (Truth)",
          autorange: "reversed",
        },
        xaxis: {
          // Predicted axis
          dtick: 1,
          type: "category",
          title: this.data.getColumn(this.columnPIndex).label + " (Predicted)",
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
          uniqueValue = this.data.getColumn(this.coloredColumnIndex).uniques[matrixNumber - 1];
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
    // axis selection
    xAxisSelect(index) {
      this.columnTIndex = index;
      this.plotDrawn = false;
    },
    yAxisSelect(index) {
      this.columnPIndex = index;
      this.plotDrawn = false;
    },
    swap() {
      let temp = this.columnPIndex;
      this.columnPIndex = this.columnTIndex;
      this.columnTIndex = temp;
      this.checkMatrix();
    },

    // Conf
    getConf() {
      let conf = {
        // Axis
        columnTIndex: this.data.getColumn(this.columnTIndex)?.label,
        columnPIndex: this.data.getColumn(this.columnPIndex)?.label,
      };

      return conf;
    },
    setConf(conf, options) {
      if (!conf) return;
      if ("columnTIndex" in conf) {
        let c = this.data.getColumnByLabel(conf.columnTIndex);
        if (c) this.columnTIndex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnTIndex + " hasn't been found",
          });
      }
      if ("columnPIndex" in conf) {
        let c = this.data.getColumnByLabel(conf.columnPIndex);
        if (c) this.columnPIndex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnPIndex + " hasn't been found",
          });
      }
      if (!options?.onStartup) this.checkMatrix();
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (vm.columnTIndex, vm.columnPIndex, Date.now()),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      return (
        this.data.getColumn(this.columnTIndex).label +
        " and " +
        this.data.getColumn(this.columnPIndex).label
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
        let colTruth = this.data.getColumn(this.columnTIndex);
        let colPred = this.data.getColumn(this.columnPIndex);
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
          let colColor = this.data.getColumn(this.coloredColumnIndex);
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
    canDraw() {
      return this.columnTIndex != null && this.columnPIndex != null;
    },
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    redrawRequired() {
      return !(this.dividePerColor && this.currentDrawnColorIndex !== this.coloredColumnIndex);
    },
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    dividePerColor() {
      this.checkMatrix();
    },
    selectedDataUpdate() {
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
