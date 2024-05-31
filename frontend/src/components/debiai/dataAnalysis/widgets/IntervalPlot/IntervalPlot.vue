<template>
  <div
    id="intervalPlot"
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
        :validColumnsProperties="validXColumnsProperties"
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
        :defaultSelected="[columnYindex]"
        :validColumnsProperties="validYColumnsProperties"
        v-on:cancel="yAxisSelection = false"
        v-on:colSelect="yAxisSelect"
      />
    </modal>
    <modal
      v-if="upperAxisSelection"
      @close="upperAxisSelection = false"
    >
      <ColumnSelection
        title="Select the upper axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="columnUpperIndex === null ? undefined : [columnUpperIndex]"
        :validColumnsProperties="validYColumnsProperties"
        v-on:cancel="upperAxisSelection = false"
        v-on:colSelect="upperAxisSelect"
      />
    </modal>
    <modal
      v-if="lowerAxisSelection"
      @close="lowerAxisSelection = false"
    >
      <ColumnSelection
        title="Select the lower axis"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="columnLowerIndex === null ? undefined : [columnLowerIndex]"
        :validColumnsProperties="validYColumnsProperties"
        v-on:cancel="lowerAxisSelection = false"
        v-on:colSelect="lowerAxisSelect"
      />
    </modal>

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
              <Column
                :column="data.columns.find((c) => c.index == columnXindex)"
                :colorSelection="true"
                v-on:selected="xAxisSelection = true"
              />
            </div>
          </div>
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
        <div id="axisSelectionBot">
          <!-- Lower axis -->
          <div class="data">
            <span class="name">Lower axis</span>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnLowerIndex)"
                :colorSelection="true"
                v-on:selected="lowerAxisSelection = true"
              />
            </div>
          </div>
          <!-- Upper axis -->
          <div class="data">
            <span class="name">Upper axis</span>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnUpperIndex)"
                :colorSelection="true"
                v-on:selected="upperAxisSelection = true"
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
        :disabled="intervalPlotDrawn"
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
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      // === Setting ===
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,
      upperAxisSelection: false,
      lowerAxisSelection: false,
      smooth: true,

      // === Configuration ===
      // Axis
      columnXindex: 0,
      columnYindex: 0,
      columnUpperIndex: 0,
      columnLowerIndex: 0,

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
  },
  mounted() {
    this.divIntervalPlot = document.getElementById("IPDiv" + this.index);
    this.xAxisSelect(0);
    this.yAxisSelect(1);

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
        columnUpper: this.data.columns[this.columnUpperIndex].label,
        columnLower: this.data.columns[this.columnLowerIndex].label,
        smooth: this.smooth,
      };

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
      if ("columnUpper" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnUpper);
        if (c) this.columnUpperIndex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("columnLower" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnLower);
        if (c) this.columnLowerIndex = c.index;
        else
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
        this.data.columns[this.columnXindex].label +
        " / " +
        this.data.columns[this.columnYindex].label;
      return confName;
    },

    // Plot
    updateTraces() {
      let colX = this.data.columns[this.columnXindex];
      let colY = this.data.columns[this.columnYindex];
      let colUpper = this.data.columns[this.columnUpperIndex];
      let colLower = this.data.columns[this.columnLowerIndex];

      // Apply selection
      let valuesX = this.selectedData.map((i) => colX.values[i]);
      let valuesY = this.selectedData.map((i) => colY.values[i]);
      let valuesUpper = this.selectedData.map((i) => colUpper.values[i]);
      let valuesLower = this.selectedData.map((i) => colLower.values[i]);

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
      let color = this.selectedData.map((i, j) =>
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
      this.xAxisSelection = false;
      this.intervalPlotDrawn = false;
    },
    yAxisSelect(index) {
      this.columnYindex = index;
      this.yAxisSelection = false;
      this.intervalPlotDrawn = false;
    },
    upperAxisSelect(index) {
      this.columnUpperIndex = index;
      this.upperAxisSelection = false;
      this.intervalPlotDrawn = false;
    },
    lowerAxisSelect(index) {
      this.columnLowerIndex = index;
      this.lowerAxisSelection = false;
      this.intervalPlotDrawn = false;
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divIntervalPlot);
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
  },
  watch: {
    selectedData() {
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
}
#axisSelection .data .value {
  flex: 1;
}
</style>
