<template>
  <div
    id="intervalPlot"
    class="dataVisualizationWidget"
  >
    <!-- Plot settings -->
    <div
      id="settings"
      v-if="settings"
      class="dataGroup"
    >
      <!-- Axis selections -->
      <div id="axisSelection">
        <div id="axisSelectionTop">
          <!-- X axis -->
          <div class="data">
            <span class="name">X axis</span>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validXColumnsProperties"
                :defaultColumnIndex="columnXindex"
                title="Select the X axis"
                v-on:selected="xAxisSelect"
              />
            </div>
          </div>
          <!-- Y axis -->
          <div class="data">
            <span class="name">Y axis</span>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validYColumnsProperties"
                :defaultColumnIndex="columnYindex"
                title="Select the Y axis"
                v-on:selected="yAxisSelect"
              />
            </div>
          </div>
        </div>
        <div id="axisSelectionBot">
          <!-- Lower axis -->
          <div class="data">
            <span class="name">Lower axis</span>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validYColumnsProperties"
                :defaultColumnIndex="columnLowerIndex"
                title="Select the lower axis"
                v-on:selected="lowerAxisSelect"
              />
            </div>
          </div>
          <!-- Upper axis -->
          <div class="data">
            <span class="name">Upper axis</span>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validYColumnsProperties"
                :defaultColumnIndex="columnUpperIndex"
                title="Select the upper axis"
                v-on:selected="upperAxisSelect"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Smooth option -->
      <div class="data">
        <span class="name">Smooth</span>
        <div class="value">
          <input
            type="checkbox"
            :id="'smoothCbxIntPlot' + index"
            class="customCbx"
            v-model="smooth"
            style="display: none"
            @click="intervalPlotDrawn = false"
          />
          <label
            :for="'smoothCbxIntPlot' + index"
            class="toggle"
          >
            <span></span>
          </label>
        </div>
      </div>

      <!-- Draw button -->
      <button
        :disabled="intervalPlotDrawn || !canDraw"
        @click="updateTraces"
        class="blue"
      >
        Draw
      </button>
    </div>

    <!-- The plotly plot -->
    <div
      class="plot"
      :id="'IPDiv' + index"
    ></div>
  </div>
</template>

<script>
import { plotlyToImage } from "@/services/statistics/analysisExport";
import Plotly from "plotly.js/dist/plotly";

// components
import ColumnSelectionButton from "../../common/ColumnSelectionButton";

