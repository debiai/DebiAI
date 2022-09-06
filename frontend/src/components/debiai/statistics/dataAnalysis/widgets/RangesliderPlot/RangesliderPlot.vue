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

    // Widget events
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawPlot);

    // Filtering
    this.border1 = null
    this.border2 = null
    // Filters events
    this.$parent.$on("filterStarted", this.filterStarted);
    this.$parent.$on("filterEnded", this.filterEnded);
    this.$parent.$on("filterCleared", this.filterCleared);
  },
  mounted() {
    this.plotDiv = document.getElementById("rangesliderPlot_" + this.index);

    if (this.data.columns.length >= 2) {
      this.xAxiesSelect(0);
      this.yAxiesSelect(1);
    }

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
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.columnXindex,
          vm.columnYindex,
          Date.now()
        ),
        () => { this.$parent.confAsChanged = true }
      );
    },
    getConfNameSuggestion() {
      let confName =
        this.data.columns[this.columnXindex].label +
        " / " +
        this.data.columns[this.columnYindex].label;
      return confName;
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
        z: valuesX,
        type: 'line',
        name: "line1",
        transforms: [{
          type: 'sort',
          target: 'x',
          order: 'descending'
        }],
      };

      var layout = {
        title: "<b>" + colX.label + "</b> / <b>" + colY.label + "</b>",
        xaxis: {
          rangeslider: true,
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
        selectdirection: 'h',
        margin: {
          l: 50,
          r: 20,
          b: 50,
          t: 50,
        },
        shapes: []
      };

      // Draw
      Plotly.react(this.plotDiv, [line1], layout, {
        displayModeBar: false,
        responsive: true,
      });


      // Deal with point click to select data
      // Goal : place two lines and export bondaries
      this.plotDiv.removeListener("plotly_click", this.selectDataOnPlot);
      this.plotDiv.on('plotly_click', this.selectDataOnPlot);

      this.plotDrawed = true;
      this.$parent.selectedDataWarning = false;
      this.currentDrawedColorIndex = this.coloredColumnIndex;
    },

    drawLine(x) {
      let lineStyle = {
        type: 'line',
        x0: x,
        x1: x,

        y0: 0,
        y1: 1,
        yref: 'paper',

        line: {
          color: 'red',
          width: 2,
          dash: 'dashdot'
        }
      }

      Plotly.relayout(this.plotDiv, { 'shapes[0]': lineStyle })
    },

    resetLines() {
      if (this.border1 !== null && this.border2 !== null) Plotly.relayout(this.plotDiv, { 'shapes[0].visible': false, 'shapes[1].visible': false })
      else if (this.border1 !== null) Plotly.relayout(this.plotDiv, { 'shapes[0].visible': false })

      this.border1 = null
      this.border2 = null
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
      if (data.points.length === 0) return

      let selectionX = data.points[0].data.x[data.points[0].pointIndex]

      // Update lines
      if (this.border1 === null) {
        // Nothing defined yet, first click
        this.border1 = selectionX
        this.drawLine(selectionX)
      } else if (this.border2 === null) {
        // Second placement
        this.border2 = selectionX
        this.drawLine(selectionX)
      } else {
        // Reset
        this.resetLines()
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

        return
      }

      if (this.border1 === null || this.border2 === null) return

      // Create a debiai filter
      let colx = this.data.columns[this.columnXindex];

      const min = this.border1 < this.border2 ? this.border1 : this.border2
      const max = this.border1 > this.border2 ? this.border1 : this.border2

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
      //   origin: "DebiAI",
      //   type: "1Drange",
      //   project_id: ProjectID,
      //   selection_ids: [SelectionID, ...],
      //   colX : colName
      //   x : [min, max],
      // }

      const exportData = {
        origin: "DebiAI",
        type: "1Drange",
        project_id: this.$store.state.ProjectPage.projectId,
        selection_ids: this.$store.state.ProjectPage.selectionsIds,
        colX: colx.label,
        x: [min, max],
      };

      this.$parent.$emit("setExport", exportData);

    },
    filterStarted() {
      this.filtering = true;
    },
    filterEnded() {
      // Remove the lines on the plot
      this.filtering = false;
    },
    filterCleared() {
      // Remove the lines on the plot
      this.resetLines();
      this.$parent.$emit("setExport", null);
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