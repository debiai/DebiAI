<template>
  <div
    id="repartitionPlot"
    class="dataVisualizationWidget"
  >
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
          <div class="name">X axis</div>
          <div class="value gapped">
            <ColumnSelectionButton
              :data="data"
              :validColumnsProperties="validColumnsProperties"
              :defaultColumnIndex="columnXindex"
              title="Select the X axis"
              v-on:selected="xAxisSelect"
            />
            <ColumnSelectionButton
              :data="data"
              :validColumnsProperties="validColumnsProperties"
              :defaultColumnIndex="secondColumnIndex"
              title="+"
              modalTitle="Select the second axis"
              tooltip="Share the distribution with another column"
              canBeRemoved
              v-on:selected="secondAxisSelect"
              v-on:removed="
                secondColumnIndex = null;
                checkPlot();
              "
            />
          </div>
        </div>
        <!-- Options -->
        <div class="dataGroup">
          <!-- group by color -->
          <div
            class="data"
            id="groupByColor"
            v-if="coloredColumnIndex != null && secondColumnIndex === null"
          >
            <div class="name">Group by color</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'dividePerColorCbx' + index"
                class="customCbx"
                v-model="dividePerColor"
                style="display: none"
              />
              <label
                :for="'dividePerColorCbx' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Weight by column -->
          <div
            class="data"
            id="weightByColumn"
          >
            <div class="name">Weight by column</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'weightByColumnCbx' + index"
                class="customCbx"
                v-model="useWeightColumn"
                style="display: none"
              />
              <label
                :for="'weightByColumnCbx' + index"
                class="toggle"
              >
                <span></span>
              </label>
              <ColumnSelectionButton
                v-if="useWeightColumn"
                :data="data"
                :validColumnsProperties="weightColumnProperties"
                :defaultColumnIndex="weightColumnIndex"
                title="Select weight column"
                tooltip="Select a column to use as weights"
                v-on:selected="weightColumnSelect"
              />
            </div>
          </div>
          <!-- Plot type -->
          <div class="data">
            <div class="name">Plot type</div>
            <div class="value">
              <button
                :class="plotType == 'bar' ? 'radioBtn selected' : 'radioBtn'"
                @click="
                  plotType = 'bar';
                  checkPlot();
                "
              >
                Bar
              </button>
              <button
                :class="plotType == 'line' ? 'radioBtn selected' : 'radioBtn'"
                @click="
                  plotType = 'line';
                  displayLegends = true;
                  checkPlot();
                "
              >
                Line
              </button>
            </div>
          </div>
          <!-- display legends -->
          <div
            class="data"
            title="Due to a technical limitation, display the legends will disable the red to blue color gradient common to all the widgets"
            v-if="coloredColumnIndex != null && dividePerColor && plotType == 'bar'"
          >
            <div class="name">Legends</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'displayLegends' + index"
                class="customCbx"
                v-model="displayLegends"
                style="display: none"
              />
              <label
                :for="'displayLegends' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Display details -->
          <div
            class="data"
            id="displayDetails"
            v-if="plotType == 'bar'"
          >
            <div class="name">Details</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'displayDetails' + index"
                class="customCbx"
                v-model="displayDetails"
                style="display: none"
              />
              <label
                :for="'displayDetails' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Bins -->
          <div class="data">
            <div class="name">Bins</div>
            <div class="value">
              <input
                type="number"
                v-model="bins"
                :min="1"
                @change="plotDrawn = false"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Draw -->
      <button
        id="drawBtn"
        type="submit"
        class="blue"
        @click="checkPlot"
        :disabled="!canDraw"
      >
        Draw
      </button>
    </div>
    <div
      class="plot"
      :id="'repDiv' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

// components
import ColumnSelectionButton from "../../common/ColumnSelectionButton";

// services
import dataOperations from "@/services/statistics/dataOperations";
import { plotlyToImage } from "@/services/statistics/analysisExport";
import swal from "sweetalert";

