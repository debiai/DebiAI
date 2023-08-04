<template>
  <div
    id="nightStarsPlot"
    class="dataVisualizationWidget"
  >
    <!-- Settings -->
    <modal
      v-if="settings"
      @close="settings = false"
    >
      <div id="settings">
        <h3>Night stars plot settings</h3>
        <div id="axisControls">
          <!-- Axis buttons -->
          <div class="dataGroup axis">
            <div class="data">
              <div class="name">X axis</div>
              <div class="value">
                <Column
                  :column="data.columns.find((c) => c.index == columnXIndex)"
                  :colorSelection="true"
                  v-on:selected="xAxisSelection = true"
                />
              </div>
            </div>
            <div class="data">
              <div class="name">Y axis</div>
              <div class="value">
                <Column
                  :column="data.columns.find((c) => c.index == columnYIndex)"
                  :colorSelection="true"
                  v-on:selected="yAxisSelection = true"
                />
              </div>
            </div>

            <!-- Scatter point opacity control -->
            <!-- <div class="dataGroup otherControls">
            <div class="data">
              <div class="name">Scatter point opacity</div>
              <div class="value">
                <div style="flex: 1">
                  Auto :
                  <input
                    type="checkbox"
                    v-model="autoPointOpacity"
                  />
                </div>

                <div class="name">opacity :</div>
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
            <div class="data">
              <div class="name">Point size</div>
              <div class="value">
                <input
                  type="number"
                  v-model="pointSize"
                  :min="0"
                  :max="100"
                />
              </div>
            </div>
          </div> -->
          </div>

          <!-- Draw -->
          <button
            id="drawBtn"
            @click="drawPlot"
            :disabled="plotDrawn"
          >
            Draw
          </button>
        </div>
      </div>
    </modal>

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
        :defaultSelected="[columnYIndex]"
        v-on:colSelect="yAxisSelect"
      />
    </modal>

    <div
      class="plot"
      :id="'NightStarPlot' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";

// components
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";

// services
import dataOperations from "@/services/statistics/dataOperations";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      // Settings
      settings: false,
      xAxisSelection: false,
      yAxisSelection: false,

      // Conf
      columnXIndex: 0,
      columnYIndex: 0,
      pointSize: 2,
      autoPointOpacity: true,
      pointOpacity: 0,

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
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawPlot);
  },
  mounted() {
    this.divPointPlot = document.getElementById("NightStarPlot" + this.index);
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
        pointSize: this.pointSize,
        autoPointOpacity: this.autoPointOpacity,
      };

      if (!this.autoPointOpacity) conf.pointOpacity = this.pointOpacity;

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
      if ("pointSize" in conf) this.pointSize = conf.pointSize;
      if ("autoPointOpacity" in conf) this.autoPointOpacity = conf.autoPointOpacity;
      if ("pointOpacity" in conf) this.pointOpacity = conf.pointOpacity;
    },
    drawPlot() {
      const starsToDraw = [];

      // Get columns
      const colX = this.data.columns[this.columnXIndex];
      const colY = this.data.columns[this.columnYIndex];

      const minX = colX.type == Number ? colX.min : 0;
      const maxX = colX.type == Number ? colX.max : colX.uniques.length - 1;

      const minY = colY.type == Number ? colY.min : 0;
      const maxY = colY.type == Number ? colY.max : colY.uniques.length - 1;

      // Apply selection
      const valuesX = this.selectedData.map((i) => colX.values[i]);
      const valuesY = this.selectedData.map((i) => colY.values[i]);

      // Color
      const colorscale = "Portland";
      const showscale = false;
      const color = 0;

      let colColor;
      if (this.coloredColumnIndex !== null) {
        colColor = this.data.columns[this.coloredColumnIndex];

        let selectedColors;
        if (colColor.type == String)
          selectedColors = this.selectedData.map((i) => colColor.valuesIndex[i]);
        else selectedColors = this.selectedData.map((i) => colColor.values[i]);

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
        starsToDraw.push({
          x: valuesX.reduce((a, b) => a + b, 0) / valuesX.length,
          y: valuesY.reduce((a, b) => a + b, 0) / valuesY.length,
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
      const traces = [];

      starsToDraw.forEach((star) => {
        console.log(star.name);
        const trace = {
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

        traces.push(trace);
      });

      const layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b>",
        xaxis: {
          range: [minX, maxX],
          type: this.data.columns[this.columnXIndex].type == String ? "category" : "-",
          title: {
            text: colX.label,
          },
        },
        yaxis: {
          range: [minY, maxY],
          type: this.data.columns[this.columnYIndex].type == String ? "category" : "-",
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

      // Draw
      Plotly.react(this.divPointPlot, traces, layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.plotDrawn = true;
      this.$parent.$emit("drawn");
      this.currentDrawnColorIndex = this.coloredColumnIndex;
      this.settings = false;
    },

    // Axis selection
    xAxisSelect(index) {
      this.columnXIndex = index;
      this.xAxisSelection = false;
      this.plotDrawn = false;
    },
    yAxisSelect(index) {
      this.columnYIndex = index;
      this.yAxisSelection = false;
      this.plotDrawn = false;
    },
    setPointOpacity() {
      this.pointOpacity = parseFloat((1 / Math.pow(this.selectedData.length, 0.2)).toFixed(2));
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
  },
  watch: {
    autoPointOpacity: function (newVal) {
      if (newVal) this.setPointOpacity();
    },
    pointOpacity: function () {
      this.plotDrawn = false;
    },
    pointSize: function () {
      this.plotDrawn = false;
    },
    selectedData: function () {
      this.plotDrawn = false;
      this.$parent.selectedDataWarning = true;
      if (this.autoPointOpacity) this.setPointOpacity();
    },
    coloredColumnIndex: function () {
      this.plotDrawn = false;
    },
    redrawRequired(o, n) {
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

.title h2 {
  margin-left: 10px;
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
  margin: 10px;
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
  margin: 10px;
  width: 80px;
  margin-left: 0px;
  margin-bottom: 0px;
}
</style>
