<template>
  <div class="card">
    <!-- Wigdet conf load or save modal -->
    <modal v-if="confSettings">
      <WidgetConfPannel :widgetTitle="title" :widgetName="name" :confToSave="confToSave"
        :suggestedConfName="suggestedConfName" @cancel="confSettings = false" @saved="confSaved" @confSelected="setConf"
        @setWidgetName="setName" />
    </modal>
    <!-- Export data modal -->
    <modal v-if="exportModal">
      <DataExportMenu :dataToExport="exportData" @exported="exportModal = false" @cancel="exportModal = false" />
    </modal>

    <!-- Widget -->
    <div id="widgetHeader" :class="
      'title grid-stack-item-content ' + (startFiltering ? 'purple' : '')
    ">
      <!-- Name -->
      <h2 id="name">
        <!-- Widget filter position -->
        <span v-if="widgetFilterOrder >= 0" title="Witget filtering order" id="witgetFilteringOrder">
          {{ widgetFilterOrder + 1 }}
        </span>
        {{ name }}
      </h2>

      <!-- Loading anim, messages & warning -->
      <div class="center">
        <!-- Loading from backend -->
        <div v-if="loading" class="saving">
          <span></span><span></span><span></span>
        </div>

        <!-- Error icon -->
        <div v-if="error_msg" @click="delete_error" class="dataError">
          <b>&#x26A0;</b> {{ error_msg }}
        </div>

        <!-- Color and selectedDataWarning -->
        <div v-if="colorWarning || selectedDataWarning" class="updateWarning">
          <b>&#x26A0;</b>
          <div v-if="colorWarning && selectedDataWarning">
            Selected color and data have changed
          </div>
          <!-- Color Warning -->
          <div v-else-if="colorWarning">The selected color have changed</div>
          <!-- selectedData Warning -->
          <div v-else-if="selectedDataWarning">
            The selected data have changed
          </div>

          <button class="warning" @click="drawPlot">Redraw</button>
          <button @click="
  colorWarning = false;
selectedDataWarning = false;
          ">
            Hide
          </button>
        </div>

        <!-- Clear filters -->
        <button v-if="clearFiltersAvailable" id="clearFiltersBtn" @click="clearFilters">
          <span class="badge">{{ widgetFilters.length }}</span>
          Clear filters
        </button>
      </div>

      <!-- Options : configuration, copy, settings, close btn, ... -->
      <div class="options" v-if="!simple">
        <!-- export btn -->
        <button v-if="exportData !== null" class="white aligned" title="Export widget data" @click="startExport">
          Export
          <inline-svg :src="require('../../../../../assets/svg/send.svg')" height="14" width="18" />
        </button>
        <!-- filtering ongoing btn -->
        <button v-if="canFilterSamples && startFiltering" class="purple highlighted" title="Stop filtering"
          @click="startFiltering = !startFiltering">
          <inline-svg :src="require('../../../../../assets/svg/filter.svg')" width="14" height="14" fill="white" />
          Filtering
        </button>
        <!-- start filtering btn -->
        <button v-if="canFilterSamples && !startFiltering" class="purple"
          :title="'Start filtering samples with the ' + title + ' widget'" @click="startFiltering = !startFiltering">
          <inline-svg :src="require('../../../../../assets/svg/filter.svg')" width="14" height="14" fill="white" />
        </button>
        <!-- save conf btn -->
        <button v-if="canSaveConfiguration" :class="'info ' + (confAsChanged ? 'highlighted' : '')"
          :title="'Save ' + title + ' widget configuration'" @click="saveConfiguration">
          <inline-svg :src="
            confAsChanged
              ? require('../../../../../assets/svg/save.svg')
              : require('../../../../../assets/svg/gear.svg')
          " width="14" height="14" fill="white" />
        </button>
        <!-- dublicate btn -->
        <button class="green" :title="'Duplicate the ' + title + ' widget'" @click="copy">
          <inline-svg :src="require('../../../../../assets/svg/copy.svg')" width="14" height="14" fill="white" />
        </button>
        <!-- Settings btn -->
        <button class="warning" :title="title + ' settings'" @click="settings">
          <inline-svg :src="require('../../../../../assets/svg/settings.svg')" width="14" height="14" />
        </button>
        <!-- Cross btn -->
        <button class="red" :title="'Close ' + title + ' widget'" @click="remove">
          <inline-svg :src="require('../../../../../assets/svg/close.svg')" width="11" height="11" fill="white" />
        </button>
      </div>
      <div class="options simple" v-else>
        <button class="red" :title="'Close ' + title + ' widget'" @click="remove"></button>
      </div>
    </div>

    <!-- Display the visualisation tool -->
    <slot />
  </div>
