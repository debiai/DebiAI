<template>
  <div
    id="RangeSliderPlot"
    class="dataVisualizationWidget"
  >
    <!-- Axis selection Modals -->
    <modal
      v-if="xAxisSelection"
      @close="xAxisSelection = false"
    >
      <ColumnSelection
        title="Select the X axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="[columnXindex]"
        v-on:cancel="xAxisSelection = false"
        v-on:colSelect="xAxisSelect"
      />
    </modal>
    <modal
      v-if="yAxisSelection"
      @close="yAxisSelection = false"
    >
      <ColumnSelection
        title="Select the Y axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        v-on:cancel="yAxisSelection = false"
        :defaultSelected="[columnYindex]"
        v-on:colSelect="yAxisSelect"
      />
    </modal>
    <!-- multi Y axis selection -->
    <modal
      v-if="yMultipleAxisSelection"
      @close="yMultipleAxisSelection = false"
    >
      <ColumnSelection
        title="Select the other columns to display in Y axis"
        :data="data"
        :colorSelection="true"
        :defaultSelected="[...selectedYColumnsIds]"
        v-on:cancel="yMultipleAxisSelection = false"
        v-on:validate="yMultipleAxisSelect"
      />
    </modal>
    <!-- Tag axis selection -->
    <modal
      v-if="tagAxisSelection"
      @close="tagAxisSelection = false"
    >
      <ColumnSelection
        title="Select the background color column"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="columnTagIndex === null ? undefined : [columnTagIndex]"
        v-on:cancel="tagAxisSelection = false"
        v-on:colSelect="tagAxisSelect"
      />
    </modal>

    <!-- Settings -->
    <div
      id="settings"
      v-if="settings"
    >
      <div id="axisControls">
        <!-- Axis buttons -->
        <div class="dataGroup axis">
          <div class="data">
            <div class="name">X axis</div>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnXindex)"
                :colorSelection="true"
                v-on:selected="xAxisSelection = true"
              />
            </div>
          </div>
          <button
            class="warning"
            @click="swap"
          >
            Swap
          </button>
          <div class="data">
            <div class="name">Y axis</div>
            <div
              class="value"
              v-if="!multipleYAxis"
            >
              <Column
                :column="data.columns.find((c) => c.index == columnYindex)"
                :colorSelection="true"
                v-on:selected="yAxisSelection = true"
              />
            </div>
            <div
              class="value"
              v-else
            >
              <button
                id="addColumnBtn"
                class=""
                title="Add more columns for the Y axis"
                @click="yMultipleAxisSelection = true"
              >
                {{
                  selectedYColumnsIds.length > 0
                    ? `${selectedYColumnsIds.length} Y column(s) selected`
                    : "+ Select Y columns"
                }}
              </button>
            </div>
          </div>
        </div>
        <div
          class="dataGroup"
          id="configButtons"
        >
          <!-- Group by color -->
          <div
            class="data"
            v-if="coloredColumnIndex !== null"
          >
            <div class="name">Group by color</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'gbc' + index"
                class="customCbx"
                style="display: none"
                v-model="dividePerColor"
              />
              <label
                :for="'gbc' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Tag column -->
          <div class="data">
            <span class="name">Background color</span>
            <div
              class="value"
              v-if="columnTagIndex !== null"
            >
              <Column
                :column="data.columns.find((c) => c.index == columnTagIndex)"
                :colorSelection="true"
                v-on:selected="tagAxisSelection = true"
              />
              <button
                class="red"
                @click="
                  columnTagIndex = null;
                  plotDrawn = false;
                "
              >
                Remove
              </button>
            </div>
            <div
              class="value"
              v-else
            >
              <button @click="tagAxisSelection = true">Select a column</button>
            </div>
          </div>
          <!-- Multiple Y axis -->
          <div class="data">
            <div class="name">Multiple Y columns</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'mya' + index"
                class="customCbx"
                style="display: none"
                v-model="multipleYAxis"
              />
              <label
                :for="'mya' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Draw -->
      <button
        id="drawBtn"
        class="blue"
        @click="drawPlot"
      >
        Draw
      </button>
    </div>

    <!-- Plot -->
    <div
      class="plot"
      :id="'rangeSliderPlot_' + this.index"
    ></div>
  </div>