export default {
  components: {
    ColumnSelectionButton,
  },
  data() {
    return {
      // === Setting ===
      settings: true,
      smooth: true,

      // === Configuration ===
      // Axis
      columnXindex: null,
      columnYindex: null,
      columnUpperIndex: null,
      columnLowerIndex: null,

      // === Other ===
      intervalPlotDrawn: false,
      validXColumnsProperties: {
        types: ["Class", "Num"],
      },
      validYColumnsProperties: {
        types: ["Num", "Bool"],
        warningTypes: ["Class"],
      },
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
  },
  created() {
    // Widget setting btn
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      window.dispatchEvent(new Event("resize"));
    });

    // Widget redraw btn
    this.$parent.$on("redraw", this.updateTraces);
  },
  mounted() {
    this.divIntervalPlot = document.getElementById("IPDiv" + this.index);

    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.getColumn(this.columnXindex)?.label,
        columnY: this.data.getColumn(this.columnYindex)?.label,
        columnUpper: this.data.getColumn(this.columnUpperIndex)?.label,
        columnLower: this.data.getColumn(this.columnLowerIndex)?.label,
        smooth: this.smooth,
      };

      return conf;
    },
    setConf(conf, options) {
      if (!conf) return;

      if ("columnX" in conf) {
        const c = this.data.getColumnByLabel(conf.columnX);
        if (c) this.columnXindex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("columnY" in conf) {
        const c = this.data.getColumnByLabel(conf.columnY);
        if (c) this.columnYindex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("columnUpper" in conf) {
        const c = this.data.getColumnByLabel(conf.columnUpper);
        if (c) this.columnUpperIndex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("columnLower" in conf) {
        const c = this.data.getColumnByLabel(conf.columnLower);
        if (c) this.columnLowerIndex = c.index;
        else if (!options?.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      // Boolean operation to prevent string or object
      if ("smooth" in conf) this.smooth = conf.smooth === true;
      this.intervalPlotDrawn = false;
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXindex, vm.columnYindex, vm.columnUpperIndex, vm.columnLowerIndex, Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      let confName =
        this.data.getColumn(this.columnXindex)?.label +
        " / " +
        this.data.getColumn(this.columnYindex)?.label;
      return confName;
    },

    // Plot
    updateTraces() {
      let colX = this.data.getColumn(this.columnXindex);
      let colY = this.data.getColumn(this.columnYindex);
      let colUpper = this.data.getColumn(this.columnUpperIndex);
      let colLower = this.data.getColumn(this.columnLowerIndex);

      if (!colX || !colY || !colUpper || !colLower) return;

      // Apply selection
      let valuesX = this.data.selectedData.map((i) => colX.values[i]);
      let valuesY = this.data.selectedData.map((i) => colY.values[i]);
      let valuesUpper = this.data.selectedData.map((i) => colUpper.values[i]);
      let valuesLower = this.data.selectedData.map((i) => colLower.values[i]);

      // Reorganize data to sort by the x axis
      let data = [];
      for (let i = 0; i < valuesX.length; i++) {
        data.push({
          x: valuesX[i],
          y: valuesY[i],
          upper: valuesUpper[i],
          lower: valuesLower[i],
        });
      }

      // Sort data by x axis
      data.sort((a, b) => a.x - b.x);

      valuesX = data.map((i) => i.x);
      valuesY = data.map((i) => i.y);
      valuesUpper = data.map((i) => i.upper);
      valuesLower = data.map((i) => i.lower);

      // Plot
      let color = this.data.selectedData.map((i, j) =>
        valuesLower[j] <= valuesY[j] && valuesY[j] <= valuesUpper[j] ? "rgb(0,225,0)" : "red"
      );

      let yTrace = {
        name: "Y",
        x: valuesX,
        y: valuesY,
        type: "scatter",
        mode: "markers+lines",
        marker: {
          color: color,
          size: 12,
          line: { color: "black", width: 3 },
        },
        line: {
          shape: this.smooth ? "spline" : "",
          color: "rgb(225, 0, 0)",
          width: 4,
        },
      };
      let upperTrace = {
        name: "upper",
        x: valuesX,
        y: valuesUpper,
        type: "scatter",
        line: {
          shape: this.smooth ? "spline" : "",
          dash: "dot",
          width: 6,
          color: "rgb(30, 30, 250)",
        },
        legendgroup: "interval",
      };
      let lowerTrace = {
        name: "lower",
        x: valuesX,
        y: valuesLower,
        type: "scatter",
        line: {
          shape: this.smooth ? "spline" : "",
          dash: "dot",
          width: 6,
          color: "rgb(30, 30, 250)",
        },
        fill: "tonexty",
        fillcolor: "rgba(0, 0, 250,0.15)",
        hoveron: "points+fills",
        legendgroup: "interval",
      };

      let layout = this.generateLayout({ colX, colY });
      this.drawPlot([upperTrace, lowerTrace, yTrace], layout); // regenerate or generate plot
      this.intervalPlotDrawn = true;
      this.$parent.$emit("drawn");
    },

    // Draw
    generateLayout({ colX, colY }) {
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
      };

      // set y axis label text if string
      if (colY.type == String) {
        layout.yaxis.tickvals = colY.valuesIndexUniques;
        layout.yaxis.ticktext = colY.uniques;
      }

      return layout;
    },
    drawPlot(traces, layout) {
      Plotly.react(this.divIntervalPlot, traces, layout, {
        responsive: true,
        displayModeBar: false,
      });
    },

    // axis selection
    xAxisSelect(index) {
      this.columnXindex = index;
      this.intervalPlotDrawn = false;
    },
    yAxisSelect(index) {
      this.columnYindex = index;
      this.intervalPlotDrawn = false;
    },
    upperAxisSelect(index) {
      this.columnUpperIndex = index;
      this.upperAxisSelection = false;
      this.intervalPlotDrawn = false;
    },
    lowerAxisSelect(index) {
      this.columnLowerIndex = index;
      this.intervalPlotDrawn = false;
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divIntervalPlot);
    },
  },
  computed: {
    canDraw() {
      return (
        this.columnXindex && this.columnYindex && this.columnUpperIndex && this.columnLowerIndex
      );
    },
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    selectedDataUpdate() {
      if (this.intervalPlotDrawn) this.$parent.selectedDataWarning = true;
    },
  },
};
</script>

<style lang="scss" scoped>
#intervalPlot {
  display: flex;
  flex-direction: column;

  #settings {
    display: flex;
    align-items: stretch;
    gap: 10px;
  }
}

/* axisSelection */
#axisSelection {
  flex: 1;
}
#axisSelection #axisSelectionTop {
  display: flex;
}
#axisSelection #axisSelectionBot {
  display: flex;
}
#axisSelection .data {
  flex: 1;
  padding: 2px;
}
#axisSelection .data .value {
  flex: 1;
}
</style>
