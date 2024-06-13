<template>
  <div
    id="pointPlot"
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
          <div class="data">
            <div class="name">X axis</div>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validColumnsProperties"
                :defaultColumnIndex="columnXindex"
                title="Select the X axis"
                v-on:selected="xAxisSelect"
              />
            </div>
          </div>
          <div class="data">
            <div class="name">Y axis</div>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validColumnsProperties"
                :defaultColumnIndex="columnYindex"
                title="Select the Y axis"
                v-on:selected="yAxisSelect"
              />
            </div>
          </div>
          <div class="data">
            <div class="name">Z axis</div>
            <div class="value">
              <ColumnSelectionButton
                :data="data"
                :validColumnsProperties="validColumnsProperties"
                :defaultColumnIndex="columnZindex"
                title="Select the Z axis"
                v-on:selected="zAxisSelect"
              />
            </div>
          </div>

          <!-- Scatter point opacity control -->
          <div class="dataGroup otherControls">
            <div class="data">
              <div class="name">Scatter point opacity</div>
              <div class="value">
                Auto:
                <input
                  type="checkbox"
                  v-model="autoPointOpacity"
                />
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
          </div>
        </div>

        <!-- Draw -->
        <button
          id="drawBtn"
          class="blue"
          @click="drawPlot"
          :disabled="!canDraw"
        >
          Draw
        </button>
      </div>
    </div>

    <div
      class="plot"
      :id="'PP3DDiv' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";

// components
import ColumnSelectionButton from "../../common/ColumnSelectionButton";

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
      columnYindex: null,
      columnZindex: null,
      pointSize: 2,
      autoPointOpacity: true,
      pointOpacity: 0,

      // Other
      currentDrawnColorIndex: null,
      plotDrawn: false,

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
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawPlot);
  },
  mounted() {
    this.divPointPlot = document.getElementById("PP3DDiv" + this.index);
    if (this.data.columns.length >= 3) this.setPointOpacity();
  },
  methods: {
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.getColumn(this.columnXindex)?.label,
        columnY: this.data.getColumn(this.columnYindex)?.label,
        columnZ: this.data.getColumn(this.columnZindex)?.label,
        pointSize: this.pointSize,
        autoPointOpacity: this.autoPointOpacity,
      };

      if (!this.autoPointOpacity) conf.pointOpacity = this.pointOpacity;

      return conf;
    },
    setConf(conf, options={}) {
      if (!conf) return;
      if ("columnX" in conf) {
        const c = this.data.getColumnByLabel(conf.columnX);
        if (c) this.columnXindex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
      }
      if ("columnY" in conf) {
        const c = this.data.getColumnByLabel(conf.columnY);
        if (c) this.columnYindex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnY + " hasn't been found",
          });
      }
      if ("columnZ" in conf) {
        const c = this.data.getColumnByLabel(conf.columnZ);
        if (c) this.columnZindex = c.index;
        else if (!options.onStartup)
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnZ + " hasn't been found",
          });
      }
      if ("pointSize" in conf) this.pointSize = conf.pointSize;
      if ("autoPointOpacity" in conf) this.autoPointOpacity = conf.autoPointOpacity;
      if ("pointOpacity" in conf) this.pointOpacity = conf.pointOpacity;
    },
    drawPlot() {
      var colX = this.data.getColumn(this.columnXindex);
      var colY = this.data.getColumn(this.columnYindex);
      var colZ = this.data.getColumn(this.columnZindex);

      if (!colX || !colY || !colZ) return;

      // Apply selection
      let valuesX = this.data.selectedData.map((i) => colX.values[i]);
      let valuesY = this.data.selectedData.map((i) => colY.values[i]);
      let valuesZ = this.data.selectedData.map((i) => colZ.values[i]);

      // Color
      let colorscale = "Portland";
      let showscale = false;
      let color = 0;
      let cmin;
      let cmax;

      var colColor;
      if (this.coloredColumnIndex !== null) {
        colColor = this.data.getColumn(this.coloredColumnIndex);
        color = this.data.selectedData.map((i) =>
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

      var pointData = {
        x: valuesX,
        y: valuesY,
        z: valuesZ,
        name: "Points",
        mode: "markers",
        type: "scatter3d",
        marker: {
          size: this.pointSize,
          cmin,
          cmax,
          opacity: this.pointOpacity,
          color,
          colorscale,
          showscale,
        },
      };

      var layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b> / <b>" + colZ.label + "</b>",
        scene: {
          xaxis: {
            type: colX.type == String ? "category" : "-",
            title: { text: colX.label },
          },
          yaxis: {
            type: colY.type == String ? "category" : "-",
            title: { text: colY.label },
          },
          zaxis: {
            type: colZ.type == String ? "category" : "-",
            title: { text: colZ.label },
          },
        },
        margin: {
          l: 50,
          r: 20,
          b: 50,
          t: 50,
        },
      };

      // Draw
      Plotly.react(this.divPointPlot, [pointData], layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.plotDrawn = true;
      this.$parent.$emit("drawn");
      this.currentDrawnColorIndex = this.coloredColumnIndex;
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
    zAxisSelect(index) {
      this.columnZindex = index;
      this.zAxisSelection = false;
      this.plotDrawn = false;
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
      return this.columnXindex !== null && this.columnYindex !== null && this.columnZindex !== null;
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
    pointOpacity() {
      this.plotDrawn = false;
    },
    pointSize() {
      this.plotDrawn = false;
    },
    selectedDataUpdate() {
      this.plotDrawn = false;
      this.$parent.selectedDataWarning = true;
      if (this.autoPointOpacity) this.setPointOpacity();
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

<style scoped>
#pointPlot {
  display: flex;
  flex-direction: column;
}

.title h2 {
  margin-left: 10px;
}

/* Controls */
#axisControls {
  display: flex;
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
.otherControls input[type="number"] {
  width: 70px;
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
