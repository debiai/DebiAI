<template>
  <div class="card">
    <!-- Widget configuration modal -->
    <modal
      v-if="confSettings"
      @close="confSettings = false"
    >
      <WidgetConfPanel
        :widgetTitle="title"
        :widgetName="name"
        :confToSave="confToSave"
        :suggestedConfName="suggestedConfName"
        :widgetKey="widgetKey"
        @cancel="confSettings = false"
        @saved="confSaved"
        @confSelected="setConf"
        @setWidgetName="setName"
      />
    </modal>

    <!-- Export data modal -->
    <modal
      v-if="exportModal"
      @close="exportModal = false"
    >
      <DataExportMenu
        :dataToExport="exportData"
        @exported="exportModal = false"
        @cancel="exportModal = false"
      />
    </modal>

    <!-- Local filters modal -->
    <modal
      v-if="showLocalFilters"
      @close="showLocalFilters = false"
    >
      <h3 class="aligned spaced gapped">
        <span>
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="18"
            height="18"
            style="margin-right: 3px"
          />
          Filters applied to this widget
        </span>
        <button
          class="red"
          @click="showLocalFilters = false"
        >
          Close
        </button>
      </h3>
      <FilterList
        :data="data"
        :filters="localFilters"
        :readOnly="true"
      />
    </modal>

    <!-- Widget Header -->
    <div
      id="widgetHeader"
      :class="'title grid-stack-item-content ' + (startFiltering ? 'purple' : '')"
    >
      <!-- Name -->
      <h2 id="name">
        <!-- Widget filter position -->
        <span
          v-if="widgetFilterOrder >= 0"
          title="Witget filtering order"
          id="witgetFilteringOrder"
        >
          {{ widgetFilterOrder + 1 }}
        </span>
        {{ name }}
      </h2>

      <!-- Loading anim, messages, warning & filters applied -->
      <div class="center">
        <!-- Loading animation -->
        <div
          v-if="loading"
          class="saving"
        >
          <span></span><span></span><span></span>
        </div>

        <!-- Error icon -->
        <div
          v-if="error_msg"
          @click="delete_error"
          class="dataError"
        >
          <b>&#x26A0;</b> {{ error_msg }}
        </div>

        <!-- Color and selectedDataWarning -->
        <div
          v-if="colorWarning || selectedDataWarning"
          class="updateWarning"
        >
          <b>&#x26A0;</b>
          <div v-if="colorWarning && selectedDataWarning">Selected color and data have changed</div>
          <!-- Color Warning -->
          <div v-else-if="colorWarning">The selected color have changed</div>
          <!-- selectedData Warning -->
          <div v-else-if="selectedDataWarning">The selected data have changed</div>

          <button
            class="warning"
            @click="drawPlot"
          >
            Redraw
          </button>
          <button
            @click="
              colorWarning = false;
              selectedDataWarning = false;
            "
          >
            Hide
          </button>
        </div>

        <!-- Clear filters -->
        <button
          v-if="clearFiltersAvailable"
          id="clearFiltersBtn"
          @click="clearFilters"
        >
          <span class="badge">{{ widgetFilters.length }}</span>
          Clear filters
        </button>

        <!-- Filters applied -->
        <button
          v-if="localFilters.length > 0"
          id="filtersApplied"
          class="warning"
          @click="showLocalFilters = true"
        >
          <span class="badge">{{ localFilters.length }}</span>
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="12"
            height="12"
            fill="black"
          />
          applied
        </button>
      </div>

      <!-- Options : configuration, copy, settings, close btn, ... -->
      <div class="options">
        <!-- Comment btn -->
        <button
          :class="'white ' + (commentModal ? 'highlighted' : '')"
          title="Comment this widget"
          @click="commentModal = !commentModal"
        >
          <span v-if="comments.length">{{ comments.length }}</span>
          <inline-svg
            :src="require('@/assets/svg/comment.svg')"
            height="14"
            width="18"
          />
        </button>
        <!-- export btn -->
        <button
          v-if="exportData !== null"
          class="white aligned"
          title="Export widget data"
          style="width: 60px"
          @click="startExport"
        >
          Export
          <inline-svg
            :src="require('@/assets/svg/send.svg')"
            height="14"
            width="18"
          />
        </button>
        <!-- export image btn -->
        <button
          v-if="canExportImage"
          class="white"
          title="Download an image of the plot"
          @click="downloadImage"
          :disabled="loading"
        >
          <inline-svg
            :src="require('@/assets/svg/downloadImage.svg')"
            height="14"
            width="18"
          />
        </button>
        <!-- filtering ongoing btn -->
        <button
          v-if="canFilterSamples && startFiltering"
          class="purple highlighted"
          style="width: 85px"
          title="Stop filtering"
          @click="startFiltering = !startFiltering"
        >
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="14"
            height="14"
            fill="white"
          />
          Filtering
        </button>
        <!-- start filtering btn -->
        <button
          v-if="canFilterSamples && !startFiltering"
          class="purple"
          :title="'Start filtering samples with the ' + title + ' widget'"
          @click="startFiltering = !startFiltering"
        >
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="14"
            height="14"
            fill="white"
          />
        </button>
        <!-- save configuration btn -->
        <button
          v-if="canSaveConfiguration"
          :class="'info ' + (confAsChanged ? 'highlighted' : '')"
          :title="'Save ' + title + ' widget configuration'"
          @click="saveConfiguration"
        >
          <inline-svg
            :src="require('@/assets/svg/save.svg')"
            width="14"
            height="14"
            style="filter: invert(95%)"
          />
        </button>
        <!-- Copy btn -->
        <button
          class="green"
          :title="'Duplicate the ' + title + ' widget'"
          @click="copy"
        >
          <inline-svg
            :src="require('@/assets/svg/copy.svg')"
            width="14"
            height="14"
            fill="white"
          />
        </button>
        <!-- Settings btn -->
        <button
          class="warning"
          :title="title + ' settings'"
          @click="settings"
        >
          <inline-svg
            :src="require('@/assets/svg/settings.svg')"
            width="14"
            height="14"
          />
        </button>
        <!-- Close btn -->
        <button
          class="red"
          :title="'Close ' + title + ' widget'"
          @click="remove"
        >
          <inline-svg
            :src="require('@/assets/svg/close.svg')"
            width="11"
            height="11"
            fill="white"
          />
        </button>
      </div>
    </div>

    <!-- Display the Widget content -->
    <slot />

    <!-- Widget Comments -->
    <Comments
      v-if="commentModal"
      :comments="comments"
      @addComment="addComment"
      @removeComment="removeComment"
      @close="commentModal = false"
    />
  </div>
