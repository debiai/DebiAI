<template>
  <div
    id="parCat"
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
      v-on:validate="selectColumns"
    />
    <div
      class="plot"
      :id="'PCatDiv' + index"
    ></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { plotlyToImage } from "@/services/statistics/analysisExport";

// components
import ColumnSelection from "../../common/ColumnSelection";
import swal from "sweetalert";

// services
export default {
  components: {
    ColumnSelection,
  },
  data() {
    return {
      settings: true,
      currentDrawnColorIndex: null,

      // Conf
      selectedColumnsIds: [],
      validColumnsProperties: {
        types: ["Num", "Bool", "Class"],
        maxUniqueValues: 20,
        warningMaxUniqueValues: 10,
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

    // Select default columns
    this.selectedColumnsIds = this.data.columns
      .filter(
        (c) =>
          c.nbOccurrence <= this.validColumnsProperties.maxUniqueValues &&
          this.validColumnsProperties.types.includes(c.typeText)
      )
      .map((c) => c.index);
  },
  mounted() {
    this.divParCat = document.getElementById("PCatDiv" + this.index);
  },
  methods: {
    // Conf
    getConf() {
      return {
        selectedColumns: this.data.getColumnExistingColumnsLabels(this.selectedColumnsIds),
      };
    },
    setConf(conf) {
      if (!conf) return;
      if ("selectedColumns" in conf) {
        this.selectedColumnsIds = [];
        conf.selectedColumns.forEach((cLabel) => {
          const c = this.data.getColumnByLabel(cLabel);
          if (c) this.selectedColumnsIds.push(c.index);
          else
            this.$store.commit("sendMessage", {
              title: "warning",
              msg: "The column " + cLabel + " hasn't been found",
            });
        });
      }
    },

    // Plot
    checkPlot() {
      // Color
      let coloredColIndex = this.$store.state.StatisticalAnalysis.coloredColumnIndex;

      let colColor;
      let nbColor;
      if (coloredColIndex !== null) {
        colColor = this.data.getColumn(coloredColIndex);
        nbColor = colColor.nbOccurrence;
      }

      // Get columns
      let selectedColumns = this.selectedColumnsIds
        .map((cIdx) => this.data.getColumn(cIdx))
        .filter((c) => c !== undefined);

      // Check that columns are not too numerous
      if (selectedColumns.some((c) => c.nbOccurrence > 20) || (nbColor && nbColor > 20)) {
        swal({
          title: "Display the Parallel Categories diagram ?",
          text: "You have selected some columns or a color with more than 20 unique values, this will have an impact on the readability of the plot and on the performances.\r \nThe Parallel Coordinates diagram is more suited for the visualizations with a lot of unique values.",
          buttons: true,
          dangerMode: true,
        }).then((validate) => {
          if (validate) this.drawPlot(selectedColumns, colColor);
        });
      } else this.drawPlot(selectedColumns, colColor);
    },
    drawPlot(selectedColumns, colColor) {
      let colorscale = "Portland";
      let showscale = false;
      this.settings = false;

      // Color
      let color;
      if (colColor) {
        if (colColor.type == String) {
          color = this.data.selectedData.map((sId) => colColor.valuesIndex[sId]);
        } else {
          color = this.data.selectedData.map((sId) => colColor.values[sId]);
          showscale = true;
        }
      }
      // Apply selection
      let colWithSelectedSamples = [];
      selectedColumns.forEach((c, i) => {
        colWithSelectedSamples.push({ label: c.label, values: [] });
        this.data.selectedData.map((j) => colWithSelectedSamples[i].values.push(c.values[j]));
      });

      let trace = {
        type: "parcats",
        line: {
          color,
          colorscale,
          showscale,
          cmin: colColor ? colColor.min : undefined,
          cmax: colColor ? colColor.max : undefined,
          // shape: "hspline", TODO : shape check box
        },
        dimensions: colWithSelectedSamples,
      };

      let layout = {
        margin: {
          l: 80,
          r: 30,
          b: 30,
          t: 50,
        },
      };

      Plotly.newPlot(this.divParCat, [trace], layout, {
        displayModeBar: false,
        responsive: true,
      });

      // Set plot selection event
      this.divParCat.removeListener("plotly_click", this.selectDataOnPlot);
      this.divParCat.on("plotly_click", this.selectDataOnPlot);

      this.currentDrawnColorIndex = colColor ? colColor.index : null;
      this.$parent.$emit("drawn");
    },

    selectColumns(selectedColumnsId) {
      this.selectedColumnsIds = selectedColumnsId;
      if (this.clearFiltersAvailable) {
        this.clearFilters();
        setTimeout(this.checkPlot, 200);
      } else this.checkPlot();
    },

    // Filters
    selectDataOnPlot(selection) {
      if (this.$parent.startFiltering && "constraints" in selection) {
        let parCatSelections = selection.constraints;
        let filters = [];
        Object.keys(parCatSelections).forEach((columnIdx) => {
          if (columnIdx === "color") {
            if (!this.selectedColumnsIds.includes(this.currentDrawnColorIndex)) {
              filters.push({
                type: "values",
                columnIndex: this.currentDrawnColorIndex,
                values: [
                  "" +
                    this.data.getColumn(this.currentDrawnColorIndex).uniques[
                      parCatSelections.color
                    ],
                ],
              });
            }
          } else
            filters.push({
              type: "values",
              columnIndex: this.selectedColumnsIds[columnIdx],
              values: ["" + parCatSelections[columnIdx]],
            });
        });
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
    // Export
    async getImage() {
      // Return the URL of an image representing this widget results
      return await plotlyToImage(this.divParCat);
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
  },
};
</script>

<style scoped>
#parCoord {
  display: flex;
  flex-direction: column;
}
</style>
