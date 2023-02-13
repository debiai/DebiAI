<template>
  <div id="pointPlot" class="dataVisualisationWidget">
    <!-- Axis selection Modals -->
    <modal v-if="xAxisSelection" @close="cancelXaxiesSettings">
      <ColumnSelection
        title="Select the X axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        :defaultSelected="[columnXindex]"
        v-on:cancel="cancelXaxiesSettings"
        v-on:colSelect="xAxiesSelect"
      />
    </modal>
    <modal v-if="yAxisSelection" @close="cancelYaxiesSettings">
      <ColumnSelection
        title="Select the Y axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        v-on:cancel="cancelYaxiesSettings"
        :defaultSelected="[columnYindex]"
        v-on:colSelect="yAxiesSelect"
      />
    </modal>
    <modal v-if="zAxisSelection" @close="cancelZaxiesSettings">
      <ColumnSelection
        title="Select the Z axis"
        :data="data"
        :validateRequiered="false"
        :colorSelection="true"
        v-on:cancel="cancelZaxiesSettings"
        :defaultSelected="[columnZindex]"
        v-on:colSelect="zAxiesSelect"
      />
    </modal>

    <div id="settings" v-if="settings">
      <div id="axisControls">
        <!-- Axis btns -->
        <div class="dataGroup axis">
          <div class="data">
            <div class="name">X axis</div>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnXindex)"
                :colorSelection="true"
                v-on:selected="selectXaxis"
              />
            </div>
          </div>
          <div class="data">
            <div class="name">Y axis</div>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnYindex)"
                :colorSelection="true"
                v-on:selected="selectYaxis"
              />
            </div>
          </div>
          <div class="data">
            <div class="name">Z axis</div>
            <div class="value">
              <Column
                :column="data.columns.find((c) => c.index == columnZindex)"
                :colorSelection="true"
                v-on:selected="selectZaxis"
              />
            </div>
          </div>

          <!-- Scatter point opacity control -->
          <div class="dataGroup otherControls">
            <div class="data">
              <div class="name">Scatter point opacity</div>
              <div class="value">
                <div style="flex: 1">
                  Auto :
                  <input type="checkbox" v-model="autoPointOpacity" />
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
                <input type="number" v-model="pointSize" :min="0" :max="100" />
              </div>
            </div>
          </div>
        </div>

        <!-- Draw -->
        <button id="drawBtn" @click="drawPlot" :disabled="plotDrawed">
          Draw
        </button>
      </div>
    </div>

    <div class="plot" :id="'PP3DDiv' + index"></div>
  </div>
</template>

<script>
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
      // Settings
      settings: true,
      xAxisSelection: false,
      yAxisSelection: false,
      zAxisSelection: false,

      // Conf
      columnXindex: 0,
      columnYindex: 0,
      columnZindex: 0,
      pointSize: 2,
      autoPointOpacity: true,
      pointOpacity: 0,

      // Other
      currentDrawedColorIndex: null,
      plotDrawed: false,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required : true },
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
    this.divPointPlot = document.getElementById("PP3DDiv" + this.index);
    if (this.data.columns.length >= 3) {
      this.xAxiesSelect(0);
      this.yAxiesSelect(1);
      this.zAxiesSelect(2);
      this.setPointOpacity();
    }
  },
  methods: {
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.columns[this.columnXindex].label,
        columnY: this.data.columns[this.columnYindex].label,
        columnZ: this.data.columns[this.columnZindex].label,
        pointSize: this.pointSize,
        autoPointOpacity: this.autoPointOpacity,
      };

      if (!this.autoPointOpacity) conf.pointOpacity = this.pointOpacity;

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
      if ("columnZ" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.columnZ);
        if (c) this.columnZindex = c.index;
        else
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnZ + " hasn't been found",
          });
      }
      if ("pointSize" in conf) this.pointSize = conf.pointSize;
      if ("autoPointOpacity" in conf)
        this.autoPointOpacity = conf.autoPointOpacity;
      if ("pointOpacity" in conf) this.pointOpacity = conf.pointOpacity;
    },
    drawPlot() {
      var colX = this.data.columns[this.columnXindex];
      var colY = this.data.columns[this.columnYindex];
      var colZ = this.data.columns[this.columnZindex];

      // Apply selection
      let valuesX = this.selectedData.map((i) => colX.values[i]);
      let valuesY = this.selectedData.map((i) => colY.values[i]);
      let valuesZ = this.selectedData.map((i) => colZ.values[i]);

      // Color
      let colorscale = "Portland";
      let showscale = false;
      let color = 0;
      let cmin;
      let cmax;

      var colColor;
      if (this.coloredColumnIndex !== null) {
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
        title:
          "<b>" +
          colX.label +
          "</b> / <b>" +
          colY.label +
          "</b> / <b>" +
          colZ.label +
          "</b>",
        scene: {
          xaxis: {
            type:
              this.data.columns[this.columnXindex].type == String
                ? "category"
                : "-",
            title: {
              text: colX.label,
            },
          },
          yaxis: {
            type:
              this.data.columns[this.columnYindex].type == String
                ? "category"
                : "-",
            title: {
              text: colY.label,
            },
          },
          zaxis: {
            type:
              this.data.columns[this.columnZindex].type == String
                ? "category"
                : "-",
            title: {
              text: colZ.label,
            },
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

      this.plotDrawed = true;
      this.$parent.selectedDataWarning = false;
      this.currentDrawedColorIndex = this.coloredColumnIndex;
    },

    // axies selection
    selectXaxis() {
      this.xAxisSelection = true;
    },
    selectYaxis() {
      this.yAxisSelection = true;
    },
    selectZaxis() {
      this.zAxisSelection = true;
    },
    cancelXaxiesSettings() {
      this.xAxisSelection = false;
    },
    cancelYaxiesSettings() {
      this.yAxisSelection = false;
    },
    cancelZaxiesSettings() {
      this.zAxisSelection = false;
    },
    xAxiesSelect(index) {
      this.columnXindex = index;
      this.xAxisSelection = false;
      this.plotDrawed = false;
    },
    yAxiesSelect(index) {
      this.columnYindex = index;
      this.yAxisSelection = false;
      this.plotDrawed = false;
    },
    zAxiesSelect(index) {
      this.columnZindex = index;
      this.zAxisSelection = false;
      this.plotDrawed = false;
    },
    setPointOpacity() {
      this.pointOpacity = parseFloat(
        (1 / Math.pow(this.selectedData.length, 0.2)).toFixed(2)
      );
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
    autoPointOpacity: function (newVal) {
      if (newVal) this.setPointOpacity();
    },
    pointOpacity: function () {
      this.plotDrawed = false;
    },
    pointSize: function () {
      this.plotDrawed = false;
    },
    selectedData: function () {
      this.plotDrawed = false;
      this.$parent.selectedDataWarning = true;
      if (this.autoPointOpacity) this.setPointOpacity();
    },
    coloredColumnIndex: function () {
      this.plotDrawed = false;
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

.title h2 {
  margin-left: 10px;
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