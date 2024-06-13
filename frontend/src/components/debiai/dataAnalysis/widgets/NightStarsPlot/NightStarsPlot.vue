<template>
  <div
    id="nightStarsPlot"
    class="dataVisualizationWidget"
  >
    <!-- Settings -->
    <div
      id="settings"
      v-if="settings"
    >
      <div id="axisControls">
        <!-- Axis buttons -->
        <!-- X axis -->
        <div class="dataGroup axis">
          <div class="data">
            <div class="name">X axis</div>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validColumnsProperties"
                :defaultColumnIndex="columnXIndex"
                title="Select the X axis"
                v-on:selected="xAxisSelect"
              />
            </div>
          </div>
          <!-- AbsX -->
          <div class="data">
            <div class="name">X absolute value</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'absX' + index"
                class="customCbx"
                v-model="absX"
                style="display: none"
              />
              <label
                :for="'absX' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
        </div>

        <!-- Y axis -->
        <div class="dataGroup axis">
          <div class="data">
            <div class="name">Y axis</div>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validColumnsProperties"
                :defaultColumnIndex="columnYIndex"
                title="Select the Y axis"
                v-on:selected="yAxisSelect"
              />
            </div>
          </div>
          <!-- AbsY -->
          <div class="data">
            <div class="name">Y absolute value</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'absY' + index"
                class="customCbx"
                v-model="absY"
                style="display: none"
              />
              <label
                :for="'absY' + index"
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
          @click="checkPlot"
          class="blue"
          :disabled="!canDraw"
        >
          Draw
        </button>
      </div>
    </div>
    <!-- Plot -->
    <div
      class="plot"
      :id="'NightStarPlot' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";
import swal from "sweetalert";

// components
import ColumnSelectionButton from "../../common/ColumnSelectionButton";

// services
import dataOperations from "@/services/statistics/dataOperations";

