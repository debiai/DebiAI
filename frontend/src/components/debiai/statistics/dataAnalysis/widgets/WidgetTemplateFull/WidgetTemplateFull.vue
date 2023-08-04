<template>
  <div
    id="WidgetTemplateFull"
    class="dataVisualizationWidget"
  >
    <!-- Column selection modal -->
    <modal
      v-if="colSelection"
      @close="colSelection = false"
    >
      <ColumnSelection
        title="Select a column"
        :data="data"
        :validateRequired="false"
        :colorSelection="true"
        :defaultSelected="[selectedColumnIndex]"
        v-on:cancel="colSelection = false"
        v-on:colSelect="colSelect"
      />
    </modal>

    <!-- Multiple columns selection modal -->
    <modal
      v-if="multipleColSelection"
      @close="multipleColSelection = false"
    >
      <ColumnSelection
        v-if="multipleColSelection"
        title="Select columns"
        :data="data"
        :cancelAvailable="selectedColumnsIndexs.length > 0"
        :colorSelection="true"
        :defaultSelected="selectedColumnsIndexs"
        v-on:cancel="multipleColSelection = false"
        v-on:validate="multipleColsSelected"
      />
    </modal>

    <!-- Controls -->
    <div
      id="settings"
      v-if="settings"
    >
      <!-- Axis btns -->
      <div class="dataGroup">
        <!-- Column selection -->
        <div class="data">
          <div class="name">My column</div>
          <div class="value">
            <Column
              :column="data.columns.find((c) => c.index == selectedColumnIndex)"
              :colorSelection="true"
              v-on:selected="colSelection = true"
            />
          </div>
        </div>
        <!-- Columns selection -->
        <div class="data">
          <div class="name">My columns</div>
          <div class="value">
            <button @click="multipleColSelection = true">
              {{ selectedColumnsIndexs.length }} col selectd
            </button>
          </div>
        </div>
        <div class="dataGroup">
          <!-- Checkbox -->
          <div class="data">
            <div class="name">Checkbox</div>
            <div class="value">
              <input
                type="checkbox"
                :id="'checkbox' + index"
                class="customCbx"
                v-model="checkboxValue"
                style="display: none"
              />
              <label
                :for="'checkbox' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>
          <!-- Selection -->
          <div class="data">
            <div class="name">Selection</div>
            <div class="value">
              <button
                :class="option == 'Opt.1' ? 'radioBtn selected' : 'radioBtn'"
                @click="option = 'Opt.1'"
              >
                Opt.1
              </button>
              <button
                :class="option == 'Opt.2' ? 'radioBtn selected' : 'radioBtn'"
                @click="option = 'Opt.2'"
              >
                Opt.2
              </button>
            </div>
          </div>
          <!-- Input -->
          <div class="data">
            <div class="name">Input</div>
            <div class="value">
              <input
                type="number"
                v-model="value"
                :min="1"
              />
            </div>
          </div>
        </div>
        <!-- Display button -->
        <button @click="display">Display</button>
      </div>
    </div>
    <div
      id="content"
      v-if="displayedData"
    >
      {{ displayedData }}
    </div>
  </div>
</template>

<script>
/**
 * Widget Template with full functionality
 * Select only the required ones
 */

// components
import ColumnSelection from "../../common/ColumnSelection";
import Column from "../../common/Column";

// services
import swal from "sweetalert";

