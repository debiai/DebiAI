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
    <!-- multi Y1 axis selection -->
    <modal
      v-if="y1AxisSelection"
      @close="y1AxisSelection = false"
    >
      <ColumnSelection
        title="Select the columns to display in the first Y axis"
        :data="data"
        :colorSelection="true"
        :defaultSelected="[...selectedY1ColumnsIds]"
        v-on:cancel="y1AxisSelection = false"
        v-on:validate="y1AxisSelect"
      />
    </modal>
    <!-- multi Y2 axis selection -->
    <modal
      v-if="y2AxisSelection"
      @close="y2AxisSelection = false"
    >
      <ColumnSelection
        title="Select the columns to display in the second Y axis"
        :data="data"
        :colorSelection="true"
        :defaultSelected="[...selectedY2ColumnsIds]"
        v-on:cancel="y2AxisSelection = false"
        v-on:validate="y2AxisSelect"
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
          <!-- X axis -->
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
          <!-- Y axis 1 -->
          <div class="data">
            <div class="name">Y1 axis</div>
            <div class="value gapped">
              <!-- Display the selected column -->
              <Column
                v-if="selectedY1ColumnsIds.length == 1"
                :column="data.columns.find((c) => c.index == selectedY1ColumnsIds[0])"
                :colorSelection="true"
                v-on:selected="y1AxisSelection = true"
              />
              <!-- Display the button to select the columns -->
              <button
                v-else
                class="selectColumnsBtn"
                title="Add more columns for the Y axis"
                @click="y1AxisSelection = true"
              >
                {{
                  selectedY1ColumnsIds.length > 0
                    ? `${selectedY1ColumnsIds.length} columns selected`
                    : "+ Select Y1 columns"
                }}
              </button>

              <!-- Group by color -->
              <div
                v-if="coloredColumnIndex !== null"
                class="aligned"
              >
                Group by color
                <input
                  type="checkbox"
                  :id="'gbcY1' + index"
                  class="customCbx"
                  style="display: none"
                  v-model="divideY1PerColor"
                />
                <label
                  :for="'gbcY1' + index"
                  class="toggle"
                >
                  <span></span>
                </label>
              </div>
            </div>
          </div>
          <!-- Y axis 2 -->
          <div class="data">
            <div class="name">Y2 axis</div>
            <div class="value gapped">
              <!-- Display the selected column -->
              <Column
                v-if="selectedY2ColumnsIds.length == 1"
                :column="data.columns.find((c) => c.index == selectedY2ColumnsIds[0])"
                :colorSelection="true"
                v-on:selected="y2AxisSelection = true"
              />

              <!-- Display the button to select the columns -->
              <button
                v-else
                class="selectColumnsBtn"
                title="Add more columns for the Y axis"
                @click="y2AxisSelection = true"
              >
                {{
                  selectedY2ColumnsIds.length > 0
                    ? `${selectedY2ColumnsIds.length} columns selected`
                    : "+ Select Y2 columns"
                }}
              </button>

              <!-- Group by color -->
              <div
                v-if="coloredColumnIndex !== null"
                class="aligned"
              >
                Group by color
                <input
                  type="checkbox"
                  :id="'gbcY2' + index"
                  class="customCbx"
                  style="display: none"
                  v-model="divideY2PerColor"
                />
                <label
                  :for="'gbcY2' + index"
                  class="toggle"
                >
                  <span></span>
                </label>
              </div>
            </div>
          </div>
        </div>
        <div
          class="dataGroup"
          id="configButtons"
        >
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
    />
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
      y1AxisSelection: false,
      y2AxisSelection: false,
      tagAxisSelection: false,

      // Conf
      columnXindex: 0,
      selectedY1ColumnsIds: [],
      selectedY2ColumnsIds: [],
      divideY1PerColor: false,
      divideY2PerColor: false,
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

    if (this.data.columns.length >= 1) this.xAxisSelect(0);

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.columns[this.columnXindex].label,
        columnsY1: this.selectedY1ColumnsIds.map((id) => this.data.columns[id].label),
        columnsY2: this.selectedY2ColumnsIds.map((id) => this.data.columns[id].label),

        // Options
        divideY1PerColor: this.divideY1PerColor,
        divideY2PerColor: this.divideY2PerColor,
      };

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

      // Axis
      if ("columnX" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnX);
        if (c) this.columnXindex = c.index;
        else sendColNotFoundMessage(conf.columnX);
      }
      if ("columnsY1" in conf) {
        this.selectedY1ColumnsIds = [];
        conf.columnsY1.forEach((label) => {
          let c = this.data.columns.find((c) => c.label == label);
          if (c) this.selectedY1ColumnsIds.push(c.index);
          else sendColNotFoundMessage(label);
        });
      }
      if ("columnsY2" in conf) {
        this.selectedY2ColumnsIds = [];
        conf.columnsY2.forEach((label) => {
          let c = this.data.columns.find((c) => c.label == label);
          if (c) this.selectedY2ColumnsIds.push(c.index);
          else sendColNotFoundMessage(label);
        });
      }

      // Options
      if ("divideY1PerColor" in conf) this.divideY1PerColor = conf.divideY1PerColor;
      if ("divideY2PerColor" in conf) this.divideY2PerColor = conf.divideY2PerColor;
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
          vm.selectedY1ColumnsIds,
          vm.selectedY2ColumnsIds,
          vm.divideY1PerColor,
          vm.divideY2PerColor,
          vm.columnTagIndex,
          Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      // X axis
      let confName = this.data.columns[this.columnXindex].label + " / ";

      // Y2 axis
      if (this.selectedY1ColumnsIds.length >= 0) {
        this.selectedY1ColumnsIds.forEach((id) => {
          confName += this.data.columns[id].label + ", ";
        });
        confName = confName.slice(0, -3);
      }

      if (this.divideY1PerColor && this.coloredColumnIndex !== null)
        confName += " / " + this.data.columns[this.coloredColumnIndex].label;

      // Y2 axis
      if (this.selectedY2ColumnsIds.length >= 0) {
        confName += " & ";
        this.selectedY2ColumnsIds.forEach((id) => {
          confName += this.data.columns[id].label + ", ";
        });
        confName = confName.slice(0, -3);
      }

      if (this.divideY2PerColor && this.coloredColumnIndex !== null)
        confName += " / " + this.data.columns[this.coloredColumnIndex].label;

      // Background color
      if (this.columnTagIndex !== null)
        confName += ", Background is " + this.data.columns[this.columnTagIndex].label;

      return confName;
    },

    // Display
    async drawPlot() {
      // Get the X column
      const colX = this.data.columns[this.columnXindex];

      // Get the Y columns
      const colY1 = this.selectedY1ColumnsIds.map((index) => this.data.columns[index]);
      const colY2 = this.selectedY2ColumnsIds.map((index) => this.data.columns[index]);

      // Apply selection filters
      const valuesX = this.selectedData.map((i) => colX.values[i]);
      const valuesY1 = colY1.map((col) => this.selectedData.map((i) => col.values[i]));
      const valuesY2 = colY2.map((col) => this.selectedData.map((i) => col.values[i]));

      // Generate the plot traces
      let tracesY1;
      if (this.divideY1PerColor && this.coloredColumnIndex !== null) {
        // Color
        tracesY1 = await this.generateColorerPlotTraces(valuesX, colY1, valuesY1);
        if (!tracesY1) return; // Canceled
      } else {
        // No color
        tracesY1 = this.generatePlotTraces(valuesX, colY1, valuesY1);
      }

      let tracesY2;
      if (this.divideY2PerColor && this.coloredColumnIndex !== null) {
        // Color
        tracesY2 = await this.generateColorerPlotTraces(valuesX, colY2, valuesY2, "y2");
        if (!tracesY2) return; // Canceled
      } else {
        // No color
        tracesY2 = this.generatePlotTraces(valuesX, colY2, valuesY2, "y2");
      }

      const data = [...tracesY1, ...tracesY2];

      // Create the layout
      const layout = this.generatePlotLayout(colX, colY1, colY2);

      // Draw the plot
      Plotly.react(this.plotDiv, data, layout, { displayModeBar: false, responsive: true });

      // // Deal with background tag color
      // let traces = lines;
      // // const traces = [];
      // const heatmap = this.drawTagHeatmap(valuesX, layout);
      // if (heatmap) {
      //   // Set all the lines axis to y2
      //   lines.forEach((line) => {
      //     line.yaxis = "y2";
      //   });

      //   traces.unshift(heatmap);
      // }

      // Deal with point click to select data
      // Goal : place two lines and export boundaries
      this.plotDiv.removeListener("plotly_click", this.selectDataOnPlot);
      this.plotDiv.on("plotly_click", this.selectDataOnPlot);

      this.plotDrawn = true;
      this.$parent.$emit("drawn");
      this.currentDrawnColorIndex = this.coloredColumnIndex;
    },
    generatePlotTraces(valuesX, colY, valuesY, isY2 = false) {
      if (valuesY.length == 0) return [];
      // Create the Y traces
      const traces = valuesY.map((valuesY, i) => {
        const yAxisColumnLabel = colY[i].label;

        const trace = {
          x: valuesX,
          y: valuesY,
          name: yAxisColumnLabel,
          type: "scatter",
          transforms: [
            {
              type: "sort",
              target: "x",
              order: "descending",
            },
          ],
        };

        if (isY2) {
          trace.yaxis = "y2";
          trace.legendgroup = "Y2";
          trace.line = { dash: "dot" };
        } else {
          trace.legendgroup = "Y1";
        }

        return trace;
      });

      return traces;
    },
    async generateColorerPlotTraces(valuesX, colY, valuesY, isY2 = false) {
      if (valuesY.length == 0) return [];

      const colColor = this.data.columns[this.coloredColumnIndex];

      // Check if the color column is not too big
      if (colColor.uniques.length > 20) {
        // This is a lot, we ask for confirmation
        const rep = await swal({
          title: "Long calculation: do you want to proceed ?",
          text:
            "Range slider plot: You have selected to group data by color\
           with more than 20 uniques values (" +
            colColor.uniques.length +
            " unique values). This will create a lot of lines, this may\
           have an impact on the performances",
          icon: "warning",
          buttons: {
            continue: { text: "continue", className: "warning" },
            cancel: "cancel",
          },
          dangerMode: true,
        });
        if (rep != "continue") return false;
      }

      // Get the colored column values
      const selectedColorsValues =
        colColor.type == String
          ? this.selectedData.map((i) => colColor.valuesIndex[i])
          : this.selectedData.map((i) => colColor.values[i]);
      const selectorUniques =
        colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques;

      // Create the Y traces
      // The traces are a combination of the Y selected axis
      // and the color unique values
      const traces = [];

      valuesY.forEach((valuesY, i) => {
        const yAxisColumnLabel = colY[i].label;
        const groupedValues = dataOperations.groupBy(selectedColorsValues, selectorUniques);

        const colorTraces = groupedValues.map((idValues, j) => {
          const colorX = idValues.map((k) => valuesX[k]);
          const colorY = idValues.map((k) => valuesY[k]);

          const trace = {
            x: colorX,
            y: colorY,
            type: "line",
            name: yAxisColumnLabel + " - " + colColor.uniques[j],
            transforms: [
              {
                type: "sort",
                target: "x",
                order: "descending",
              },
            ],
          };

          if (isY2) {
            trace.yaxis = "y2";
            trace.legendgroup = "Y2 - " + colColor.uniques[j];
            trace.line = { dash: "dot" };
          } else {
            trace.legendgroup = "Y1 - " + colColor.uniques[j];
          }

          return trace;
        });

        traces.push(...colorTraces);
      });

      return traces;
    },
    generatePlotLayout(colX, colY1, colY2) {
      // Create the plot title
      let plotTitle = "<b>" + colX.label + "</b>";

      // Add the Y1 columns to the title
      let colY1Labels = colY1.map((col) => col.label).join(", ");
      if (colY1Labels.length > 50) colY1Labels = colY1Labels.slice(0, 50) + "...";
      if (colY1Labels.length > 0) {
        plotTitle += "/ <b>" + colY1Labels + "</b>";
        if (this.divideY1PerColor && this.coloredColumnIndex !== null)
          plotTitle +=
            " grouped by <b>" + this.data.columns[this.coloredColumnIndex].label + "</b>";
      }

      // Add the Y2 columns to the title
      let colY2Labels = colY2.map((col) => col.label).join(", ");
      if (colY2Labels.length > 50) colY2Labels = colY2Labels.slice(0, 50) + "...";
      if (colY2Labels.length > 0) {
        plotTitle += " & <b>" + colY2Labels + "</b>";
        if (this.divideY1PerColor && this.coloredColumnIndex !== null)
          plotTitle +=
            " grouped by <b>" + this.data.columns[this.coloredColumnIndex].label + "</b>";
      }

      // Add the background color to the title
      if (this.columnTagIndex !== null) {
        const colTag = this.data.columns[this.columnTagIndex];
        plotTitle += " with background color <b>" + colTag.label + "</b>";
      }

      // Create the layout
      const layout = {
        title: plotTitle,
        xaxis: {
          rangeslider: true,
        },
        yaxis: {
          fixedrange: false,
          title: this.selectedY1ColumnsIds.length == 1 ? colY1[0].label : "",
        },
        selectdirection: "h",
        margin: {
          l: 70,
          r: 20,
          b: 50,
          t: 50,
        },
        shapes: [],
      };

      // Add yaxis2 to the layout
      if (this.selectedY2ColumnsIds.length > 0) {
        layout.yaxis2 = {
          title: this.selectedY2ColumnsIds.length == 1 ? colY2[0].label : "",
          fixedrange: false,
          overlaying: "y",
          side: "right",
        };
      }

      return layout;
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

      if (colTag.type === String) heatmap.showscale = false;

      // Complete the layout with an additional yaxis
      layout.yaxis = {
        title: "Ax1",
        side: "right",
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
    y1AxisSelect(indexes) {
      this.selectedY1ColumnsIds = indexes;
      this.y1AxisSelection = false;
      this.plotDrawn = false;
    },
    y2AxisSelect(indexes) {
      this.selectedY2ColumnsIds = indexes;
      this.y2AxisSelection = false;
      this.plotDrawn = false;
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
    selectedY1ColumnsIds() {
      this.plotDrawn = false;
    },
    selectedY2ColumnsIds() {
      this.plotDrawn = false;
    },
  },
};
</script>

<style scoped lang="scss">
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

  .selectColumnsBtn {
    white-space: nowrap;
  }
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