export default {
  components: {
    ColumnSelectionButton,
  },
  data() {
    return {
      // Settings
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,

      // Conf
      columnXIndex: null,
      columnYIndex: null,
      dividePerColor: true,
      absX: false,
      absY: false,

      // Other
      currentDrawnColorIndex: null,
      validColumnsProperties: {
        types: ["Num"],
        warningTypes: ["Class"],
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
    this.$parent.$on("redraw", this.checkPlot);
  },
  mounted() {
    this.divPointPlot = document.getElementById("NightStarPlot" + this.index);
    if (this.data.columns.length >= 3) {
      this.setPointOpacity();
    }
  },
  methods: {
    getConf() {
      const conf = {
        // Axis
        columnX: this.data.getColumn(this.columnXIndex)?.label,
        columnY: this.data.getColumn(this.columnYIndex)?.label,
        dividePerColor: this.dividePerColor,
        absX: this.absX,
        absY: this.absY,
      };

      return conf;
    },
    setConf(conf, options = {}) {
      if (!conf) return;
      if ("columnX" in conf) {
        const c = this.data.getColumnByLabel(conf.columnX);
        if (c) this.columnXIndex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("columnY" in conf) {
        const c = this.data.getColumnByLabel(conf.columnY);
        if (c) this.columnYIndex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("dividePerColor" in conf) this.dividePerColor = conf.dividePerColor;
      if ("absX" in conf) this.absX = conf.absX;
      if ("absY" in conf) this.absY = conf.absY;

      // Draw plot
      if (!options.onStartup) this.checkPlot(true);
    },

    // Plot
    checkPlot(failFast = false) {
      const colColor = this.data.columns[this.coloredColumnIndex];

      if (
        this.coloredColumnIndex !== null &&
        this.dividePerColor &&
        colColor.uniques.length > 100
      ) {
        if (failFast) return false;

        swal({
          title: "Long calculation: do you want to proceed ?",
          text: "Night star plot: You have selected more than 100 uniques color values. This may take a while !",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        }).then((validate) => {
          if (validate) this.drawPlot();
        });
      } else {
        this.drawPlot();
      }
    },

    drawPlot() {
      const starsToDraw = [];

      // Get columns
      const colX = this.data.getColumn(this.columnXIndex);
      const colY = this.data.getColumn(this.columnYIndex);
      if (!colX || !colY) return;

      const minX = colX.type == Number ? colX.min : 0;
      const maxX = colX.type == Number ? colX.max : colX.uniques.length - 1;

      const minY = colY.type == Number ? colY.min : 0;
      const maxY = colY.type == Number ? colY.max : colY.uniques.length - 1;

      // Apply selection
      let valuesX = this.data.selectedData.map((i) => colX.values[i]);
      let valuesY = this.data.selectedData.map((i) => colY.values[i]);

      // Apply abs
      if (this.absX) valuesX = valuesX.map((v) => Math.abs(v));
      if (this.absY) valuesY = valuesY.map((v) => Math.abs(v));

      // Color
      const colorscale = "Portland";
      const showscale = false;
      const color = 0;

      let colColor;
      let extraPlotName = "";
      if (this.coloredColumnIndex !== null && this.dividePerColor) {
        colColor = this.data.columns[this.coloredColumnIndex];
        extraPlotName = " grouped by " + colColor.label;

        let selectedColors;
        if (colColor.type == String)
          selectedColors = this.data.selectedData.map((i) => colColor.valuesIndex[i]);
        else selectedColors = this.data.selectedData.map((i) => colColor.values[i]);

        // === Divide bar per color ===
        const groupedValues = dataOperations.groupBy(
          selectedColors,
          colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques
        );

        groupedValues.forEach((groupDataId, i) => {
          const coloredValuesX = groupDataId.map((i) => valuesX[i]);
          const coloredValuesY = groupDataId.map((i) => valuesY[i]);

          const averageX = coloredValuesX.reduce((a, b) => a + b, 0) / coloredValuesX.length;
          const averageY = coloredValuesY.reduce((a, b) => a + b, 0) / coloredValuesY.length;

          const stdX = Math.sqrt(
            coloredValuesX.map((x) => Math.pow(x - averageX, 2)).reduce((a, b) => a + b, 0) /
              coloredValuesX.length
          );

          const stdY = Math.sqrt(
            coloredValuesY.map((y) => Math.pow(y - averageY, 2)).reduce((a, b) => a + b, 0) /
              coloredValuesY.length
          );

          starsToDraw.push({
            x: averageX,
            y: averageY,
            stdX,
            stdY,
            color: i,
            name: colColor.uniques[i],
          });
        });
      } else {
        const averageX = valuesX.reduce((a, b) => a + b, 0) / valuesX.length;
        const averageY = valuesY.reduce((a, b) => a + b, 0) / valuesY.length;
        starsToDraw.push({
          x: averageX,
          y: averageY,
          stdX: Math.sqrt(
            valuesX.map((x) => Math.pow(x - averageX, 2)).reduce((a, b) => a + b, 0) /
              valuesX.length
          ),
          stdY: Math.sqrt(
            valuesY.map((y) => Math.pow(y - averageY, 2)).reduce((a, b) => a + b, 0) /
              valuesY.length
          ),
          color,
          name: "All data star",
        });
      }

      // Convert to plotly format
      const traces = starsToDraw.map((star) => {
        return {
          name: star.name,
          x: [star.x],
          y: [star.y],
          error_x: {
            type: "data",
            array: [star.stdX],
            visible: true,
          },
          error_y: {
            type: "data",
            array: [star.stdY],
            visible: true,
          },
          marker: {
            size: 10,
            color,
            colorscale,
            showscale,
          },
        };
      });

      // Layout
      const layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b>" + extraPlotName,
        xaxis: {
          range: [minX, maxX],
          type: this.data.getColumn(this.columnXIndex)?.type == String ? "category" : "-",
          title: {
            text: colX.label,
          },
        },
        yaxis: {
          range: [minY, maxY],
          type: this.data.getColumn(this.columnYIndex)?.type == String ? "category" : "-",
          title: {
            text: colY.label,
          },
        },
        margin: {
          l: 60,
          r: 20,
          b: 60,
          t: 50,
        },
      };

      if (this.absX) {
        layout.xaxis.title.text += "(absolute value)";
        if (layout.xaxis.range[0] < 0) layout.xaxis.range[0] = 0;
      }
      if (this.absY) {
        layout.yaxis.title.text += "(absolute value)";
        if (layout.yaxis.range[0] < 0) layout.yaxis.range[0] = 0;
      }

      // Draw
      Plotly.react(this.divPointPlot, traces, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.$parent.$emit("drawn");
      this.currentDrawnColorIndex = this.coloredColumnIndex;
    },

    // Axis selection
    xAxisSelect(index) {
      this.columnXIndex = index;
      this.xAxisSelection = false;
    },
    yAxisSelect(index) {
      this.columnYIndex = index;
      this.yAxisSelection = false;
    },
    setPointOpacity() {
      this.pointOpacity = parseFloat((1 / Math.pow(this.data.selectedData.length, 0.2)).toFixed(2));
    },
    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divPointPlot);
    },
  },
  computed: {
    canDraw() {
      return this.columnXIndex !== null && this.columnYIndex !== null;
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
    autoPointOpacity(newVal) {
      if (newVal) this.setPointOpacity();
    },
    pointOpacity() {},
    pointSize() {},
    selectedDataUpdate() {
      this.$parent.selectedDataWarning = true;
      if (this.autoPointOpacity) this.setPointOpacity();
    },
    coloredColumnIndex() {},
    redrawRequired(o, n) {
      this.$parent.colorWarning = n;
    },
  },
};
</script>

<style lang="scss" scoped>
#settings {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Controls */
#axisControls {
  display: flex;

  #inputs {
    flex: 1;
    display: flex;
    justify-content: space-evenly;
  }
}

.axis {
  flex: 1;
  gap: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}
.value {
  flex: 1;
}

#drawBtn {
  width: 80px;
  margin: 3px;
}
</style>