export default {
  components: {
    ColumnSelection,
    Column,
  },
  data() {
    return {
      // Settings
      settings: true,

      // Conf
      selectedColumnIndex: 0,
      selectedColumnsIndexs: [0],
      checkboxValue: true,
      option: "Opt.1",
      value: 0,

      // Other
      colSelection: false,
      multipleColSelection: false,
      displayedData: null,
    };
  },
  props: {
    data: { type: Object, required: true },
    index: { type: String, required: true },
    selectedData: { type: Array, required: true },
  },
  created() {
    // Watching for changes from the parent widget

    // Settings btn
    this.$parent.$on("settings", () => {
      this.settings = !this.settings;
    });

    // Redraw btn
    this.$parent.$on("redraw", () => {
      // We draw something again
      this.display();
    });

    // Filters
    this.$parent.$on("filterStarted", () => {});
    this.$parent.$on("filterEnded", () => {});
    this.$parent.$on("filterCleared", () => {});

    // Exporting data
    // You can emit the following event to export and data with an export method
    this.$parent.$emit("setExport", {
      // The only required field is the export type
      type: "MyDataExportType (bounding box, 1Drange, 2Drange, IdList, csv, ...)",

      // Then you can add any data you want, just make sure the object is a valid JSON
      myData1: 0,
      myData2: "data",
      myData3: [null, null, null],
      // ...
    });
  },
  mounted() {
    // Watch for configuration changes
    this.defConfChangeUpdate();
  },
  methods: {
    // ====== Functions defined in the template ===========
    colSelect(index) {
      this.selectedColumnIndex = index;
      this.colSelection = false;
    },
    multipleColsSelected(indexs) {
      this.selectedColumnsIndexs = indexs;
      this.multipleColSelection = false;
    },
    display() {
      // Do something with the data
      const selectedColumn = this.data.columns[this.selectedColumnIndex];
      const columnData = this.selectedData.map((d) => selectedColumn.values[d]);
      this.displayedData =
        "The first 30 selected values of the chosen column are : " +
        columnData.slice(0, 30).join(", ");

      // We tell the parent that the widget was displayed
      // This will remove some warning and store the current filters
      this.$parent.$emit("drawn");
    },

    // =============== Widget configuration ===============
    /**
     * getConf
     *
     * This optional function can be used to get the configuration of the widget
     * If this function and the setConf function are defined,
     * the blue "save configuration" button will be displayed
     *
     * This function is called when the user clicks on the "save configuration" button
     * it returns the configuration of the widget in an object format
     */
    getConf() {
      let conf = {
        selectedColumn: this.data.columns[this.selectedColumnIndex].label,
        selectedColumns: this.selectedColumnsIndexs.map((index) => this.data.columns[index].label),
        checkboxValue: this.checkboxValue,
        option: this.option,
        value: this.value,
      };

      return conf;
    },
    /**
     * setConf
     *
     * This optional function can be used to load a saved the configuration
     *
     * This function is called when the user create a widget with a saved configuration
     * it takes in input a previously saved configuration
     */
    setConf(conf) {
      if (!conf) return;
      if ("selectedColumn" in conf) {
        let c = this.data.columns.find((c) => c.label == conf.selectedColumn);
        if (c) this.selectedColumnIndex = c.index;
        else {
          // Send a warning to the user
          this.$store.commit("sendMessage", {
            title: "warning",
            msg: "The column " + conf.columnX + " hasn't been found",
          });
        }
      }
      if ("selectedColumns" in conf) {
        this.selectedColumnsIndexs = [];
        conf.selectedColumns.forEach((cLabel) => {
          let c = this.data.columns.find((c) => c.label == cLabel);
          if (c) this.selectedColumnsIndexs.push(c.index);
          else
            this.$store.commit("sendMessage", {
              title: "warning",
              msg: "The column " + cLabel + " hasn't been found",
            });
        });
      }
      if ("checkboxValue" in conf) this.checkboxValue = conf.checkboxValue;
      if ("option" in conf) this.option = conf.option;
      if ("value" in conf) this.value = conf.option;
    },
    /**
     * defConfChangeUpdate
     *
     * This optional function tells the widget that the configuration has changed
     * It will prevent the user to close the widget without saving the configuration
     */
    defConfChangeUpdate() {
      this.$watch(
        (vm) => (
          vm.selectedColumnIndex,
          vm.selectedColumnsIndexs,
          vm.checkboxValue,
          vm.option,
          vm.value,
          Date.now()
        ),
        () => {
          this.$parent.confAsChanged = true;
        }
      );
    },
    /**
     * getConfNameSuggestion
     *
     * This optional function can be used to get the name of the configuration
     */
    getConfNameSuggestion() {
      return "Custom configuration with " + this.data.columns[this.selectedColumnIndex].label;
    },

    // =============== Filtering ===============
    /*
     * If we want to filter the data we can use the following function
     * If this function is defined, the purple "filter" button will be displayed in the widget
     *
     * The filterStarted event is emitted when the filter button is pressed
     * The filterEnded event is emitted when the filter button is pressed again
     * The filterCleared event is emitted when the filter cleared button is pressed
     *
     * See the "created()"
     */
    selectDataOnPlot() {
      if (this.$parent.startFiltering) {
        // The filtering button is active

        let filters = [];

        // Lets filter values on the selected column:
        const selectedValues = [];
        filters.push({
          type: "values",
          columnIndex: this.selectedColumnIndex,
          values: selectedValues,
        });

        // Lets filter intervals on the selected column:
        const min = this.value - 5;
        const max = this.value + 5;
        filters.push({
          type: "intervals",
          columnIndex: this.selectedColumnIndex,
          intervals: [{ min, max }],
        });

        // Apply the filters
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

    // =============== Alerting ===============
    /**
     * The swal component is used to display messages and confirmation
     * Refer to https://www.npmjs.com/package/sweetalert
     */
    sendSwal() {
      swal({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((validate) => {
        if (validate) {
          // Do something
        }
      });
    },

    // =============== Exporting ==============
    exportJsonWithExportMethods() {
      // You can export data with the export methods
      // More info here : https://debiai.irt-systemx.fr/dashboard/dataExport/#exporting-widget-annotations

      // Set the data that your widget can export with the following line:
      this.$parent.$emit("setExport", {
        foo: "bar",
      });

      // You can clear the data that your widget can export with the following line:
      this.$parent.$emit("setExport", null);
    },
    async getImage() {
      // Return the URL of an image representing this widget results
      // If this widget is a plotly widget, you can use the following function:
      // const plotlyToImage = require("@/services/statistics/analysisExport").plotlyToImage;
      // return await plotlyToImage(this.plotlyDiv);
      // Refer to the other widgets to see how to use it.
    },
  },
  computed: {
    coloredColumnIndex() {
      // Return the index of the column that is colored
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
    redrawRequiered() {
      return !(this.currentDrawnColorIndex !== this.coloredColumnIndex);
    },
  },
  watch: {
    selectedData: function () {
      // The selected data have changed
      // We might want to warn the user that an update is required
      this.$parent.selectedDataWarning = true;
      // A redraw btn will be displayed, pressing it will send redraw
      // that can watched and used to redraw a plot (see created())
    },
    coloredColumnIndex: function () {
      // The colored colum has changed
      // We cat tell the parent widget that an update is required
      this.$parent.colorWarning = true;
      // A redraw btn will be displayed, pressing it will send redraw
      // that can watched and used to redraw a plot (see created())
    },
  },
};
</script>

<style scoped>
input {
  width: 100px;
}
</style>