</template>

<script>
import WidgetConfPanel from "./widgetConfigurationCreation/WidgetConfPanel";
import DataExportMenu from "../dataExport/DataExportMenu";
import FilterList from "../dataFilters/FilterList";
import Comments from "./comments/Comments";

import swal from "sweetalert";

export default {
  name: "Widget",
  components: { WidgetConfPanel, DataExportMenu, FilterList, Comments },
  props: {
    data: { type: Object, required: true },
    widgetKey: { type: String, required: true },
    title: { type: String, default: "Widget" },
    index: { type: String, required: true },
    configuration: { type: Object },
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
      showLocalFilters: false,
      localFilters: [],

      // Export
      exportData: null,
      exportModal: false,
      canExportImage: false,

      // Comments
      commentModal: false,
      comments: [],
    };
  },
  created() {
    this.$on("loading", (loading) => (this.loading = loading));
    this.$on("errorMessage", this.errorMessage);
    this.$on("setExport", this.setExport);
    this.$on("drawn", this.drawn);
    this.timeout = null;
    this.name = this.title;
  },
  mounted() {
    // Get what the widget content can do
    this.getWidgetProperties();
  },
  methods: {
    // Configurations
    getWidgetProperties() {
      this.loading = true;
      let slotCom = this.$slots.default[0];

      if (slotCom.componentInstance) {
        // canSaveConfiguration
        if ("getConf" in slotCom.componentInstance && "setConf" in slotCom.componentInstance)
          this.canSaveConfiguration = true;

        // canFilterSamples
        if ("selectDataOnPlot" in slotCom.componentInstance) this.canFilterSamples = true;

        // canExportImage
        if ("getImage" in slotCom.componentInstance) this.canExportImage = true;

        // Apply given configuration
        if (this.canSaveConfiguration && this.configuration) this.setConf(this.configuration);
        this.loading = false;
      } else {
        // No component instance
        // try to get the configuration from the slot after a delay
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
      // First ask if the user wants to save the widget configuration
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
    getComponentConf() {
      if (this.canSaveConfiguration) {
        let slotCom = this.$slots.default[0].componentInstance;
        return slotCom.getConf();
      } else return null;
    },
    copy() {
      if (this.canSaveConfiguration) {
        // Load configuration to copy
        let configuration = this.getComponentConf();
        this.$emit("copy", { configuration, name: this.name });
      } else this.$emit("copy");
    },

    // configuration
    setConf(configuration) {
      let slotCom = this.$slots.default[0];
      slotCom.componentInstance.setConf(configuration.configuration);
      if (configuration.name) this.name = configuration.name;
      else this.name = this.title;
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
      // Load configuration to save
      let slotCom = this.$slots.default[0].componentInstance;
      this.confToSave = slotCom.getConf();

      // Find a suggested name
      if (slotCom.getConfNameSuggestion) this.suggestedConfName = slotCom.getConfNameSuggestion();
      else this.suggestedConfName = null;

      // Open the configuration creator modal
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
    drawn() {
      this.selectedDataWarning = false;

      // The plot has been drawn, we can save a copy of the local filters
      const storeFilters = this.$store.state.StatisticalAnalysis.filters;
      this.localFilters = JSON.parse(JSON.stringify(storeFilters));
    },

    // Export
    setExport(exportData) {
      const dataProviderId = this.$store.state.ProjectPage.dataProviderId;
      const projectId = this.$store.state.ProjectPage.projectId;
      const selectionIds = this.$store.state.ProjectPage.selectionsIds;

      if (!exportData) {
        this.exportData = null;
        return;
      }

      // Add project and data provider id to the export data
      this.exportData = {
        origin: "DebiAI",
        project_id: projectId,
        data_provider_id: dataProviderId,
        selection_ids: selectionIds,
        ...exportData,
      };
    },
    startExport() {
      this.exportModal = true;
    },
    getImage() {
      if (this.canExportImage) {
        let slotCom = this.$slots.default[0].componentInstance;
        return slotCom.getImage();
      } else return null;
    },
    downloadImage() {
      // Star a request
      this.$store.commit("startRequest", {
        name: "Downloading image",
        code: this.index,
      });
      this.loading = true;

      setTimeout(() => {
        this.getImage()
          .then((image) => {
            if (image) {
              let link = document.createElement("a");
              link.href = image;

              // Get the project name
              const projectName = this.$store.state.ProjectPage.projectId;

              const imageName = this.name.replace(/ /g, "_");
              link.download = projectName + "_" + imageName;
              link.click();
            }
          })
          .finally(() => {
            this.loading = false;
            this.$store.commit("endRequest", this.index);
          });
      }, 100);
    },

    // Comments
    addComment({ title, text }) {
      this.comments.push({
        id: this.$services.uuid(),
        title,
        text,
      });
    },
    removeComment(id) {
      this.comments = this.comments.filter((comment) => comment.id !== id);
    },
    getComments() {
      return this.comments;
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
      return this.$store.state.StatisticalAnalysis.filters.filter(
        (filter) => filter.from.widgetIndex === this.index
      );
    },
    clearFiltersAvailable() {
      return this.widgetFilters.length > 0;
    },
    widgetFilterOrder() {
      // Place in the filtering order of the widget
      return this.$store.state.StatisticalAnalysis.filters.findIndex(
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
    commentModal(newVal) {
      // Update the plot size when the comment modal is opened or closed
      window.dispatchEvent(new Event("resize"));
    },
    comments(newVal) {
      // Update the plot size when the comments are updated
      window.dispatchEvent(new Event("resize"));
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  height: 98%;
}

.card .title {
  display: flex;
  cursor: grab;
  transition: background-color 0.2s;
}

#widgetHeader {
  color:rgb(105, 105, 105);
  background: rgb(230, 230, 230);
}

.card .title:active {
  cursor: grabbing;
}

.card .title.purple {
  background-color: var(--virtual);
}

#name {
  overflow: hidden;
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
  opacity: 0;
  transition: opacity 0.5s;

  button {
    width: 35px;
    padding: 2px 0px 2px 0px;
  }
  button.warning {
    width: 70px;
  }

  button + button {
    margin-left: 5px;
  }
}

.card:hover {
  .options {
    opacity: 1;
    transition: opacity 0.1s;
  }
}

.center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-evenly;

  padding-left: 4px;
  padding-right: 4px;

  /* Warning */
  .updateWarning {
    display: flex;
    align-items: center;
    color: var(--warning);
    padding: 0px 8px 0px 8px;
  }

  /* Set all the text to no wram and overflow hidden */
  .updateWarning * {
    white-space: nowrap;
    overflow: hidden;
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
}
</style>