</template>

<script>
import WidgetConfPannel from "./widgetConfiguration/WidgetConfPannel";
import DataExportMenu from "../dataExport/DataExportMenu";

import swal from "sweetalert";

export default {
  name: "Widget",
  components: { WidgetConfPannel, DataExportMenu },
  props: {
    title: { type: String, default: "Widget" },
    index: { type: String, required: true },
    simple: { type: Boolean, default: false },
    conf: { type: Object },
  },
  data() {
    return {
      name: null,
      colorWarning: false,
      selectedDataWarning: false,
      loading: false,
      error_msg: null,

      // Configurations
      canSaveConfiguration: false,
      confSettings: false,
      confToSave: null,
      confAsChanged: false,
      suggestedConfName: null,

      // Filters
      canFilterSamples: false,
      startFiltering: false,

      // Export
      exportData: null,
      exportModal: false,
    };
  },
  created() {
    this.$on("loading", (loading) => (this.loading = loading));
    this.$on("errorMessage", this.errorMessage);
    this.$on("setExport", this.setExport);
    this.timeout = null;
    this.name = this.title;
  },
  mounted() {
    this.getWidgetProperties();
  },
  methods: {
    // Configurations
    getWidgetProperties() {
      this.loading = true;
      let slotCom = this.$slots.default[0];

      if (slotCom.componentInstance) {
        // canSaveConfiguration
        if (
          "getConf" in slotCom.componentInstance &&
          "setConf" in slotCom.componentInstance
        )
          this.canSaveConfiguration = true;

        // canFilterSamples
        if ("selectDataOnPlot" in slotCom.componentInstance)
          this.canFilterSamples = true;

        // Apply given conf
        if (this.canSaveConfiguration && this.conf) this.setConf(this.conf);
        this.loading = false;
      } else {
        // No component instance
        // try to get the conf from the slot after a delay
        setTimeout(() => this.getWidgetProperties(), 20);
      }
    },
    // Controls
    settings() {
      this.$emit("settings");
    },
    drawPlot() {
      this.$emit("redraw");
    },
    async remove() {
      // Firt ask if the user wants to save the widget configuration
      if (this.canSaveConfiguration && this.confAsChanged) {
        let rep = await swal({
          title: "Save the widget configuration ?",
          text: "You have changed the widget configuration, do you want to save it ?",
          buttons: {
            cancel: "Cancel",
            no: { text: "No", className: "red" },
            yes: "yes",
          },
        });
        if (rep === "yes") {
          this.saveConfiguration();
          return;
        } else if (rep === null) return;
      }

      // Then ask if the user wants to remove the widget filters
      if (this.canFilterSamples && this.widgetFilters.length > 0) {
        let rep = await swal({
          title: "Remove the widget filters ?",
          text: "You have set some filters with this widget, do you want to remove them ?",
          buttons: {
            cancel: "Cancel",
            no: "No",
            yes: { text: "Yes", className: "red" },
          },
        });
        if (rep === "yes") this.clearFilters();
        else if (rep === null) return;
      }

      // Finally remove the widget
      this.$emit("remove");
    },
    copy() {
      if (this.canSaveConfiguration) {
        // Load conf to copy
        let slotCom = this.$slots.default[0].componentInstance;
        let conf = slotCom.getConf();
        this.$emit("copy", { conf, name: this.name + " copy" });
      } else this.$emit("copy");
    },

    // Conf
    setConf(conf) {
      let slotCom = this.$slots.default[0];
      slotCom.componentInstance.setConf(conf.conf);
      this.name = conf.name;
      this.confSettings = false;
      setTimeout(() => {
        this.confAsChanged = false;
      }, 500);
    },
    setName(name) {
      this.name = name;
      this.confSettings = false;
    },
    saveConfiguration() {
      // Load conf to save
      let slotCom = this.$slots.default[0].componentInstance;
      this.confToSave = slotCom.getConf();

      // Find a suggested name
      this.suggestedConfName = "";
      if (this.name !== this.title) this.suggestedConfName = this.name;
      else if ("getConfNameSuggestion" in slotCom)
        this.suggestedConfName = slotCom.getConfNameSuggestion();

      // Open the conf creator modal
      this.confSettings = true;
    },
    confSaved(confName) {
      this.setName(confName);
      this.confAsChanged = false;
    },

    // Filters
    clearFilters() {
      this.$store.commit("addFilters", {
        filters: [],
        from: {
          widgetType: this.$parent.type,
          widgetName: this.$parent.name,
          widgetIndex: this.index,
        },
        removeExisting: true,
      });
      this.$emit("filterCleared");
    },

    // Export
    setExport(exportData) {
      this.exportData = exportData;
    },

    startExport() {
      this.exportModal = true;
    },

    // Other
    errorMessage(e) {
      this.error_msg = e;
      this.timeout = setTimeout(() => {
        this.delete_error();
      }, 5000);
    },
    delete_error() {
      this.error_msg = null;
      clearTimeout(this.timeout);
    },
  },
  computed: {
    // Filters
    widgetFilters() {
      return this.$store.state.SatisticalAnasysis.filters.filter(
        (filter) => filter.from.widgetIndex === this.index
      );
    },
    clearFiltersAvailable() {
      return this.widgetFilters.length > 0;
    },
    widgetFilterOrder() {
      // Place in the filtering order of the widget
      return this.$store.state.SatisticalAnasysis.filters.findIndex(
        (filter) => filter.from.widgetIndex === this.index
      );
    },
  },
  watch: {
    startFiltering(newVal) {
      if (newVal) this.$emit("filterStarted");
      else this.$emit("filterEnded");
    },
    widgetFilters(newVal) {
      if (newVal.length == 0) {
        // When all the filters has been removed, we can clear the filters
        this.$emit("filterCleared");
      }
    },
  },
};
</script>

