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

    // Plot
    async checkPlot(askConfirmation = true) {
      let colX = this.data.getColumn(this.columnXindex);
      if (!colX) return;

      // // Check synchronously if the selected column type is string and if their is more than 100 uniques values
      // if (colX.type == String && colX.uniques.length > 100) {
      //   if (!askConfirmation) return;

      //   const answer = await swal({
      //     title: "Warning",
      //     text:
      //       "You are about to display a plot with more than 100 bins.\n" +
      //       "This may take a while. Do you want to proceed?",
      //     icon: "warning",
      //     buttons: true,
      //   });
      //   console.log(answer);
      // }

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
      // on x axis
      let colSecondX;
      let secondSelectedX;
      if (this.data.columnExists(this.secondColumnIndex)) {
        colSecondX = this.data.getColumn(this.secondColumnIndex);
        if (colSecondX.type == String)
          secondSelectedX = this.data.selectedData.map((i) => colSecondX.valuesIndex[i]);
        else secondSelectedX = this.data.selectedData.map((i) => colSecondX.values[i]);
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
          let rep = dataOperations.getRepartition(values, this.bins - 1, colX.min, colX.max);

          xSections = rep.xSections;
          let repartition = rep.repartition;

          if (colX.type == String) xSectionsText = xSections.map((v, i) => colX.uniques[i]);

          let trace = {
            name: String(colColor.uniques[i]),
            type: this.plotType,
            mode: "lines",
            x: xSections,
            y: repartition.map((v) => (v * 100) / this.data.selectedData.length),
          };

          // Display more values in the bars
          if (this.displayDetails)
            trace.text = repartition.map((v) => "<b>" + v + "</b> / " + idValues.length);

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
        let rep = dataOperations.getRepartition(selectedX, this.bins - 1, colX.min, colX.max);

        xSections = rep.xSections;
        let repartition = rep.repartition;

        plotlyData = [
          {
            name: colX.label + " distribution",
            mode: "lines",
            type: this.plotType,
            x: xSections,
            y: repartition.map((v) => (v * 100) / this.data.selectedData.length),
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
          let rep2 = dataOperations.getRepartition(
            secondSelectedX,
            this.bins - 1,
            colX.min,
            colX.max
          );

          let xSections2 = rep2.xSections;
          let repartition2 = rep2.repartition;
          plotlyData.push({
            name: colSecondX.label + " distribution",
            mode: "lines",
            type: this.plotType,
            x: xSections2,
            y: repartition2.map((v) => (v * 100) / this.data.selectedData.length),
            marker: {
              color: "rgb(223,17,10)",
              line: {
                color: "rgb(0, 104, 141)",
                width: 1.5,
              },
            },
          });
          if (this.displayDetails)
            plotlyData[1].text = repartition2.map(
              (v) => "<b>" + v + "</b> / " + this.data.selectedData.length
            );
        }

        // Display more values in the bars
        if (this.displayDetails)
          plotlyData[0].text = repartition.map(
            (v) => "<b>" + v + "</b> / " + this.data.selectedData.length
          );
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
