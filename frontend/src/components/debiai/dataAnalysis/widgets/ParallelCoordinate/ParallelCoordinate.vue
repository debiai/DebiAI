<template>
  <div
    id="parCoord"
    class="dataVisualizationWidget"
  >
    <!-- Settings -->
    <ColumnSelection
      v-if="settings"
      title="Select the columns to display in the parallel coordinates plot"
      :data="data"
      :cancelAvailable="selectedColumnsIds.length > 0"
      :colorSelection="true"
      :defaultSelected="selectedColumnsIds"
      :validColumnsProperties="validColumnsProperties"
      v-on:cancel="settings = false"
      v-on:validate="validateSettings"
    />
    <div
      class="plot"
      :id="'PCDiv' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";
// import swal from "sweetalert";

// components
import ColumnSelection from "../../common/ColumnSelection";

// services
import selection from "@/services/statistics/parCoordSelection";
import dataOperations from "@/services/statistics/dataOperations";

export default {
  components: {
    ColumnSelection,
  },
  data() {
    return {
      settings: true,
      selectedColumnsIds: [],
      currentDrawnColorIndex: null,
      validColumnsProperties: {
        types: ["Num", "Bool", "Class"],
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
    this.$parent.$on("filterCleared", this.filterCleared);

    // Select default columns
    this.selectedColumnsIds = this.data.columns
      .filter((c) => c.nbOccurrence > 1 && this.validColumnsProperties.types.includes(c.typeText))
      .map((c) => c.index);
  },
  mounted() {
    this.divParCord = document.getElementById("PCDiv" + this.index);
  },
  methods: {
    // Conf
    getConf() {
      return {
        selectedColumns: this.data.getColumnExistingColumnsLabels(this.selectedColumnsIds),
      };
    },
    setConf(conf, options = {}) {
      if (!conf) return;
      if ("selectedColumns" in conf) {
        this.selectedColumnsIds = [];
        conf.selectedColumns.forEach((cLabel) => {
          const c = this.data.getColumnByLabel(cLabel);
          if (c) this.selectedColumnsIds.push(c.index);
          else if (!options.onStartup)
            this.$store.commit("sendMessage", {
              title: "warning",
              msg: "The column " + cLabel + " hasn't been found",
            });
        });
      }
    },

    // Plot
    drawPlot() {
      // Filter selected columns
      let columns = this.data.getColumnExistingColumns(this.selectedColumnsIds);

      let plotlyColumns = dataOperations.columnsCreation(columns, this.data.selectedData);

      // Color
      let coloredColIndex = this.$store.state.StatisticalAnalysis.coloredColumnIndex;
      let colColor = this.data.getColumn(coloredColIndex);
      this.currentDrawnColorIndex = coloredColIndex;

      let colorscale = "Portland";
      let showscale = false;

      let color;
      if (colColor) {
        if (colColor.type == String) {
          color = this.data.selectedData.map((sId) => colColor.valuesIndex[sId]);
        } else {
          color = this.data.selectedData.map((sId) => colColor.values[sId]);
          showscale = true;
        }
      }

      let trace = {
        type: "parcoords",
        line: {
          color,
          colorscale,
          showscale,
          cmin: colColor ? colColor.min : undefined,
          cmax: colColor ? colColor.max : undefined,
        },
        dimensions: plotlyColumns,
      };

      let layout = {
        margin: {
          l: 80,
          r: 30,
          b: 30,
          t: 50,
        },
      };

      Plotly.newPlot(this.divParCord, [trace], layout, {
        displayModeBar: false,
        responsive: true,
      });

      this.$parent.$emit("drawn");

      // Plot selection update
      this.divParCord.removeListener("plotly_restyle", this.selectDataOnPlot);
      this.divParCord.on("plotly_restyle", this.selectDataOnPlot);

      // black slider color
      var lineList = document.getElementsByClassName("highlight");
      for (var i = 0; i < lineList.length; i++) {
        lineList.item(i).setAttribute("stroke", "black");
        lineList.item(i).setAttribute("stroke-width", "6");
      }
    },

    // Filters
    selectDataOnPlot() {
      if (this.divParCord.data && this.divParCord.data[0]) {
        this.$parent.startFiltering = true;
        let intervals = this.divParCord.data[0].dimensions;

        // Convert plotly intervals to DebiAI filters
        let filters = selection.convertPlotlySelectionsToFilters(this.data, intervals);

        this.$store.commit("addFilters", {
          filters,
          from: {
            widgetType: this.$parent.type,
            widgetName: this.$parent.name,
            widgetIndex: this.index,
          },
          removeExisting: true,
        });
      }
    },
    filterCleared() {
      // clear plotly par cat selections
      // Only if the current widget has some filters drawn
      if (this.divParCord.data && this.divParCord.data[0]) {
        let intervals = this.divParCord.data[0].dimensions;

        // Convert plotly intervals to DebiAI filters
        let filters = selection.convertPlotlySelectionsToFilters(this.data, intervals);

        // This prevent the plotly_restyle event to be triggered
        // and do a death loop with the widget
        if (filters.length == 0) return;

        // Clear plotly selections
        var update = {};
        this.selectedColumnsIds.forEach((colId, i) => {
          update["dimensions[" + i + "].constraintrange"] = null;
        });
        try {
          Plotly.restyle(this.divParCord, update);
        } catch (e) {
          if (e instanceof TypeError) return;
          else console.log(e);
        }
      }
    },

    // Settings
    validateSettings(sci) {
      this.selectedColumnsIds = sci;
      this.settings = false;
      setTimeout(() => {
        this.drawPlot();
      }, 0.1);
    },

    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divParCord);
    },
  },
  computed: {
    redrawRequired() {
      return !(
        this.currentDrawnColorIndex !== this.$store.state.StatisticalAnalysis.coloredColumnIndex &&
        !this.settings &&
        this.selectedColumnsIds.length > 0
      );
    },
    startFiltering() {
      return !this.$parent.startFiltering;
    },
    selectedDataUpdate() {
      return this.data.selectedData;
    },
  },
  watch: {
    redrawRequired(o, n) {
      this.$parent.colorWarning = n;
    },
    selectedDataUpdate() {
      if (!this.settings && !this.$parent.startFiltering) this.$parent.selectedDataWarning = true;
    },
    startFiltering(o, n) {
      if (n) this.selectDataOnPlot();
    },
  },
};
</script>

<style scoped>
#parCoord {
  display: flex;
  flex-direction: column;
}
</style>
