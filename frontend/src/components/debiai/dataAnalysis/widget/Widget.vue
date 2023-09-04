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
        @confSelected="(conf) => setConf(conf, false)"
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
      :class="widgetHeaderClass"
      @mousedown="grabbing = true"
      @mouseup="grabbing = false"
    >
      <!-- Name, filtering btn, filtering order, ... -->
      <div id="name">
        <h2>{{ name }}</h2>

        <!-- Widget filter position 2 -->
        <span style="width: 35px">
          <span
            v-if="widgetFilterOrder >= 0"
            title="widget filtering order"
            id="widgetFilteringOrder2"
            class="filterOrder"
          >
            {{ widgetFilterOrder + 1 }}
          </span>
        </span>

        <!-- start filtering btn -->
        <button
          v-if="canFilterSamples && !startFiltering"
          :title="'Start filtering samples with the ' + title + ' widget'"
          @click="startFiltering = !startFiltering"
          style="height: 28px"
        >
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="12"
            height="12"
            fill="black"
          />
          Start filtering
        </button>

        <!-- filtering ongoing btn -->
        <button
          v-if="canFilterSamples && startFiltering"
          class="highlighted"
          title="Stop filtering"
          @click="startFiltering = !startFiltering"
          style="height: 28px"
        >
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="12"
            height="12"
          />
          Filtering
        </button>

        <!-- Clear filters -->
        <div
          v-if="canFilterSamples && startFiltering && !clearFiltersAvailable"
          style="margin-left: 10px"
        >
          No filters
        </div>
        <button
          v-if="clearFiltersAvailable"
          id="clearFiltersBtn"
          @click="clearFilters"
          style="height: 28px"
        >
          <span class="badge">{{ widgetFilters.length }}</span>
          Clear filters
        </button>

        <!-- Widget filter position -->
        <span
          v-if="widgetFilterOrder >= 0"
          title="widget filtering order"
          id="widgetFilteringOrder"
          class="filterOrder"
        >
          {{ widgetFilterOrder + 1 }}
        </span>
      </div>

      <!-- Loading anim, messages, warning -->
      <div class="center">
        <!-- Loading animation -->
        <LoadingAnimation v-if="loading" />

        <!-- Error icon -->
        <div
          v-if="error_msg"
          @click="delete_error"
          class="dataError"
        >
          <b>&#x26A0;</b> {{ error_msg }}
        </div>

        <!-- Color and selectedDataWarning -->
        <transition name="fade">
          <div
            v-if="colorWarning || selectedDataWarning"
            class="updateWarning"
          >
            <b>&#x26A0;</b>
            <div v-if="colorWarning && selectedDataWarning">
              Selected color and data have changed
            </div>
            <!-- Color Warning -->
            <div v-else-if="colorWarning">The color has changed</div>
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
        </transition>
      </div>

      <!-- On right: filters applied, configuration, copy, settings, close btn, ... -->
      <div class="options">
        <!-- Filters applied -->
        <button
          v-if="localFilters.length > 0"
          id="filtersApplied"
          @click="showLocalFilters = true"
          title="Filters applied to this widget on creation"
          style="height: 28px"
        >
          <inline-svg
            :src="require('@/assets/svg/filter.svg')"
            width="12"
            height="12"
            fill="black"
          />
          On creation
          <span class="badge">{{ localFilters.length }}</span>
        </button>

        <!-- export btn -->
        <button
          v-if="exportData !== null"
          class="aligned"
          title="Export widget data"
          style="width: 75px"
          @click="startExport"
        >
          Export
          <inline-svg
            :src="require('@/assets/svg/send.svg')"
            height="14"
            width="18"
          />
        </button>

        <!-- Settings btn -->
        <button
          class="settings"
          :title="title + ' settings'"
          @click="settings"
        >
          <inline-svg
            :src="require('@/assets/svg/settings.svg')"
            width="14"
            height="14"
          />
        </button>

        <!-- Menu btn -->
        <button
          @click="showMenu = !showMenu"
          :title="'Open the ' + title + ' widget menu'"
        >
          <inline-svg
            :src="require('@/assets/svg/menu.svg')"
            width="15"
            height="15"
          />
        </button>
      </div>
    </div>

    <!-- Menu -->
    <transition name="fade">
      <dropdown-menu
        v-if="showMenu"
        :menu="[
          { name: 'Duplicate', action: copy, icon: 'copy' },
          {
            name: 'Download image',
            action: downloadImage,
            icon: 'downloadImage',
            disabled: loading,
            available: canExportImage,
          },

          {
            name: 'Comment' + (comments.length ? ' (' + comments.length + ')' : ''),
            action: () => (commentModal = !commentModal),
            icon: 'comment',
          },
          {
            name: 'Save / load settings',
            action: saveConfiguration,
            icon: 'save',
            available: canSaveConfiguration,
          },
          { name: 'separator' },
          { name: 'Close', action: remove, icon: 'close' },
        ]"
        @close="showMenu = false"
      />
    </transition>

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
import DropdownMenu from "@/components/common/DropdownMenu";

import swal from "sweetalert";

export default {
  name: "Widget",
  components: { WidgetConfPanel, DataExportMenu, FilterList, Comments, DropdownMenu },
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
      showMenu: false,
      colorWarning: false,
      selectedDataWarning: false,
      loading: false,
      error_msg: null,
      grabbing: false,

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
        if (this.canSaveConfiguration && this.configuration) this.setConf(this.configuration, true);
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

      // Finally remove the widget with an animation
      // Apply animation to the widget
      this.$el.style.animation = "removeWidget 300ms";
      setTimeout(() => {
        this.$emit("remove");
      }, 300);
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
    setConf(configuration, onStartup = false) {
      let slotCom = this.$slots.default[0];
      slotCom.componentInstance.setConf(configuration.configuration, { onStartup: onStartup });
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
    // Css
    widgetHeaderClass() {
      let baseClass = "title grid-stack-item-content";
      if (this.startFiltering) baseClass += " filtering";
      if (this.grabbing) baseClass += " grabbing";
      return baseClass;
    },

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
  margin: 5px;

  #widgetHeader {
    display: flex;
    cursor: grab;
    padding: 3px 3px 3px 8px;

    &.grabbing {
      cursor: grabbing;
    }

    #name {
      display: flex;
      align-items: center;
      h2 {
        white-space: nowrap;
      }

      button {
        opacity: 0;
        transition: opacity 0.3s;
        margin-left: 5px;
        white-space: nowrap;
      }

      #widgetFilteringOrder {
        opacity: 0;
      }
    }

    /* Options */
    .options {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      opacity: 0;
      transition: opacity 0.3s;

      button {
        display: flex;
        justify-content: center;
        align-items: center;
        min-width: 33px;
        min-height: 28px;

        &.settings {
          width: 70px;
        }
      }

      button + button {
        margin-left: 5px;
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
        color: var(--danger);
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
  }

  &:hover {
    #widgetHeader {
      #name {
        button,
        #widgetFilteringOrder {
          opacity: 1;
        }
        #widgetFilteringOrder2 {
          opacity: 0;
        }
      }

      .options {
        opacity: 1;
      }
    }
  }
}
</style>
