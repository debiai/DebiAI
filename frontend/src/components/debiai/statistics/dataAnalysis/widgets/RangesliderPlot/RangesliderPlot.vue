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

      // Filtering
      border1: null,
      border2: null,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    this.plotDrawed = false;
    this.currentDrawedColorIndex = null;

    // Widget events
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
      if (!this.settings) window.dispatchEvent(new Event("resize"));
    });
    this.$parent.$on("redraw", this.drawPlot);

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

      this.plotDiv.removeListener("plotly_selected", this.selectDataOnPlot);
      this.plotDiv.on("plotly_selected", this.selectDataOnPlot);

      this.plotDiv.on('plotly_click', (data) => {
        if (data.points.length === 0) return
        let selectionX = data.points[0].data.x[data.points[0].pointIndex]

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
      });

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
      Plotly.relayout(this.plotDiv, { 'shapes[0].visible': false, 'shapes[1].visible': false })
      // Plotly.relayout(this.plotDiv, { 'shapes[0].visible': false })

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
    selectDataOnPlot(event) {
      // Some event msgs :
      // {
      //   xaxis.range[0]: "2020-01-19 18:59:16.806",
      //   xaxis.range[1]: "2020-01-20 12:44:37.1109"
      // }
      // {
      //   yaxis.range[0]: 59,
      //   yaxis.range[1]: 44
      // }
      // {
      //   xaxis.range[0]: "2020-01-19 18:59:16.806",
      //   xaxis.range[1]: "2020-01-20 12:44:37.1109"
      //   yaxis.range[0]: 59,
      //   yaxis.range[1]: 44
      // }
      // {
      //   xaxis.autorange: true,
      //   yaxis.autorange: true
      // }

      // The values returned by plotly are not the same as the ones in the data
      // (they can be in between 2 values)

      let str = JSON.stringify(event, null, 4); // (Optional) beautiful indented output.
      console.log(str); // Logs output to dev tools console.
      return
      // // let filters = [];
      // this.$parent.$emit("setExport", null);

      // if ("xaxis.range[0]" in event && "xaxis.range[1]" in event) {
      //   // let min = event["xaxis.range[0]"];
      //   // let max = event["xaxis.range[1]"];

      //   let col = this.data.columns[this.columnXindex];
      //   console.log(col.uniques);

      //   if (col.type == String) {
      //     // Find the closest values
      //     // The value to the right of the range[0]:
      //     // let leftValue = col.uniques.reduce((a, b) => {
      //     //   console.log("reducing left", min, a, b, a > min, a < b, a > min && a < b ? a : b);
      //     //   return a > min && a < b ? a : b;
      //     // });
      //     // let rightValue = col.uniques.reduce((a, b) => {
      //     //   return a < max && a > b ? a : b;
      //     // });

      //     // console.log(leftValue, rightValue);
      //   }
      // }
      // return
      // // Create a debiai filter from a column and a range
      // if (col.type !== String) {
      //   if (absolute) {
      //     return {
      //       type: "intervals",
      //       intervals: [
      //         { min, max },
      //         { max: -min, min: -max },
      //       ],
      //       columnIndex: col.index,
      //     };
      //   } else {
      //     return {
      //       type: "intervals",
      //       intervals: [{ min, max }],
      //       columnIndex: col.index,
      //     };
      //   }
      // } else {
      //   let selectedUniquesValuesIndex = col.valuesIndexUniques.filter(
      //     (v) => v >= min && v <= max
      //   );
      //   let selectedValues = selectedUniquesValuesIndex.map(
      //     (v) => col.uniques[v]
      //   );

      //   // Quick fix for the case of timestamps
      //   if (selectedValues.length == 0) selectedValues = [min, max];

      //   return {
      //     type: "values",
      //     values: selectedValues,
      //     columnIndex: col.index,
      //   };
      // }


      // // Get the filters acording
      // let colx = this.data.columns[this.columnXindex];
      // filters.push(
      //   this.getFilterFromColumn(
      //     colx,
      //     event.range.x[0],
      //     event.range.x[1],
      //     false
      //   )
      // );

      // //   // Exporting the bondaries of the selection
      // //   // We want to export the range of the selection
      // //   // Filter format :
      // //   // [
      // //   //   {
      // //   //     "type": "values",
      // //   //     "values": [
      // //   //       "image-1",
      // //   //       "image-3",
      // //   //       ...
      // //   //     ],
      // //   //     "columnIndex": 0
      // //   //   },
      // //   //   {
      // //   //     "type": "intervals",
      // //   //     "intervals": [
      // //   //       {
      // //   //        max: 19.950596252129472,
      // //   //        min: 6.730834752981263
      // //   //       }
      // //   //     ],
      // //   //     "columnIndex": 1
      // //   //   }
      // //   // ]

      // //   // Goal format :
      // //   // {
      // //   //   origin: "DebiAI",
      // //   //   type: "2Drange",
      // //   //   project_id: ProjectID,
      // //   //   selection_ids: [SelectionID, ...],
      // //   //   colX : colName
      // //   //   colY : colName
      // //   //   x : [min, max],
      // //   //   y : [min, max]
      // //   // }

      // //   if (filters.length == 2) {

      // //     const getRangeFromFilter = (filter) => {
      // //       if (filter.type == "values") return [
      // //         filter.values[0],
      // //         filter.values[filter.values.length - 1]
      // //       ];
      // //       else if (filter.type == "intervals") return [
      // //         filter.intervals[0].min,
      // //         filter.intervals[0].max
      // //       ];
      // //       return null;
      // //     };
      // //     const rangeX = getRangeFromFilter(filters[0]);
      // //     const rangeY = getRangeFromFilter(filters[1]);

      // //     const exportData = {
      // //       origin: "DebiAI",
      // //       type: "2Drange",
      // //       project_id: this.$store.state.ProjectPage.projectId,
      // //       selection_ids: this.$store.state.ProjectPage.selectionsIds,
      // //       colX: colx.label,
      // //       colY: coly.label,
      // //       x: rangeX,
      // //       y: rangeY,
      // //     };

      // //     this.$parent.$emit("setExport", exportData);
      // //   }

      // // }

      // // // Store the filters in the DebiAI selection system
      // // this.$store.commit("addFilters", {
      // //   filters,
      // //   from: {
      // //     widgetType: this.$parent.type,
      // //     widgetName: this.$parent.name,
      // //     widgetIndex: this.index,
      // //   },
      // //   removeExisting: true,
      // // });
    },
    filterStarted() {
      // Set the layout on select mod
      if (this.plotDrawed)
        Plotly.relayout(this.plotDiv, { dragmode: "select" });
    },
    filterEnded() {
      // Remove the layout select mod
      if (this.plotDrawed)
        Plotly.relayout(this.plotDiv, { dragmode: "zoom" });

      this.$parent.$emit("setExport", null);
    },
    filterCleared() {
      // Remove the selection on the plot
      if (this.plotDrawed)
        Plotly.restyle(this.plotDiv, "selectedpoints", null);

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