export default {
  components: {
    ColumnSelectionButton,
  },
  data() {
    return {
      // Settings
      settings: true,

      // Conf
      columnXindex: null,
      secondColumnIndex: null,
      dividePerColor: true,
      displayLegends: false,
      displayDetails: false,
      plotType: "bar",
      bins: 0,

      // Weight column options
      useWeightColumn: false,
      weightColumnIndex: null,
      weightColumnProperties: {
        types: ["Num"],
      },

      // Other
      plotDrawn: false,
      currentDrawnColorIndex: null,

      validColumnsProperties: {
        types: ["Num", "Class", "Bool"],
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
    this.$parent.$on("redraw", this.checkPlot);
  },
  mounted() {
    this.divRepPlot = document.getElementById("repDiv" + this.index);
    this.setBins();

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        columnX: this.data.getColumn(this.columnXindex)?.label,
        plotType: this.plotType,
        bins: this.bins,
      };

      if (this.plotType === "bar" && this.displayDetails) conf.displayDetails = this.displayDetails;
      if (this.coloredColumnIndex !== null) {
        if (this.displayLegends) conf.displayLegends = this.displayLegends;
        conf.dividePerColor = this.dividePerColor;
      }
      if (this.useWeightColumn && this.weightColumnIndex !== null) {
        conf.useWeightColumn = this.useWeightColumn;
        conf.weightColumn = this.data.getColumn(this.weightColumnIndex)?.label;
      }
      return conf;
    },
    setConf(conf, options = {}) {
      if (!conf) return;
      if ("columnX" in conf) {
        let c = this.data.getColumnByLabel(conf.columnX);
        if (c) this.columnXindex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("plotType" in conf) this.plotType = conf.plotType;
      if ("displayDetails" in conf) this.displayDetails = conf.displayDetails;
      if ("displayLegends" in conf) this.displayLegends = conf.displayLegends;
      if ("dividePerColor" in conf) this.dividePerColor = conf.dividePerColor;
      if ("bins" in conf) this.bins = conf.bins;
      if ("useWeightColumn" in conf) this.useWeightColumn = conf.useWeightColumn;
      if ("weightColumn" in conf) {
        let c = this.data.getColumnByLabel(conf.weightColumn);
        if (c) this.weightColumnIndex = c.index;
      }

      this.checkPlot(false);
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXindex,
          vm.dividePerColor,
          vm.displayLegends,
          vm.displayDetails,
          vm.plotType,
          vm.bins,
          vm.useWeightColumn,
          vm.weightColumnIndex,
          Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      return this.data.getColumn(this.columnXindex)?.label;
    },

    // Calculate weighted repartition
    getWeightedRepartition(values, weights, nbBins, min, max) {
      // If values aren't numbers, return the standard repartition
      if (values.length === 0 || typeof values[0] === "string") {
        return dataOperations.getRepartition(values, nbBins, min, max);
      }

      // Set up bins
      const step = (max - min) / nbBins;
      const xSections = [];
      const repartition = new Array(nbBins + 1).fill(0);

      // Generate bin boundaries
      for (let i = 0; i <= nbBins; i++) {
        xSections.push(min + i * step);
      }

      // Populate bins with weighted values
      for (let i = 0; i < values.length; i++) {
        const value = values[i];
        if (value < min || value > max || isNaN(value)) continue;

        // Calculate bin index
        let binIndex = Math.floor((value - min) / step);
        // Handle edge case for max value
        if (binIndex > nbBins) binIndex = nbBins;

        // Add weight to the appropriate bin
        repartition[binIndex] += weights[i];
      }

      return { xSections, repartition };
    },

    // Plot
    async checkPlot(askConfirmation = true) {
      let colX = this.data.getColumn(this.columnXindex);
      if (!colX) return;

      // Alert the user if he decided to divide by more than 100 uniq values
      if (this.bins > 100 && colX.type == String) {
        if (!askConfirmation) return;

        const answer = await swal({
          title: "Warning",
          text:
            "You are about to display a plot with more than 100 bins.\n" +
            "This may take a while, do you want to proceed?",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        });

        if (answer !== true) return;
      }

      if (this.coloredColumnIndex !== null) {
        const colColor = this.data.getColumn(this.coloredColumnIndex);
        if (!colColor) return;

        if (this.dividePerColor && colColor.uniques.length > 100) {
          if (!askConfirmation) return;

          const answer2 = await swal({
            title: "Long calculation: do you want to proceed ?",
            text:
              "Repartition plot: You appear to have selected more than 100 uniques color values.\n" +
              "This may take a while, do you want to proceed?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
          });

          if (answer2 !== true) return;
        }
      }

      this.drawPlot();
    },

    drawPlot() {
      let colX = this.data.getColumn(this.columnXindex);
      if (!colX) return;

      let plotlyData = [];

      // === Apply selection ===
      // on x axis
      let selectedX;
      if (colX.type == String) selectedX = this.data.selectedData.map((i) => colX.valuesIndex[i]);
      else selectedX = this.data.selectedData.map((i) => colX.values[i]);

      // get weight values if needed
      let weights;
      if (this.useWeightColumn && this.weightColumnIndex !== null) {
        const weightColumn = this.data.getColumn(this.weightColumnIndex);
        if (weightColumn && weightColumn.type != String) {
          weights = this.data.selectedData.map((i) => weightColumn.values[i]);
        }
      }

      // on x axis
      let colSecondX;
      let secondSelectedX;
      let secondWeights;
      if (this.data.columnExists(this.secondColumnIndex)) {
        colSecondX = this.data.getColumn(this.secondColumnIndex);
        if (colSecondX.type == String)
          secondSelectedX = this.data.selectedData.map((i) => colSecondX.valuesIndex[i]);
        else secondSelectedX = this.data.selectedData.map((i) => colSecondX.values[i]);

        // copy weights for second column if using weights
        if (weights) {
          secondWeights = [...weights];
        }
      }

      let colColor;
      let xSections;
      let xSectionsText;
      if (this.data.columnExists(this.coloredColumnIndex) && this.dividePerColor) {
        // on color axis
        colColor = this.data.getColumn(this.coloredColumnIndex);
        let selectedColors;
        if (colColor.type == String)
          selectedColors = this.data.selectedData.map((i) => colColor.valuesIndex[i]);
        else selectedColors = this.data.selectedData.map((i) => colColor.values[i]);

        // === Divide bar per color ===
        let groupedValues = dataOperations.groupBy(
          selectedColors,
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques
        );

        groupedValues.forEach((idValues, i) => {
          let values = idValues.map((i) => selectedX[i]);

          // Apply weights if needed
          let groupWeights;
          if (weights) {
            groupWeights = idValues.map((i) => weights[i]);
          }

          // Get distribution with or without weights
          let rep;
          if (this.useWeightColumn && groupWeights) {
            rep = this.getWeightedRepartition(
              values,
              groupWeights,
              this.bins - 1,
              colX.min,
              colX.max
            );
          } else {
            rep = dataOperations.getRepartition(values, this.bins - 1, colX.min, colX.max);
          }

          xSections = rep.xSections;
          let repartition = rep.repartition;
          let totalWeight =
            this.useWeightColumn && groupWeights
              ? groupWeights.reduce((sum, val) => sum + val, 0)
              : idValues.length;
          let totalSampleWeight =
            this.useWeightColumn && weights
              ? weights.reduce((sum, val) => sum + val, 0)
              : this.data.selectedData.length;

          if (colX.type == String) xSectionsText = xSections.map((v, i) => colX.uniques[i]);

          let trace = {
            name: String(colColor.uniques[i]),
            type: this.plotType,
            mode: "lines",
            x: xSections,
            y: repartition.map((v) => (v * 100) / totalSampleWeight),
          };

          // Display more values in the bars
          if (this.displayDetails) {
            if (this.useWeightColumn && groupWeights) {
              trace.text = repartition.map(
                (v) => "<b>" + v.toFixed(2) + "</b> / " + totalWeight.toFixed(2)
              );
            } else {
              trace.text = repartition.map((v) => "<b>" + v + "</b> / " + idValues.length);
            }
          }

          // Disabled on option the colorscale because of a plotly Bug
          // follow this issue : https://github.com/plotly/plotly.js/issues/5285
          if (!this.displayLegends) {
            let color =
              colColor.type == String
                ? xSections.map(() => colColor.valuesIndexUniques[i])
                : xSections.map(() => colColor.uniques[i]);

            trace.marker = {
              color,
              colorscale: "Portland",
              cmin: colColor.min,
              cmax: colColor.max,
              showscale: true,
            };

            trace.showlegend = false;
          }

          plotlyData.push(trace);
        });
      } else {
        // No color or no group by selected
        let rep;
        let totalWeight = this.data.selectedData.length;

        // Get distribution with or without weights
        if (this.useWeightColumn && weights) {
          rep = this.getWeightedRepartition(selectedX, weights, this.bins - 1, colX.min, colX.max);
          totalWeight = weights.reduce((sum, val) => sum + val, 0);
        } else {
          rep = dataOperations.getRepartition(selectedX, this.bins - 1, colX.min, colX.max);
        }

        xSections = rep.xSections;
        let repartition = rep.repartition;

        plotlyData = [
          {
            name: colX.label + " distribution",
            mode: "lines",
            type: this.plotType,
            x: xSections,
            y: repartition.map((v) => (v * 100) / totalWeight),
            marker: {
              color: "rgb(0,157,223)",
              line: {
                color: "rgb(0, 104, 141)",
                width: 1.5,
              },
            },
          },
        ];

        // deal with the second axis
        if (this.secondColumnIndex !== null) {
          let rep2;
          let totalWeight2 = this.data.selectedData.length;

          // Get distribution with or without weights for second axis
          if (this.useWeightColumn && secondWeights) {
            rep2 = this.getWeightedRepartition(
              secondSelectedX,
              secondWeights,
              this.bins - 1,
              colX.min,
              colX.max
            );
            totalWeight2 = secondWeights.reduce((sum, val) => sum + val, 0);
          } else {
            rep2 = dataOperations.getRepartition(
              secondSelectedX,
              this.bins - 1,
              colX.min,
              colX.max
            );
          }

          let xSections2 = rep2.xSections;
          let repartition2 = rep2.repartition;
          plotlyData.push({
            name: colSecondX.label + " distribution",
            mode: "lines",
            type: this.plotType,
            x: xSections2,
            y: repartition2.map((v) => (v * 100) / totalWeight2),
            marker: {
              color: "rgb(223,17,10)",
              line: {
                color: "rgb(0, 104, 141)",
                width: 1.5,
              },
            },
          });
          if (this.displayDetails) {
            if (this.useWeightColumn && secondWeights) {
              plotlyData[1].text = repartition2.map(
                (v) => "<b>" + v.toFixed(2) + "</b> / " + totalWeight2.toFixed(2)
              );
            } else {
              plotlyData[1].text = repartition2.map(
                (v) => "<b>" + v + "</b> / " + this.data.selectedData.length
              );
            }
          }
        }

        // Display more values in the bars
        if (this.displayDetails) {
          if (this.useWeightColumn && weights) {
            const totalWeight = weights.reduce((sum, val) => sum + val, 0);
            plotlyData[0].text = repartition.map(
              (v) => "<b>" + v.toFixed(2) + "</b> / " + totalWeight.toFixed(2)
            );
          } else {
            plotlyData[0].text = repartition.map(
              (v) => "<b>" + v + "</b> / " + this.data.selectedData.length
            );
          }
        }
      }

      // set labels for x axis
      if (colX.type == String) xSectionsText = xSections.map((v, i) => colX.uniques[i]);
      else xSections = undefined;

      let layout = {
        title: "<b>" + colX.label + "</b> Distribution",
        bargap: 0,
        barmode: this.secondColumnIndex !== null ? "group" : "stack",
        xaxis: {
          title: {
            text: colX.label,
          },
          tickvals: xSections,
          ticktext: xSectionsText,
        },
        yaxis: {
          title: {
            text: "Density (%)",
          },
        },
        margin: {
          l: 50,
          r: 20,
          b: 60,
          t: 40,
        },
      };

      // Add the second axis name
      if (this.secondColumnIndex !== null)
        layout.title = "<b>" + colSecondX.label + "</b> and " + layout.title;

      // Add the weight column information
      if (this.useWeightColumn && this.weightColumnIndex !== null) {
        const weightCol = this.data.getColumn(this.weightColumnIndex);
        layout.title += " Weighted by <b>" + weightCol.label + "</b>";
      }

      // Add the color to the legend name
      if (colColor) layout.title += " Grouped by <b>" + colColor.label + "</b>";

      Plotly.react(this.divRepPlot, plotlyData, layout, {
        displayModeBar: false,
        responsive: true,
      });
      this.currentDrawnColorIndex = this.coloredColumnIndex;
      this.plotDrawn = true;
      this.$parent.$emit("drawn");

      // Set selection events
      this.divRepPlot.removeListener("plotly_click", this.selectDataOnPlot);
      this.divRepPlot.on("plotly_click", this.selectDataOnPlot);
    },

    clearPlot() {
      Plotly.purge(this.divRepPlot);
      this.plotDrawn = false;
    },

    // Filters
    selectDataOnPlot(selection) {
      if (
        this.$parent.startFiltering &&
        selection.points &&
        selection.points[0] &&
        selection.points[0].x !== undefined &&
        this.bins > 0
      ) {
        let selectionPoint = selection.points[0];
        let col = this.data.getColumn(this.columnXindex);
        let filters = [];

        if (col.type == String) {
          filters.push({
            type: "values",
            columnIndex: this.columnXindex,
            values: [col.uniques[selectionPoint.x]],
          });
        } else {
          let min = selectionPoint.x;
          // Find the bins intervals
          let max = min + (col.max - col.min) / this.bins;

          // add filter
          filters.push({
            type: "intervals",
            columnIndex: this.columnXindex,
            intervals: [{ min, max }],
          });
        }
        // apply filters on the color
        if (this.data.columnExists(this.coloredColumnIndex) && this.dividePerColor) {
          filters.push({
            type: "values",
            columnIndex: this.currentDrawnColorIndex,
            values: [
              "" +
                this.data.getColumn(this.currentDrawnColorIndex).uniques[
                  selectionPoint.curveNumber
                ],
            ],
          });
        }
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
      return await plotlyToImage(this.divRepPlot);
    },

    // axis selection
    xAxisSelect(index) {
      this.columnXindex = index;
      this.setBins();
      if (this.bins < 100) this.checkPlot(false);
      else this.clearPlot();
    },
    secondAxisSelect(index) {
      this.secondColumnIndex = index;
      this.dividePerColor = false;
      this.checkPlot(false);
    },
    weightColumnSelect(index) {
      this.weightColumnIndex = index;
      this.checkPlot(false);
    },
    setBins() {
      let colX = this.data.getColumn(this.columnXindex);
      if (!colX) return;
      this.bins =
        colX.type == String ? colX.nbOccurrence : colX.nbOccurrence > 100 ? 100 : colX.nbOccurrence;
    },
  },
  computed: {
    canDraw() {
      return this.columnXindex !== null && this.bins > 0;
    },
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    redrawRequired() {
      return !(this.currentDrawnColorIndex !== this.coloredColumnIndex);
    },
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    dividePerColor() {
      this.checkPlot();
    },
    displayLegends() {
      this.checkPlot();
    },
    displayDetails() {
      this.checkPlot();
    },
    useWeightColumn() {
      if (this.useWeightColumn && this.weightColumnIndex === null) {
        this.plotDrawn = false;
      } else {
        this.checkPlot();
      }
    },
    weightColumnIndex() {
      if (this.useWeightColumn) {
        this.checkPlot();
      }
    },
    selectedDataUpdate() {
      if (!this.$parent.startFiltering && this.plotDrawn) this.$parent.selectedDataWarning = true;
    },
    coloredColumnIndex() {
      this.plotDrawn = false;
    },
    redrawRequired(o, n) {
      this.$parent.colorWarning = n;
    },
  },
};
</script>

<style scoped lang="scss">
#repartitionPlot {
  display: flex;
  flex-direction: column;

  /* Controls */
  #axisControls {
    display: flex;

    #columnAxisSelection {
      position: relative;
    }

    #statisticalControls {
      display: flex;
    }

    .dataGroup {
      flex-wrap: wrap;
    }

    #columnAxisSelection.data + .data {
      margin-left: 0px;
      margin-top: 10px;
    }
  }

  /* Axis Selection */
  #columnAxisSelection {
    flex: 1;
    display: flex;
    flex-direction: column;

    .dataGroup {
      justify-content: space-evenly;
    }

    .value {
      flex: 1;
      display: flex;
    }
  }

  #drawBtn {
    margin: 3px;
    width: 80px;
  }

  input {
    width: 70px;
  }
}
</style>
