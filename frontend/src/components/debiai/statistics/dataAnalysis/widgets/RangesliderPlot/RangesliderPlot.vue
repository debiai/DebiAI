<template>
  <div id="RangesliderPlot" class="dataVisualisationWidget">
    <!-- Axis selection Modals -->
    <modal v-if="xAxisSelection">
      <ColumnSelection title="Select the X axis" :data="data" :validateRequiered="false" :colorSelection="true"
        :defaultSelected="[columnXindex]" v-on:cancel="xAxisSelection = false" v-on:colSelect="xAxiesSelect" />
    </modal>
    <modal v-if="yAxisSelection">
      <ColumnSelection title="Select the Y axis" :data="data" :validateRequiered="false" :colorSelection="true"
        v-on:cancel="yAxisSelection = false" :defaultSelected="[columnYindex]" v-on:colSelect="yAxiesSelect" />
    </modal>

    <div id="settings" v-if="settings">
      <div id="axisControls">
        <!-- Axis btns -->
        <div class="dataGroup axis">
          <div class="data">
            <div class="name">X axis</div>
            <div class="value">
              <Column :column="data.columns.find((c) => c.index == columnXindex)" :colorSelection="true"
                v-on:selected="xAxisSelection = true" />
            </div>
          </div>
          <button class="warning" @click="swap">Swap</button>
          <div class="data">
            <div class="name">Y axis</div>
            <div class="value">
              <Column :column="data.columns.find((c) => c.index == columnYindex)" :colorSelection="true"
                v-on:selected="yAxisSelection = true" />
            </div>
          </div>
        </div>

        <!-- Draw -->
        <button id="drawBtn" @click="drawPlot" :disabled="plotDrawed">
          Draw
        </button>
      </div>

    </div>

    <!-- Plot -->
    <div class="plot" :id="'rangesliderPlot_' + this.index"></div>

  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
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
      columnXindex: 0,
      columnYindex: 0,

      // Other
      currentDrawedColorIndex: null,
      plotDrawed: false,
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
    if (this.data.columns.length >= 2) {
      this.xAxiesSelect(0);
      this.yAxiesSelect(1);
    }
  },
  methods: {
    // Conf
    getConf() {
      let conf = {
        // Axis
        columnX: this.data.columns[this.columnXindex].label,
        columnY: this.data.columns[this.columnYindex].label,
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
    },

    // Display
    drawPlot() {
      var colX = this.data.columns[this.columnXindex];
      var colY = this.data.columns[this.columnYindex];

      // Apply selection
      let valuesX = this.selectedData.map((i) => colX.values[i]);
      let valuesY = this.selectedData.map((i) => colY.values[i]);

      // Color
      // let colorscale = "Portland";
      // let showscale = false;
      // let color = 0;

      // var colColor;
      // if (this.coloredColumnIndex !== null) {
      //   colColor = this.data.columns[this.coloredColumnIndex];
      //   color = this.selectedData.map((i) =>
      //     colColor.type == String ? colColor.valuesIndex[i] : colColor.values[i]
      //   );
      //   // Deal with color if string
      //   // if (colColor.type === String) {
      //   //   cmin = Math.min(...colColor.valuesIndexUniques);
      //   //   cmax = Math.max(...colColor.valuesIndexUniques);
      //   // } else {
      //   //   showscale = true;
      //   //   cmin = colColor.min;
      //   //   cmax = colColor.max;
      //   // }
      // }

      var line1 = {
        x: valuesX,
        y: valuesY,
        mode: "lines",
        name: "line1",
        transforms: [{
          type: 'sort',
          target: 'x',
          order: 'descending'
        }]
      };

      var layout = {
        title:
          "<b>" +
          colX.label +
          "</b> / <b>" +
          colY.label +
          "</b>",
        xaxis: {
          rangeslider: {}
        },
        yaxis: {
          autorange: true,
          type: "linear",
          fixedrange: false,
        },
        scene: {
          xaxis: {
            title: { text: colX.label },
          },
          yaxis: {
            title: {
              text: colY.label,
            },
            autorange: true,
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
      Plotly.react('rangesliderPlot_' + this.index, [line1], layout, {
        displayModeBar: false,
        responsive: true,
      });


      this.plotDrawed = true;
      this.$parent.selectedDataWarning = false;
      this.currentDrawedColorIndex = this.coloredColumnIndex;
    },

    // axies selection
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
    swap() {
      let temp = this.columnYindex;
      this.columnYindex = this.columnXindex;
      this.columnXindex = temp;
      this.drawPlot();
    },
  },
  computed: {
  },
  watch: {
  },
};
</script>

<style scoped>
#RangesliderPlot {
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

#drawBtn {
  margin: 10px;
  width: 80px;
  margin-left: 0px;
  margin-bottom: 0px;
}
</style>