<style scoped>
.card {
  height: 98%;
}

.card .title {
  display: flex;
  cursor: grab;
  transition: background-color 0.2s;
}

.card .title:active {
  cursor: grabbing;
}

.card .title.purple {
  background-color: var(--virtual);
}

#name {
  min-width: 30px;
}

#name.clickable {
  cursor: pointer;
}

#name.clickable:hover {
  text-decoration: underline;
}

#name #witgetFilteringOrder {
  border: white 1px solid;
  border-radius: 20px;
  padding: 2px 1px 0px 4px;
  margin-right: 5px;
  font-size: 0.8em;
}

/* Options */
.options {
  display: flex;
  justify-content: flex-end;
}

.options button.warning {
  width: 70px;
}

.options button+button {
  margin-left: 10px;
}

.simple button.red {
  width: 20px;
  height: 20px;
}

.center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-evenly;

  padding-left: 4px;
  padding-right: 4px;
}

/* Warning */
.updateWarning {
  display: flex;
  align-items: center;
  color: var(--warning);
  padding: 0px 8px 0px 8px;
}

.updateWarning button {
  padding: 1px 5px 1px 5px;
  margin-left: 10px;
}

/* Error */
.dataError {
  color: #ea5050;
  margin: 0px 10px 0px 10px;
  padding: 0px 8px 0px 8px;

  cursor: pointer;
}

.dataError:hover {
  filter: brightness(80%);
}

/* Loading Anim */
@keyframes blink {
  0% {
    opacity: 0.2;
  }

  20% {
    opacity: 1;
  }

  100% {
    opacity: 0.2;
  }
}

.saving {
  margin-left: 5px;
}

.saving span {
  animation-name: blink;
  animation-duration: 1.4s;
  animation-iteration-count: infinite;
  animation-fill-mode: both;
  height: 10px;
  width: 10px;
  border-radius: 50%;
  background-color: cadetblue;
  display: inline-block;
  margin-right: 2.5px;
  margin-left: 2.5px;
}

.saving span:nth-child(2) {
  animation-delay: 0.2s;
}

.saving span:nth-child(3) {
  animation-delay: 0.4s;
}
</style>