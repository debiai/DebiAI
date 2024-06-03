<template>
  <div
    id="densityPlot2D"
    class="dataVisualizationWidget"
  >
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
                :column="data.columns.find((c) => c.index == columnXIndex)"
                :colorSelection="true"
                v-on:selected="xAxisSelection = true"
              />
              <!-- AbsX -->
              Absolute value :
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
          <!-- Y axis -->
          <div class="data">
            <div class="name">Y axis</div>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnYIndex)"
                :colorSelection="true"
                v-on:selected="yAxisSelection = true"
              />
              <!-- AbsY -->
              Absolute value :
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
          <!-- Divided per color -->
          <!-- <div
              class="data"
              id="dividePerColor"
              v-if="coloredColumnIndex !== null"
            >
              <div class="name">Divided per color</div>
              <div class="value">
                <input
                  type="checkbox"
                  :id="'dividePerColor' + index"
                  class="customCbx"
                  v-model="dividePerColor"
                  style="display: none"
                />
                <label
                  :for="'dividePerColor' + index"
                  class="toggle"
                >
                  <span></span>
                </label>
              </div>
            </div> -->
        </div>

        <!-- Draw -->
        <button
          id="drawBtn"
          @click="checkPlot"
        >
          Draw
        </button>
      </div>
      <div
        id="colorScaleControl"
        class="dataGroup"
        style="justify-content: space-evenly"
      >
        <!-- Contour number -->
        <div class="data">
          <div class="name">Contour number</div>
          <div class="value">
            <input
              type="number"
              min="1"
              v-model="contourNumber"
              style="width: 70px"
            />
          </div>
        </div>

        <!-- Color scale -->
        <div class="data">
          <div class="name">Color scale</div>
          <div class="value">
            <select v-model="colorScale">
              <option
                v-for="cs in colorScales"
                :key="cs"
                :value="cs"
              >
                {{ cs }}
              </option>
            </select>
          </div>
        </div>

        <!-- Reverse color scale -->
        <div class="data">
          <div class="name">Reverse color scale</div>
          <div class="value">
            <input
              type="checkbox"
              :id="'reverseColorScale' + index"
              class="customCbx"
              v-model="reverseColorScale"
              style="display: none"
            />
            <label
              :for="'reverseColorScale' + index"
              class="toggle"
            >
              <span></span>
            </label>
          </div>
        </div>
      </div>
    </div>

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
        :defaultSelected="[columnXIndex]"
        :validColumnsProperties="validColumnsProperties"
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
        :validColumnsProperties="validColumnsProperties"
        :defaultSelected="[columnYIndex]"
        v-on:cancel="yAxisSelection = false"
        v-on:colSelect="yAxisSelect"
      />
    </modal>

    <div
      class="plot"
      :id="'DensityPlot2D' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";

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
      // Settings
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,

      // Conf
      columnXIndex: 0,
      columnYIndex: 0,
      absX: false,
      absY: false,
      colorScale: "Blues",
      reverseColorScale: true,
      contourNumber: 15,

      // Other
      currentDrawnColorIndex: null,
      colorScales: [
        "Greys",
        "YlGnBu",
        "Greens",
        "YlOrRd", // Best
        "Bluered",
        "RdBu",
        "Reds",
        "Blues",
        "Picnic",
        "Rainbow",
        "Portland",
        "Jet",
        "Hot", // Best 2
        "Blackbody",
        "Earth",
        "Electric",
        "Viridis",
        "Cividis",
      ],

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
    this.divPointPlot = document.getElementById("DensityPlot2D" + this.index);
    if (this.data.columns.length >= 3) {
      this.xAxisSelect(0);
      this.yAxisSelect(1);
      this.setPointOpacity();
    }
  },
  methods: {
    getConf() {
      const conf = {
        // Axis
        columnX: this.data.columns[this.columnXIndex].label,
        columnY: this.data.columns[this.columnYIndex].label,
        absX: this.absX,
        absY: this.absY,
        colorScale: this.colorScale,
        reverseColorScale: this.reverseColorScale,
        contourNumber: this.contourNumber,
      };

      return conf;
    },
    setConf(conf) {
      if (!conf) return;
      if ("columnX" in conf) {
        const c = this.data.columns.find((c) => c.label == conf.columnX);
        if (c) this.columnXIndex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("columnY" in conf) {
        const c = this.data.columns.find((c) => c.label == conf.columnY);
        if (c) this.columnYIndex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("absX" in conf) this.absX = conf.absX;
      if ("absY" in conf) this.absY = conf.absY;
      if ("colorScale" in conf) this.colorScale = conf.colorScale;
      if ("reverseColorScale" in conf) this.reverseColorScale = conf.reverseColorScale;
      if ("contourNumber" in conf) this.contourNumber = conf.contourNumber;

      // Draw plot
      this.checkPlot();
    },
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXIndex,
          vm.columnYIndex,
          vm.absX,
          vm.absY,
          vm.colorScale,
          vm.reverseColorScale,
          vm.contourNumber
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    getConfNameSuggestion() {
      let confName =
        this.data.columns[this.columnXIndex].label +
        (this.absX ? " (abs)" : "") +
        " / " +
        this.data.columns[this.columnYIndex].label +
        (this.absY ? " (abs)" : "");

      return confName;
    },
    // Plot
    checkPlot() {
      this.drawPlot();
    },

    drawPlot() {
      // const starsToDraw = [];

      // Get columns
      const colX = this.data.columns[this.columnXIndex];
      const colY = this.data.columns[this.columnYIndex];

      // Check if columns are valid
      if (
        (colX.type === String && colX.uniques.length > 100) ||
        (colY.type === String && colY.uniques.length > 100)
      ) {
        this.$store.commit("sendMessage", {
          title: "warning",
          msg: "The 2D density plot can't be drawn with a string column with more than 100 uniques values",
        });
        return;
      }

      // const minX = colX.type == Number ? colX.min : 0;
      // const maxX = colX.type == Number ? colX.max : colX.uniques.length - 1;

      // const minY = colY.type == Number ? colY.min : 0;
      // const maxY = colY.type == Number ? colY.max : colY.uniques.length - 1;

      // Apply selection
      let valuesX = this.data.selectedData.map((i) => colX.values[i]);
      let valuesY = this.data.selectedData.map((i) => colY.values[i]);

      // Apply abs
      if (this.absX) valuesX = valuesX.map((v) => Math.abs(v));
      if (this.absY) valuesY = valuesY.map((v) => Math.abs(v));

      // Color
      // let colColor;
      let extraPlotName = "";
      // if (this.coloredColumnIndex !== null && this.dividePerColor) {
      //   colColor = this.data.columns[this.coloredColumnIndex];
      //   extraPlotName = " grouped by " + colColor.label;

      //   let selectedColors;
      //   if (colColor.type == String)
      //     selectedColors = this.data.selectedData.map((i) => colColor.valuesIndex[i]);
      //   else selectedColors = this.data.selectedData.map((i) => colColor.values[i]);

      //   // === Divide bar per color ===
      //   const groupedValues = dataOperations.groupBy(
      //     selectedColors,
      //     colColor.type == String ? colColor.valuesIndexUniques : colColor.uniques
      //   );

      //   groupedValues.forEach((groupDataId, i) => {
      //     const coloredValuesX = groupDataId.map((i) => valuesX[i]);
      //     const coloredValuesY = groupDataId.map((i) => valuesY[i]);

      //     const averageX = coloredValuesX.reduce((a, b) => a + b, 0) / coloredValuesX.length;
      //     const averageY = coloredValuesY.reduce((a, b) => a + b, 0) / coloredValuesY.length;

      //     const stdX = Math.sqrt(
      //       coloredValuesX.map((x) => Math.pow(x - averageX, 2)).reduce((a, b) => a + b, 0) /
      //         coloredValuesX.length
      //     );

      //     const stdY = Math.sqrt(
      //       coloredValuesY.map((y) => Math.pow(y - averageY, 2)).reduce((a, b) => a + b, 0) /
      //         coloredValuesY.length
      //     );

      //     starsToDraw.push({
      //       x: averageX,
      //       y: averageY,
      //       stdX,
      //       stdY,
      //       color: i,
      //       name: colColor.uniques[i],
      //     });
      //   });
      // } else {
      //   const averageX = valuesX.reduce((a, b) => a + b, 0) / valuesX.length;
      //   const averageY = valuesY.reduce((a, b) => a + b, 0) / valuesY.length;
      //   starsToDraw.push({
      //     x: averageX,
      //     y: averageY,
      //     stdX: Math.sqrt(
      //       valuesX.map((x) => Math.pow(x - averageX, 2)).reduce((a, b) => a + b, 0) /
      //         valuesX.length
      //     ),
      //     stdY: Math.sqrt(
      //       valuesY.map((y) => Math.pow(y - averageY, 2)).reduce((a, b) => a + b, 0) /
      //         valuesY.length
      //     ),
      //     color,
      //     name: "All data star",
      //   });
      // }

      // // Draw
      // Plotly.react(this.divPointPlot, traces, layout, {
      //   displayModeBar: false,
      //   responsive: true,
      // });

      // this.$parent.$emit("drawn");
      // this.currentDrawnColorIndex = this.coloredColumnIndex;

      var densityTrace = {
        x: valuesX,
        y: valuesY,
        name: "density",
        ncontours: this.contourNumber,
        reversescale: this.reverseColorScale,
        showscale: false,
        type: "histogram2dcontour",
      };

      var xDensityTrace = {
        x: valuesX,
        name: colX.label + " density",
        marker: { color: "#009ddf" },
        yaxis: "y2",
        type: "histogram",
      };

      var yDensityTrace = {
        y: valuesY,
        name: colY.label + " density",
        marker: { color: "#009ddf" },
        xaxis: "x2",
        type: "histogram",
      };

      const data = [densityTrace, xDensityTrace, yDensityTrace];

      const layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b>" + extraPlotName,
        showlegend: false,
        margin: {
          l: 60,
          r: 20,
          b: 60,
          t: 50,
        },
        hovermode: "closest",
        bargap: 0,
        xaxis: {
          domain: [0, 0.85],
          title: { text: colX.label },
        },
        yaxis: {
          domain: [0, 0.85],
          title: { text: colY.label },
        },
        xaxis2: {
          domain: [0.85, 1],
          showticklabels: false,
        },
        yaxis2: {
          domain: [0.85, 1],
          showticklabels: false,
        },
      };

      if (this.absX) {
        layout.xaxis.title.text += "(absolute value)";
      }
      if (this.absY) {
        layout.yaxis.title.text += "(absolute value)";
      }

      Plotly.react(this.divPointPlot, data, layout, {
        displayModeBar: false,
        responsive: true,
      });

      // Update the plot color scale
      Plotly.restyle(this.divPointPlot, { colorscale: [this.colorScale] }, [0]);
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
    selectedDataUpdate() {
      this.$parent.selectedDataWarning = true;
      if (this.autoPointOpacity) this.setPointOpacity();
    },
  },
};
</script>

<style scoped>
#pointPlot {
  display: flex;
  flex-direction: column;
}

#settings {
  text-align: left;
}

/* Controls */
#axisControls {
  display: flex;
}
#statisticalControls {
  display: flex;
}
#statisticalControls #inputs {
  flex: 1;
  display: flex;
  justify-content: space-evenly;
}
.dataGroup {
  margin-bottom: 0px;
}

.otherControls {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}
.axis {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}
.value {
  flex: 1;
}

#drawBtn {
  margin: 3px;
  width: 80px;
}
</style>
