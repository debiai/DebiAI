<template>
  <div
    id="pointPlot"
    class="dataVisualisationWidget"
  >
    <!-- Modals -->
    <!-- Xcol selection -->
    <modal
      v-if="xAxisSelection"
      @close="xAxisSelection = false"
    >
      <ColumnSelection
        title="Select the X axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        :defaultSelected="[columnXindex]"
        v-on:cancel="xAxisSelection = false"
        v-on:colSelect="xAxiesSelect"
      />
    </modal>
    <!-- Ycol selection -->
    <modal
      v-if="yAxisSelection"
      @close="yAxisSelection = false"
    >
      <ColumnSelection
        title="Select the Y axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        :defaultSelected="[columnYindex]"
        v-on:cancel="yAxisSelection = false"
        v-on:colSelect="yAxiesSelect"
      />
    </modal>
    <!-- Size axis selection -->
    <modal
      v-if="sizeAxisSelection"
      @close="sizeAxisSelection = false"
    >
      <ColumnSelection
        title="Select the point size axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        :defaultSelected="columnSizeIndex === null ? undefined : [columnSizeIndex]"
        v-on:cancel="sizeAxisSelection = false"
        v-on:colSelect="sizeAxiesSelect"
      />
    </modal>
    <!-- Axis range selection -->
    <modal
      @close="axisRangeModal = false"
      v-if="axisRangeModal"
    >
      <AxiesRangeSelection
        :index="index"
        :axisXAuto="axisXAuto"
        :axisYAuto="axisYAuto"
        :axisXMin="axisXMin"
        :axisXMax="axisXMax"
        :axisYMin="axisYMin"
        :axisYMax="axisYMax"
        v-on:cancel="axisRangeModal = false"
        v-on:apply="axisRangeSelect"
      />
    </modal>

    <!-- Settings -->
    <div
      id="settings"
      v-if="settings"
    >
      <!-- Axis selections -->
      <div
        id="axisSelection"
        class="dataGroup"
      >
        <!-- X axis -->
        <div class="data">
          <span class="name">X axis</span>
          <div class="value">
            <Column
              :column="data.columns.find((c) => c.index == columnXindex)"
              :colorSelection="true"
              v-on:selected="xAxisSelection = true"
            />
          </div>
        </div>
        <!-- Swap axis -->
        <button
          class="warning"
          id="swapBtn"
          @click="swap"
        >
          Swap
        </button>
        <!-- Y axis -->
        <div class="data">
          <span class="name">Y axis</span>
          <div class="value">
            <Column
              :column="data.columns.find((c) => c.index == columnYindex)"
              :colorSelection="true"
              v-on:selected="yAxisSelection = true"
            />
          </div>
        </div>
      </div>

      <!-- 2D points & lite plot specific controls -->
      <div id="plotControls">
        <!-- 2d Point Plot Controls -->
        <div
          id="2dPointPlotControls"
          class="dataGroup"
        >
          <!-- Draw -->
          <button
            class="drawBtn"
            @click="pointPlot"
            v-if="!pointPlotDrawed"
          >
            Draw 2D points
          </button>
          <button
            class="drawBtn warning"
            @click="clearPointPlot"
            v-else
          >
            Erase 2D points
          </button>
          <!-- Point size axis -->
          <div class="data">
            <span class="name">Point size axis</span>
            <div
              class="value"
              v-if="columnSizeIndex !== null"
            >
              <Column
                :column="data.columns.find((c) => c.index == columnSizeIndex)"
                :colorSelection="true"
                v-on:selected="sizeAxisSelection = true"
              />
              <button
                class="red"
                @click="
                  columnSizeIndex = null;
                  pointPlotDrawed = false;
                "
              >
                Remove
              </button>
            </div>
            <div
              class="value"
              v-else
            >
              <button
                class="blue"
                @click="sizeAxisSelection = true"
              >
                Select an axis
              </button>
            </div>
          </div>
          <!-- Max point Size -->
          <div
            class="data"
            v-if="columnSizeIndex !== null"
          >
            <span class="name">Max point Size</span>
            <div class="value">
              <input
                type="number"
                v-model="maxPointSize"
                :min="1"
                :step="5"
                @change="pointPlotDrawed = false"
              />
            </div>
          </div>
          <!-- Point opacity -->
          <div class="data">
            <span class="name">Point opacity</span>
            <div class="value">
              <div style="flex: 1">
                Auto :
                <input
                  type="checkbox"
                  v-model="autoPointOpacity"
                />
              </div>

              <span class="name">Opacity</span>
              <div class="value">
                <input
                  type="number"
                  v-if="!autoPointOpacity"
                  v-model="pointOpacity"
                  :step="0.05"
                  :min="0.01"
                  :max="1"
                />
                <div v-else>{{ Math.round(pointOpacity * 1000) / 1000 }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- line Plot Controls -->
        <div
          id="linePlotControls"
          class="dataGroup"
        >
          <!-- Draw -->
          <button
            class="drawBtn orange"
            @click="checkLinePlot"
            v-if="!linePlotDrawed"
          >
            Draw statistics
          </button>
          <button
            v-else
            class="drawBtn warning"
            @click="clearLinePlot"
          >
            Clear statistics
          </button>
          <!-- Bins -->
          <div class="data">
            <span class="name">Bins</span>
            <div class="value">
              <input
                type="number"
                v-model="bins"
                :min="1"
                @change="linePlotDrawed = false"
              />
            </div>
          </div>
          <!-- Display average as bar -->
          <div class="data">
            <span class="name">Display as bar</span>
            <div class="value">
              <input
                type="checkbox"
                :id="'avegareAsBar' + index"
                class="customCbx"
                style="display: none"
                v-model="avegareAsBar"
              />
              <label
                :for="'avegareAsBar' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Display null values -->
          <div
            class="data"
            v-if="!avegareAsBar"
          >
            <span class="name">Display null</span>
            <div class="value">
              <input
                type="checkbox"
                :id="'displayNull' + index"
                class="customCbx"
                style="display: none"
                v-model="displayNull"
                @change="updateTraces()"
              />
              <label
                :for="'displayNull' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- 2D points & lite plot common controls -->
      <div
        id="commonControls"
        class="dataGroup"
      >
        <!-- Groub by color -->
        <div
          class="data"
          v-if="coloredColumnIndex != null"
        >
          <span class="name">Groub by color</span>
          <div class="value">
            <input
              type="checkbox"
              :id="'dividePerColorCbxPointPlot' + index"
              class="customCbx"
              v-model="dividePerColor"
              style="display: none"
            />
            <label
              :for="'dividePerColorCbxPointPlot' + index"
              class="toggle"
            >
              <span></span>
            </label>
          </div>
        </div>
        <!-- Absolute value -->
        <div class="data">
          <span class="name">Absolute value</span>
          <div class="value">
            <input
              type="checkbox"
              :id="'absolute' + index"
              class="customCbx"
              v-model="absolue"
              style="display: none"
            />
            <label
              :for="'absolute' + index"
              class="toggle"
            >
              <span></span>
            </label>
          </div>
        </div>
        <!-- Fixe ranges -->
        <button
          style="margin: 2px"
          class="warning"
          @click="axisRangeModal = !axisRangeModal"
          v-if="!axisXAuto || !axisYAuto"
        >
          Edit the axis ranges
        </button>
        <button
          style="margin: 2px"
          @click="axisRangeModal = !axisRangeModal"
          v-else
        >
          Set the axis ranges
        </button>
      </div>
    </div>

    <!-- The plotly plot -->
    <div
      class="plot"
      :id="'PPDiv' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";

// components
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";
import AxiesRangeSelection from "../../common/AxiesRangeSelection";

// services
import dataOperations from "../../../../../../services/statistics/dataOperations";
import swal from "sweetalert";

export default {
  components: {
    ColumnSelection,
    Column,
    AxiesRangeSelection,
  },
  data() {
    return {
      // === Setting ===
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,
      sizeAxisSelection: false,
      axisRangeModal: false,

      // === Configuration ===
      // Axis
      columnXindex: 0,
      columnYindex: 0,
      // Shared settings
      dividePerColor: true,
      absolue: false,
      // 2d point plot settings
      autoPointOpacity: true,
      pointOpacity: null,
      columnSizeIndex: null,
      maxPointSize: 50,
      // Line plot settings
      avegareAsBar: false,
      displayNull: true,
      bins: 0,
      // Axis range
      axisXAuto: true,
      axisXMin: 0,
      axisXMax: 1,
      axisYAuto: true,
      axisYMin: 0,
      axisYMax: 1,

      // === Other ===
      pointPlotDrawed: false,
      linePlotDrawed: false,
      currentDrawedColorIndex: null,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Widget setting btn
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      window.dispatchEvent(new Event("resize"));
    });

    // Widget redraw btn
    this.$parent.$on("redraw", this.updateTraces);

    // Filters
    this.$parent.$on("filterStarted", this.filterStarted);
    this.$parent.$on("filterEnded", this.filterEnded);
    this.$parent.$on("filterCleared", this.filterCleared);
  },
  mounted() {
    this.divPointPlot = document.getElementById("PPDiv" + this.index);
    this.xAxiesSelect(0);
    this.yAxiesSelect(1);
    this.setPointOpacity();

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.columns[this.columnXindex].label,
        columnY: this.data.columns[this.columnYindex].label,
        // Shared settings
        dividePerColor: this.dividePerColor,
        absolue: this.absolue,
        // 2d point plot settings
        autoPointOpacity: this.autoPointOpacity,
        // Line plot settings
        avegareAsBar: this.avegareAsBar,
        bins: this.bins,
      };

      if (!this.avegareAsBar) conf.displayNull = this.displayNull;
      if (!this.autoPointOpacity) conf.pointOpacity = this.pointOpacity;
      if (this.columnSizeIndex !== null) {
        conf.maxPointSize = this.maxPointSize;
        conf.columnSized = this.data.columns[this.columnSizeIndex].label;
      }

      return conf;
    },
    setConf(conf) {
      if (!conf) return;

      if ("columnX" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnX);
        if (c) this.columnXindex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("columnY" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnY);
        if (c) this.columnYindex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("columnSized" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnSized);
        if (c) this.columnSizeIndex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnSized + " hasn't been found",
          });
      }
      if ("absolue" in conf) this.absolue = conf.absolue;
      if ("autoPointOpacity" in conf) this.autoPointOpacity = conf.autoPointOpacity;
      if ("pointOpacity" in conf) this.pointOpacity = conf.pointOpacity;
      if ("columnSizeIndex" in conf) this.columnSizeIndex = conf.columnSizeIndex;
      if ("maxPointSize" in conf) this.maxPointSize = conf.maxPointSize;
      if ("avegareAsBar" in conf) this.avegareAsBar = conf.avegareAsBar;
      if ("displayNull" in conf) this.displayNull = conf.displayNull;
      if ("bins" in conf) this.bins = conf.bins;
      if ("dividePerColor" in conf) this.dividePerColor = conf.dividePerColor;
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXindex,
          vm.columnYindex,
          vm.dividePerColor,
          vm.absolue,
          vm.autoPointOpacity,
          vm.pointOpacity,
          vm.columnSizeIndex,
          vm.maxPointSize,
          vm.avegareAsBar,
          vm.displayNull,
          vm.bins,
          Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      let confName =
        this.data.columns[this.columnXindex].label +
        " / " +
        this.data.columns[this.columnYindex].label;

      // Add the sized column to the legend name
      if (this.columnSizeIndex !== null)
        confName += " Sized by " + this.data.columns[this.columnSizeIndex].label;

      // Add if y is absolute
      if (this.absolue) confName += " (abs)";

      return confName;
    },

    // Plot
    updateTraces() {
      if (this.pointPlotDrawed) this.pointPlot();
      if (this.linePlotDrawed) this.checkLinePlot();
    },

    // Point plot
    pointPlot() {
      let colX = this.data.columns[this.columnXindex];
      let colY = this.data.columns[this.columnYindex];

      // Apply selection
      let valuesX = this.selectedData.map((i) => colX.values[i]);
      let valuesY;
      if (colY.type == String) valuesY = this.selectedData.map((i) => colY.valuesIndex[i]);
      else valuesY = this.selectedData.map((i) => colY.values[i]);

      // abs checked
      if (this.absolue) valuesY = valuesY.map((val) => Math.abs(val));

      // Color
      let colorscale = "Portland";
      let showscale = false;
      let color = 0;
      let cmin;
      let cmax;

      let colColor;
      if (this.coloredColumnIndex !== null && this.dividePerColor) {
        colColor = this.data.columns[this.coloredColumnIndex];
        color = this.selectedData.map((i) =>
          colColor.type == String ? colColor.valuesIndex[i] : colColor.values[i]
        );
        // Deal with color if string
        if (colColor.type === String) {
          cmin = Math.min(...colColor.valuesIndexUniques);
          cmax = Math.max(...colColor.valuesIndexUniques);
        } else {
          showscale = true;
          cmin = colColor.min;
          cmax = colColor.max;
        }
      }

      // Size
      let size;
      let tmin;
      let tmax;
      const MIN_POINT_SIZE = 3;
      let colSize;
      if (this.columnSizeIndex !== null) {
        colSize = this.data.columns[this.columnSizeIndex];
        size = this.selectedData.map((i) =>
          colSize.type == String ? colSize.valuesIndex[i] : colSize.values[i]
        );
        if (colSize.type === String) {
          tmax = colSize.valuesIndexUniques.length - 1;
        } else {
          tmin = colSize.min;
          tmax = colSize.max;
          size = size.map((s) => s - tmin);
        }
        let ratio = (this.maxPointSize - MIN_POINT_SIZE) / tmax;
        size = size.map((s) => MIN_POINT_SIZE + ratio * s);
      }

      // Assembling the plotly trace
      let pointData = {
        x: valuesX,
        y: valuesY,
        name: "Points",
        mode: "markers",
        type: "scattergl",
        marker: {
          cmin,
          cmax,
          opacity: this.pointOpacity,
          color,
          colorscale,
          showscale,
          size,
        },
      };

      let layout = this.gerenateLayout({ colX, colY, colColor, colSize });

      // Draw
      this.clearPointPlot();
      if (this.linePlotDrawed) {
        Plotly.addTraces(this.divPointPlot, [pointData], 0);
        this.updateLayout(layout);
      } else this.drawPlot([pointData], layout); // regenererate or generate plot

      this.pointPlotDrawed = true;
      this.$parent.$emit("drawed");
      this.currentDrawedColorIndex = this.coloredColumnIndex;
    },
    clearPointPlot() {
      // remove the first trace
      if (!this.linePlotDrawed) Plotly.purge(this.divPointPlot);
      else {
        let tracesToDelete = [];
        this.divPointPlot.data.forEach((trace, i) => {
          if (trace.name === "Points" && trace.mode === "markers") tracesToDelete.push(i);
        });

        Plotly.deleteTraces(this.divPointPlot, tracesToDelete);
      }
      this.pointPlotDrawed = false;
    },

    // Line plot
    checkLinePlot() {
      if (!this.dividePerColor || this.coloredColumnIndex == null) {
        this.linePlot();
        return;
      }

      // Check that the group by color is not to performance intensiv
      let colColor = this.data.columns[this.coloredColumnIndex];

      if (colColor.uniques.length <= 100) {
        this.linePlot();
        return;
      }

      // if it is, ask for confirmation
      swal({
        title: "Long calculation: do you want to proceed ?",
        text: "Point plot: You appear to have selected more than 100 uniques color values. This may take a while !",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((validate) => {
        if (validate) this.linePlot();
      });
    },
    linePlot() {
      let traces = [];
      let colX = this.data.columns[this.columnXindex];
      let valuesX;
      if (colX.type == String) valuesX = this.selectedData.map((i) => colX.valuesIndex[i]);
      else valuesX = this.selectedData.map((i) => colX.values[i]);

      let colY = this.data.columns[this.columnYindex];
      let valuesY;
      if (colY.type == String) valuesY = this.selectedData.map((i) => colY.valuesIndex[i]);
      else valuesY = this.selectedData.map((i) => colY.values[i]);

      // abs checked
      if (this.absolue) valuesY = valuesY.map((val) => Math.abs(val));

      let colColor = this.data.columns[this.coloredColumnIndex];
      if (colColor && this.dividePerColor) {
        // === Divide lines per color ===
        let selectedColorsValues =
          colColor.type == String
            ? this.selectedData.map((i) => colColor.valuesIndex[i])
            : this.selectedData.map((i) => colColor.values[i]);
        let selectorUniques =
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques;

        let groupedValues = dataOperations.groupBy(selectedColorsValues, selectorUniques);

        let fromIn = dataOperations.getMin(valuesX);
        let toIn = dataOperations.getMax(valuesX);

        groupedValues.forEach((idValues, colColorUniqueId) => {
          let stats = dataOperations.getStats(
            idValues.map((i) => valuesX[i]),
            idValues.map((i) => valuesY[i]),
            this.bins - 1,
            {
              fromIn,
              toIn,
              detailed: false,
              displayNull: this.displayNull,
            }
          );

          if (colX.type == String) {
            stats.xSections = stats.xSections.map(
              (v, i) => colX.uniques[Math.floor(i * (colX.uniques.length / this.bins))]
            );
          }

          traces.push({
            name: String(colColor.uniques[colColorUniqueId]),
            x: stats.xSections,
            y: stats.average,
            type: this.avegareAsBar ? "bar" : "scattergl",
            mode: "lines",
            line: {
              // color:
              //   colColor.type == String
              //     ? colColor.valuesIndexUniques[colColorUniqueId]
              //     : colColor.uniques[colColorUniqueId],
              width: 3,
              shape: "spline",
            },
          });
        });
      } else {
        let colY = this.data.columns[this.columnYindex];
        if (colY.type == String) this.valuesY = this.selectedData.map((i) => colY.valuesIndex[i]);

        let stats = dataOperations.getStats(valuesX, valuesY, this.bins - 1, {
          displayNull: this.displayNull,
        });

        if (colX.type == String) {
          stats.xSections = stats.xSections.map(
            (v, i) => colX.uniques[Math.floor(i * (colX.uniques.length / this.bins))]
          );
        }

        traces = [
          {
            x: stats.xSections,
            y: stats.average,
            mode: "lines",
            type: this.avegareAsBar ? "bar" : "scattergl",
            name: "Average",
            line: { color: "red", width: 5, shape: "spline" },
            marker: { color: "#ff5869" },
          },
          {
            x: stats.xSections,
            y: stats.average,
            type: "scattergl",
            mode: "lines",
            name: "STD",
            line: { color: "red", width: 0, shape: "spline" },
            error_y: {
              type: "data",
              array: stats.std,
              visible: true,
            },
            visible: "legendonly",
          },
          {
            x: stats.xSections,
            y: stats.max,
            type: "scattergl",
            mode: "lines",
            name: "Max",
            line: { color: "blue" },
            visible: "legendonly",
          },
          {
            x: stats.xSections,
            y: stats.min,
            mode: "lines",
            type: "scattergl",
            name: "Min",
            line: { color: "blue", shape: "spline" },
            visible: "legendonly",
          },
          {
            x: stats.xSections,
            y: stats.q1,
            mode: "lines",
            type: "scattergl",
            name: "Third decile",
            line: { color: "purle", shape: "spline" },
            visible: "legendonly",
          },
          {
            x: stats.xSections,
            y: stats.q3,
            mode: "lines",
            type: "scattergl",
            name: "First decile",
            line: { color: "purle", shape: "spline" },
            visible: "legendonly",
          },
        ];
      }

      let layout = this.gerenateLayout({ colX, colY, colColor });

      this.clearLinePlot();
      if (this.pointPlotDrawed) {
        Plotly.addTraces(this.divPointPlot, traces);
        this.updateLayout(layout);
      } else this.drawPlot(traces, layout); // regenererate or generate plot

      this.linePlotDrawed = true;
      this.$parent.$emit("drawed");
      this.currentDrawedColorIndex = this.coloredColumnIndex;
    },
    clearLinePlot() {
      // remove the last two traces
      if (!this.pointPlotDrawed) Plotly.purge(this.divPointPlot);
      else {
        let tracesToDelete = [];
        this.divPointPlot.data.forEach((trace, i) => {
          if (trace.name !== "Points" && trace.mode == "lines") tracesToDelete.push(i);
        });

        Plotly.deleteTraces(this.divPointPlot, tracesToDelete);
      }
      this.linePlotDrawed = false;
    },

    // Draw
    gerenateLayout({ colX, colY, colColor, colSize }) {
      let layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b>",
        xaxis: {
          title: {
            text: colX.label,
          },
        },
        yaxis: {
          title: {
            text: colY.label,
          },
        },
        margin: {
          l: 50,
          r: 20,
          b: 50,
          t: 50,
        },

        // Dragmode for the filtering
        dragmode: this.$parent.startFiltering ? "select" : "zoom",
      };

      // Add the color to the legend name
      if (this.dividePerColor && colColor)
        layout.title += " Grouped by <b>" + colColor.label + "</b>";

      // Add the sized column to the legend name
      if (this.columnSizeIndex !== null && colSize)
        layout.title += " Sized by <b>" + colSize.label + "</b>";

      // Add if y is absolute
      if (this.absolue) layout.yaxis.title.text += " (absolute value)";

      // set y axies label text if string
      if (colY.type == String) {
        layout.yaxis.tickvals = colY.valuesIndexUniques;
        layout.yaxis.ticktext = colY.uniques;
      }

      return layout;
    },
    updateLayout(layout) {
      Plotly.relayout(this.divPointPlot, {
        title: layout.title,
        "yaxis.title.text": layout.yaxis.title.text,
      });
    },
    drawPlot(traces, layout) {
      // Apply range if needed
      if (!this.axisXAuto) layout.xaxis.range = [this.axisXMin, this.axisXMax];
      if (!this.axisYAuto) layout.yaxis.range = [this.axisYMin, this.axisYMax];

      // Draw the plot
      Plotly.react(this.divPointPlot, traces, layout, {
        responsive: true,
        displayModeBar: false,
      });

      // Set zoom events for the data filtering
      this.divPointPlot.removeListener("plotly_selected", this.selectDataOnPlot);
      this.divPointPlot.on("plotly_selected", this.selectDataOnPlot);
    },

    // Filters
    selectDataOnPlot(event) {
      if (!this.$parent.startFiltering) return;

      // Clear the export
      this.$parent.$emit("setExport", null);

      // An event msg :
      // {
      //   points: ...,
      //   selections: [{
      //     x0: ...,
      //     x1: ...,
      //     y0: ...,
      //     y1: ...,
      //     ...
      //  }] // One per rectangles
      //  range: { x : [min, max], y : [min, max] }
      // }
      // or undefined (single click or double click out)
      // or { points: [], selections: [] } (double click in)
      if (!event || !event.selections || event.selections.length === 0) {
        this.$store.commit("addFilters", {
          filters: [],
          from: {
            widgetType: this.$parent.type,
            widgetName: this.$parent.name,
            widgetIndex: this.index,
          },
          removeExisting: true,
        });
        this.$parent.$emit("setExport", null);
        Plotly.relayout(this.divPointPlot, { shapes: [] }); // Rectangle
        return;
      }

      // Create the filters
      let colx = this.data.columns[this.columnXindex];
      let coly = this.data.columns[this.columnYindex];

      // Create the first filter
      const selections = event.selections;
      const filters = [
        this.getFilterFromColumn(colx, selections[0].x0, selections[0].x1, false),
        this.getFilterFromColumn(coly, selections[0].y1, selections[0].y0, this.absolue),
      ];

      // // Create the other filters
      // We are not doing this anymore because it is not possible make filters union in DebiAI
      // TODO : make it possible to make filters union in DebiAI
      // for (let i = 1; i < selections.length; i++) {
      //   const nextFiltersx = this.getFilterFromColumn(
      //     colx,
      //     selections[i].x0,
      //     selections[0].x1,
      //     false
      //   );
      //   const nextFiltersy = this.getFilterFromColumn(
      //     coly,
      //     selections[i].y1,
      //     selections[0].y0,
      //     this.absolue
      //   );

      //   if (filters[0].intervals) filters[0].intervals.push(nextFiltersx.intervals[0]);
      //   if (filters[0].values) filters[0].values = filters[0].values.concat(nextFiltersx.values);
      //   if (filters[1].intervals) filters[1].intervals.push(nextFiltersy.intervals[0]);
      //   if (filters[1].values) filters[1].values = filters[1].values.concat(nextFiltersy.values);
      // }

      // Display a rectangle on the plot
      // This doesn't work , it triggers a recursive loop, I think that relayout triggers a plotly_selected event
      // const recStyle = {
      //   type: "rect",
      //   x0: selections[0].x0,
      //   x1: selections[0].x1,
      //   y0: selections[0].y0,
      //   y1: selections[0].y1,

      //   fillcolor: "none",
      //   line: { width: 2, color: "red" },
      // };

      // console.log("update");
      // Plotly.relayout(this.divPointPlot, { shapes: [recStyle] });

      // Store the filters in the DebiAI selection system
      this.$store.commit("addFilters", {
        filters,
        from: {
          widgetType: this.$parent.type,
          widgetName: this.$parent.name,
          widgetIndex: this.index,
        },
        removeExisting: true,
      });

      // Exporting the bondaries of the selections with the export feature
      // Exporting only the first selection TODO : add all the selections
      // Goal format :
      // {
      //   type: "2Drange",
      //   colX : colName
      //   colY : colName
      //   x : [min, max],
      //   y : [min, max]
      // }

      const getRangeFromFilter = (filter) => {
        if (filter.type == "values")
          return [filter.values[0], filter.values[filter.values.length - 1]];
        else if (filter.type == "intervals")
          return [filter.intervals[0].min, filter.intervals[0].max];
        return null;
      };
      const rangeX = getRangeFromFilter(filters[0]);
      const rangeY = getRangeFromFilter(filters[1]);

      const exportData = {
        type: "2Drange",
        colX: colx.label,
        colY: coly.label,
        x: rangeX,
        y: rangeY,
      };

      this.$parent.$emit("setExport", exportData);
    },
    getFilterFromColumn(col, min, max, absolute) {
      // Create a debiai filter from a column and a range

      // Filter format :
      // [
      //   {
      //     "type": "values",
      //     "values": [
      //       "image-1",
      //       "image-3",
      //       ...
      //     ],
      //     "columnIndex": 0
      //   },
      //   {
      //     "type": "intervals",
      //     "intervals": [
      //       {
      //        max: 19.950596252129472,
      //        min: 6.730834752981263
      //       }
      //     ],
      //     "columnIndex": 1
      //   }
      // ]

      // Fix the fact that the min and max may be inverted
      if (min > max) {
        let tmp = min;
        min = max;
        max = tmp;
      }

      if (col.type !== String) {
        if (absolute) {
          return {
            type: "intervals",
            intervals: [
              { min, max },
              { max: -min, min: -max },
            ],
            columnIndex: col.index,
          };
        } else {
          return {
            type: "intervals",
            intervals: [{ min, max }],
            columnIndex: col.index,
          };
        }
      } else {
        let selectedUniquesValuesIndex = col.valuesIndexUniques.filter((v) => v >= min && v <= max);
        let selectedValues = selectedUniquesValuesIndex.map((v) => col.uniques[v]);

        // Quick fix for the case of timestamps
        if (selectedValues.length == 0) selectedValues = [min, max];

        return {
          type: "values",
          values: selectedValues,
          columnIndex: col.index,
        };
      }
    },
    filterStarted() {
      // Set the layout on select mod
      if (this.pointPlotDrawed || this.linePlotDrawed)
        Plotly.relayout(this.divPointPlot, { dragmode: "select" });
    },
    filterEnded() {
      // Remove the layout select mod
      if (this.pointPlotDrawed || this.linePlotDrawed)
        Plotly.relayout(this.divPointPlot, { dragmode: "zoom" });

      this.$parent.$emit("setExport", null);
    },
    filterCleared() {
      // Remove the selection on the plot
      if (this.pointPlotDrawed || this.linePlotDrawed)
        Plotly.restyle(this.divPointPlot, "selectedpoints", null);

      this.$parent.$emit("setExport", null);
    },

    // axies selection
    xAxiesSelect(index) {
      this.columnXindex = index;
      this.xAxisSelection = false;
      this.pointPlotDrawed = false;
      this.linePlotDrawed = false;
      this.setBins();
    },
    yAxiesSelect(index) {
      this.columnYindex = index;
      this.yAxisSelection = false;
      this.pointPlotDrawed = false;
      this.linePlotDrawed = false;
    },
    sizeAxiesSelect(index) {
      this.columnSizeIndex = index;
      this.sizeAxisSelection = false;
      this.pointPlotDrawed = false;
    },
    swap() {
      let memoryLinePlotDrawed = this.linePlotDrawed;
      let temp = this.columnYindex;
      this.columnYindex = this.columnXindex;
      this.columnXindex = temp;
      this.setBins();

      this.linePlotDrawed = memoryLinePlotDrawed;
      this.updateTraces();
    },
    setBins() {
      let colX = this.data.columns[this.columnXindex];
      if (colX.type == String) this.bins = Math.min(colX.nbOccu, 300);
      else this.bins = Math.min(colX.nbOccu, 30);
      this.linePlotDrawed = false;
    },
    setPointOpacity() {
      this.pointOpacity = parseFloat((1 / Math.pow(this.selectedData.length, 0.2)).toFixed(2));
    },
    axisRangeSelect({ axisXAuto, axisXMin, axisXMax, axisYAuto, axisYMin, axisYMax }) {
      this.axisRangeModal = false;
      this.pointPlotDrawed = false;
      this.linePlotDrawed = false;
      this.axisXAuto = axisXAuto;
      this.axisXMin = axisXMin;
      this.axisXMax = axisXMax;
      this.axisYAuto = axisYAuto;
      this.axisYMin = axisYMin;
      this.axisYMax = axisYMax;
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.SatisticalAnasysis.coloredColumnIndex;
    },
    redrawRequiered() {
      return !(this.currentDrawedColorIndex !== this.coloredColumnIndex);
    },
  },
  watch: {
    dividePerColor: function () {
      this.updateTraces();
    },
    autoPointOpacity: function (newVal) {
      if (newVal) this.setPointOpacity();
    },
    pointOpacity: function () {
      this.pointPlotDrawed = false;
    },
    absolue: function () {
      this.updateTraces();
    },
    displayNull: function () {
      if (this.linePlotDrawed) this.checkLinePlot();
    },
    avegareAsBar: function () {
      if (this.linePlotDrawed) this.checkLinePlot();
    },
    selectedData: function () {
      if (!this.$parent.startFiltering && (this.pointPlotDrawed || this.linePlotDrawed))
        this.$parent.selectedDataWarning = true;
    },
    redrawRequiered(o, n) {
      this.$parent.colorWarning = n;
    },
  },
};
</script>

<style scoped>
#pointPlot {
  display: flex;
  flex-direction: column;
}

/* axisSelection */
#axisSelection {
  flex-wrap: wrap;
}

#axisSelection .data {
  flex: 1;
}

#axisSelection .data .value {
  flex: 1;
}

#axisSelection #swapBtn {
  margin: 0 10px 0 10px;
}

/* plotControls */
#plotControls {
  display: flex;
}

#plotControls .dataGroup {
  flex: 1;
  flex-direction: column;
  justify-content: flex-start;
}

#plotControls .drawBtn {
  height: 40px;
}

#plotControls .data {
  margin-top: 3px;
  min-height: 35px;
}

#plotControls .data .name {
  flex: 0.4;
}

#plotControls .data .value {
  flex: 1;
}

/* commonControls */
#commonControls {
  justify-content: space-evenly;
}

#commonControls .data {
  min-height: 35px;
}
</style>