</template>

<script>
import swal from "sweetalert";
import Plotly from "plotly.js/dist/plotly";
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";
import dataOperations from "@/services/statistics/dataOperations";
import { plotlyToImage } from "@/services/statistics/analysisExport";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      // Settings
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,
      yMultipleAxisSelection: false,
      multipleYAxis: false,
      tagAxisSelection: false,

      // Conf
      columnXindex: 0,
      columnYindex: 0,
      selectedYColumnsIds: [],
      dividePerColor: true,
      columnTagIndex: null,

      // Other
      currentDrawnColorIndex: null,
      plotDrawn: false,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Widget events
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawPlot);

    // Filtering
    this.border1 = null;
    this.border2 = null;
    // Filters events
    this.$parent.$on("filterStarted", this.filterStarted);
    this.$parent.$on("filterEnded", this.filterEnded);
    this.$parent.$on("filterCleared", this.filterCleared);
  },
  mounted() {
    this.plotDiv = document.getElementById("rangeSliderPlot_" + this.index);

    if (this.data.columns.length >= 2) {
      this.xAxisSelect(0);
      this.yAxisSelect(1);
    }

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.columns[this.columnXindex].label,
        dividePerColor: this.dividePerColor,
      };

      // Multiple Y axis
      if (this.multipleYAxis) {
        conf.multipleYAxis = true;
        conf.YColumns = this.selectedYColumnsIds.map((id) => this.data.columns[id].label);
      } else {
        conf.columnY = this.data.columns[this.columnYindex].label;
      }

      // Tag column
      if (this.columnTagIndex !== null)
        conf.columnTag = this.data.columns[this.columnTagIndex].label;
      else conf.columnTag = null;

      return conf;
    },
    setConf(conf) {
      const sendColNotFoundMessage = (col) => {
        this.$store.commit("sendMessage", {
          title: "warning",
          msg: "The column " + col + " hasn't been found",
        });
      };
      if (!conf) return;
      if ("columnX" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnX);
        if (c) this.columnXindex = c.index;
        else sendColNotFoundMessage(conf.columnX);
      }
      if ("columnY" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnY);
        if (c) this.columnYindex = c.index;
        else sendColNotFoundMessage(conf.columnY);
      }
      if ("multipleYAxis" in conf && conf.multipleYAxis && "YColumns" in conf) {
        this.multipleYAxis = true;
        this.selectedYColumnsIds = [];
        conf.YColumns.forEach((label) => {
          let c = this.data.columns.find((c) => c.label == label);
          if (c) this.selectedYColumnsIds.push(c.index);
          else sendColNotFoundMessage(label);
        });
      } else this.multipleYAxis = false;
      if ("dividePerColor" in conf) this.dividePerColor = conf.dividePerColor;
      if (conf.columnTag === null || conf.columnTag === undefined) this.columnTagIndex = null;
      if ("columnTag" in conf && conf.columnTag !== null) {
        let c = this.data.columns.find((c) => c.label == conf.columnTag);
        if (c) this.columnTagIndex = c.index;
        else sendColNotFoundMessage(conf.columnTag);
      }
      this.plotDrawn = false;
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXindex,
          vm.columnYindex,
          vm.selectedYColumnsIds,
          vm.dividePerColor,
          vm.multipleYAxis,
          vm.columnTagIndex,
          Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      let confName;
      if (this.multipleYAxis) {
        confName = this.data.columns[this.columnXindex].label + " / ";
        this.selectedYColumnsIds.forEach((id) => {
          confName += this.data.columns[id].label + ", ";
        });
        confName = confName.slice(0, -3);
      } else
        confName =
          this.data.columns[this.columnXindex].label +
          " / " +
          this.data.columns[this.columnYindex].label;

      console.log(this.multipleYAxis);
      console.log(confName);
      if (this.dividePerColor && this.coloredColumnIndex !== null)
        confName += " / " + this.data.columns[this.coloredColumnIndex].label;

      if (this.columnTagIndex !== null)
        confName += ", Background is " + this.data.columns[this.columnTagIndex].label;

      return confName;
    },

    // Display
    async drawPlot() {
      var colX = this.data.columns[this.columnXindex];

      // Get the Y axis index
      let YAxisIndexes;
      if (this.multipleYAxis) YAxisIndexes = this.selectedYColumnsIds;
      else YAxisIndexes = [this.columnYindex];
      var colsY = YAxisIndexes.map((index) => this.data.columns[index]);

      // Apply selection
      let valuesX = this.selectedData.map((i) => colX.values[i]);
      let valuesListY = colsY.map((col) => this.selectedData.map((i) => col.values[i]));

      const lines = [];

      if (this.dividePerColor && this.coloredColumnIndex !== null) {
        // Color
        const colColor = this.data.columns[this.coloredColumnIndex];

        if (colColor.uniques.length > 20) {
          // This is a lot, we ask for confirmation
          let rep = await swal({
            title: "Long calculation: do you want to proceed ?",
            text: "Range slider plot: You have selected to group data by color\
           with more than 20 uniques values. This will create a lot of lines, this may\
           have an impact on the performances",
            icon: "warning",
            buttons: {
              continue: { text: "continue", className: "warning" },
              cancel: "cancel",
            },
            dangerMode: true,
          });
          if (rep != "continue") return;
        }

        let selectedColorsValues =
          colColor.type == String
            ? this.selectedData.map((i) => colColor.valuesIndex[i])
            : this.selectedData.map((i) => colColor.values[i]);
        let selectorUniques =
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques;

        valuesListY.forEach((valuesY, i) => {
          const yAxisColumnLabel = colsY[i].label;
          let groupedValues = dataOperations.groupBy(selectedColorsValues, selectorUniques);

          groupedValues.forEach((idValues, j) => {
            let colorX = idValues.map((k) => valuesX[k]);
            let colorY = idValues.map((k) => valuesY[k]);

            let lineName;
            if (this.multipleYAxis) lineName = yAxisColumnLabel + " - " + colColor.uniques[j];
            else lineName = colColor.uniques[j];

            lines.push({
              x: colorX,
              y: colorY,
              type: "line",
              name: lineName,
              transforms: [
                {
                  type: "sort",
                  target: "x",
                  order: "descending",
                },
              ],
            });
          });
        });
      } else {
        // No color
        valuesListY.forEach((valuesY, i) => {
          const yAxisColumnLabel = colsY[i].label;

          lines.push({
            x: valuesX,
            y: valuesY,
            type: "line",
            name: yAxisColumnLabel,
            transforms: [
              {
                type: "sort",
                target: "x",
                order: "descending",
              },
            ],
          });
        });
        // Set the color to black if there is only one line
        if (lines.length == 1) lines[0].line = { color: "black" };
      }

      // Create the plot title
      let plotTitle;

      if (this.multipleYAxis) {
        let colYLabels = colsY.map((col) => col.label).join(", ");
        if (colYLabels.length > 50) colYLabels = colYLabels.slice(0, 50) + "...";

        plotTitle = "<b>" + colX.label + "</b> / <b>" + colYLabels + "</b>";
      } else plotTitle = "<b>" + colX.label + "</b> / <b>" + colsY[0].label + "</b>";

      if (this.dividePerColor && this.coloredColumnIndex !== null) {
        const colColor = this.data.columns[this.coloredColumnIndex];
        plotTitle += " grouped by <b>" + colColor.label + "</b>";
      }

      if (this.columnTagIndex !== null) {
        const colTag = this.data.columns[this.columnTagIndex];
        plotTitle += " with background color <b>" + colTag.label + "</b>";
      }

      // Create the layout
      const layout = {
        title: plotTitle,
        xaxis: {
          rangeSlider: true,
        },
        yaxis: {
          autorange: true,
          type: "linear",
          fixedrange: false,
        },
        scene: {
          yaxis: {
            autorange: true,
          },
        },
        selectdirection: "h",
        margin: {
          l: 50,
          r: 20,
          b: 50,
          t: 50,
        },
        shapes: [],
      };

      // Deal with background tag color
      let traces = lines;
      // const traces = [];
      const heatmap = this.drawTagHeatmap(valuesX, layout);
      if (heatmap) {
        // Set all the lines axis to y2
        lines.forEach((line) => {
          line.yaxis = "y2";
        });

        traces.unshift(heatmap);
      }

      // Draw
      Plotly.react(this.plotDiv, traces, layout, {
        displayModeBar: false,
        responsive: true,
      });

      // Deal with point click to select data
      // Goal : place two lines and export boundaries
      this.plotDiv.removeListener("plotly_click", this.selectDataOnPlot);
      this.plotDiv.on("plotly_click", this.selectDataOnPlot);

      this.plotDrawn = true;
      this.$parent.$emit("drawn");
      this.currentDrawnColorIndex = this.coloredColumnIndex;
    },
    drawLine(x) {
      const lineStyle = {
        type: "line",
        x0: x,
        x1: x,

        y0: 0,
        y1: 1,
        yref: "paper",

        line: {
          color: "red",
          width: 2,
          dash: "dashdot",
        },
      };

      Plotly.relayout(this.plotDiv, { "shapes[0]": lineStyle });
    },
    drawRectangle(x1, x2) {
      const recStyle = {
        type: "rect",
        x0: x1,
        x1: x2,

        y0: 0,
        y1: 1,
        yref: "paper",

        fillcolor: "red",
        opacity: 0.1,
        line: { width: 0 },
      };

      Plotly.relayout(this.plotDiv, { "shapes[0]": recStyle });
    },
    drawTagHeatmap(x, layout) {
      if (this.columnTagIndex === null) return;
      const colTag = this.data.columns[this.columnTagIndex];

      // Get the tag values with selection
      let valuesTag = [];
      if (colTag.type === String) valuesTag = this.selectedData.map((i) => colTag.valuesIndex[i]);
      else valuesTag = this.selectedData.map((i) => colTag.values[i]);

      // Construct a text array for the hover
      const textTag = valuesTag.map((v) => colTag.uniques[v] || v);

      // Create an array full of 1 for the y axis
      const valuesTagY = [];
      for (let i = 0; i < valuesTag.length; i++) valuesTagY.push(1);

      const heatmap = {
        name: colTag.label,
        x: x,
        y: valuesTagY,
        z: valuesTag,
        text: textTag,
        hovertemplate: "%{text}",
        type: "heatmap",
        opacity: 0.45,
        colorscale: "Portland",
      };

      if (colTag.type === String || this.multipleYAxis) heatmap.showscale = false;

      // Complete the layout with an additional yaxis
      layout.yaxis = {
        title: "Ax1",
        side: "right",
        title: "",
        showgrid: false,
        showticklabels: false,
        showline: false,
        zeroline: false,
        ticks: "",
        ticksuffix: " ",
      };
      layout.yaxis2 = {
        overlaying: "y",
        autorange: true,
        type: "linear",
        fixedrange: false,
      };

      return heatmap;
    },
    resetShapes() {
      if (this.border1 !== null && this.border2 !== null)
        Plotly.relayout(this.plotDiv, {
          "shapes[0].visible": false, // First line
          "shapes[1].visible": false, // Second line
          "shapes[2].visible": false, // Rectangle
        });
      else if (this.border1 !== null) Plotly.relayout(this.plotDiv, { "shapes[0].visible": false });

      this.border1 = null;
      this.border2 = null;
    },

    // axis selection
    xAxisSelect(index) {
      this.columnXindex = index;
      this.xAxisSelection = false;
      this.plotDrawn = false;
    },
    yAxisSelect(index) {
      this.columnYindex = index;
      this.yAxisSelection = false;
      this.plotDrawn = false;
    },
    yMultipleAxisSelect(indexes) {
      this.selectedYColumnsIds = indexes;
      this.yMultipleAxisSelection = false;
      this.plotDrawn = false;
    },
    swap() {
      let temp = this.columnYindex;
      this.columnYindex = this.columnXindex;
      this.columnXindex = temp;
      this.drawPlot();
    },
    tagAxisSelect(index) {
      this.columnTagIndex = index;
      this.tagAxisSelection = false;
      this.plotDrawn = false;
    },
    // Filters
    selectDataOnPlot(data) {
      if (!this.filtering) return;

      // Event data format:
      // {
      // points: [{
      //   curveNumber: 1,  // index in data of the trace associated with the selected point
      //   pointNumber: 1,  // index of the selected point
      //   x: 1,      // x value
      //   y: 1,      // y value
      //   data: {/* */},       // ref to the trace as sent to Plotly.newPlot associated with the selected point
      //   fullData: {/* */},   // ref to the trace including all of the default attributes
      //  xaxis: {/* */},   // ref to x-axis object (i.e layout.xaxis) associated with the selected point
      //  yaxis: {/* */}    // ref to y-axis object " "
      // }, {

      /* similarly for other selected points */
      // }]
      // }

      // Get clicked point
      if (data.points.length === 0) return;

      let selectionX = data.points[0].data.x[data.points[0].pointIndex];

      // Update lines
      if (this.border1 === null) {
        // Nothing defined yet, first click
        this.border1 = selectionX;
        this.drawLine(selectionX);
      } else if (this.border2 === null) {
        // Second placement
        this.border2 = selectionX;
        this.drawLine(selectionX);
        this.drawRectangle(this.border1, this.border2);
      } else {
        // Reset
        this.resetShapes();
      }

      if (this.border1 === null && this.border2 === null) {
        // Remove filter
        this.$store.commit("addFilters", {
          filters: [],
          from: {
            widgetType: this.$parent.type,
            widgetName: this.$parent.name,
            widgetIndex: this.index,
          },
          removeExisting: true,
        });

        // Cancel export
        this.$parent.$emit("setExport", null);

        return;
      }

      if (this.border1 === null || this.border2 === null) return;

      // Create a debiai filter
      let colx = this.data.columns[this.columnXindex];

      const min = this.border1 < this.border2 ? this.border1 : this.border2;
      const max = this.border1 > this.border2 ? this.border1 : this.border2;

      const filter = {
        type: "intervals",
        intervals: [{ min, max }],
        columnIndex: colx.index,
      };

      // Store the filters in the DebiAI selection system
      this.$store.commit("addFilters", {
        filters: [filter],
        from: {
          widgetType: this.$parent.type,
          widgetName: this.$parent.name,
          widgetIndex: this.index,
        },
        removeExisting: true,
      });

      // Export boundaries
      // Goal format :
      // {
      //   type: "1Drange",
      //   colX : colName
      //   x : [min, max],
      // }

      const exportData = {
        type: "1Drange",
        colX: colx.label,
        x: [min, max],
      };

      this.$parent.$emit("setExport", exportData);
    },
    filterStarted() {
      this.filtering = true;
      this.$store.commit("sendMessage", {
        title: "info",
        msg: "Click on two samples to select the data between them",
      });
    },
    filterEnded() {
      // Remove the lines on the plot
      this.filtering = false;
    },
    filterCleared() {
      // Remove the lines on the plot
      this.resetShapes();
      this.$parent.$emit("setExport", null);
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.plotDiv);
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
      this.plotDrawn = false;
    },
    selectedData() {
      if (!this.$parent.startFiltering) this.$parent.selectedDataWarning = true;
    },
    redrawRequired(o, n) {
      this.$parent.colorWarning = n;
    },
    multipleYAxis() {
      this.plotDrawn = false;
    },
  },
};
</script>

<style scoped>
#RangeSliderPlot {
  display: flex;
  flex-direction: column;
}

.title h2 {
  margin-left: 10px;
}

#settings {
  display: flex;
  flex-direction: row;
}

/* Controls */
#axisControls {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.otherControls {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.axis {
  margin: 10px;
  margin-bottom: 0px;
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.axis .data {
  flex: 1;
}

.axis .data .value {
  flex: 1;
}

#configButtons {
  margin: 10px;
  justify-content: space-evenly;
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
}

#drawBtn {
  margin: 10px;
  width: 70px;
  margin-left: 0px;
}
</style>
