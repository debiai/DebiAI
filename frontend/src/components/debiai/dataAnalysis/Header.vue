<template>
  <div id="Header">
    <!-- colored column selection modal -->
    <modal
      v-if="selectColoredCol"
      @close="selectColoredCol = false"
    >
      <ColumnSelection
        title="Select the workspace colored column"
        :data="data"
        :validateRequired="false"
        :colorSelection="false"
        v-on:cancel="selectColoredCol = false"
        v-on:colSelect="coloredColSelect"
      />
    </modal>
    <!-- Filters modal -->
    <modal
      v-if="filtersMenu"
      @close="filtersMenu = false"
    >
      <GlobalFilters
        :data="data"
        v-on:cancel="filtersMenu = false"
      />
    </modal>

    <!-- DebiAI Logo and project name -->
    <div id="logoAndName">
      <!-- DebiAI Logo -->
      <router-link
        id="debiaiMenuLogo"
        :to="
          '/dataprovider/' +
          $store.state.ProjectPage.dataProviderId +
          '/project/' +
          $store.state.ProjectPage.projectId
        "
      >
        <img
          src="@/assets/images/DebiAI_black.png"
          alt="DebiAI"
          height="48"
        />
      </router-link>

      <!-- Project name -->
      <div id="projectName">
        <router-link :to="'/'">Projects</router-link>
        /
        <router-link
          :to="
            '/dataprovider/' +
            $store.state.ProjectPage.dataProviderId +
            '/project/' +
            $store.state.ProjectPage.projectId
          "
          >{{ $store.state.ProjectPage.projectId }}</router-link
        >
        / Analysis
      </div>
    </div>

    <!-- Add widget button -->
    <button
      id="addWidgetButton"
      @click="$emit('addWidget')"
    >
      <inline-svg
        :src="require('@/assets/svg/close.svg')"
        width="13"
        height="13"
      />
      Add a widget

      <!-- <inline-svg
        :src="require('@/assets/svg/bar_plot.svg')"
        width="15"
        height="15"
      /> -->
    </button>

    <!-- Colored column info -->
    <div
      id="coloredColumn"
      v-if="coloredColumnIndex !== null"
    >
      Color
      <button
        @click="selectColoredCol = true"
        class="blue"
        title="Change the analysis colored column"
      >
        {{ data.columns.find((c) => c.index == coloredColumnIndex).label }}
      </button>
      <!-- <Column
        :column="data.columns.find((c) => c.index == coloredColumnIndex)"
        :colorSelection="false"
        v-on:selected="selectColoredCol = true"
      /> -->
    </div>
    <div
      id="coloredColumn"
      v-else
    >
      Color
      <button
        @click="selectColoredCol = true"
        title="Select the analysis colored column"
      >
        <inline-svg
          :src="require('@/assets/svg/close.svg')"
          width="8"
          height="8"
        />
      </button>
    </div>

    <!-- Filters panel button and selected data info -->
    <div
      id="filtersAndSelectedData"
      :class="$store.state.StatisticalAnalysis.filters.length ? 'filters' : ''"
    >
      <!-- Filters panel button -->
      <!-- Selected data info -->
      <SelectedDataInfo
        :data="data"
        :selectedData="selectedData"
        v-on:dataSelection="dataSelection"
      />

      <!-- Global filters -->
      <button
        @click="filtersMenu = true"
        id="filtersMenu"
        title="Global filters"
        :class="$store.state.StatisticalAnalysis.filters.length > 0 ? 'blue' : ''"
      >
        <inline-svg
          :src="require('@/assets/svg/filter.svg')"
          width="20"
          height="20"
          style="margin-right: 3px"
        />
        <span
          class="badge"
          v-if="$store.state.StatisticalAnalysis.filters.length"
          >{{ $store.state.StatisticalAnalysis.filters.length }}</span
        >
      </button>
    </div>
  </div>
</template>

<script>
import SelectedDataInfo from "./dataNavigation/SelectedDataInfo";
import Column from "./common/Column";
import ColumnSelection from "./common/ColumnSelection";
import GlobalFilters from "./dataFilters/GlobalFilters";

export default {
  components: {
    SelectedDataInfo,
    Column,
    ColumnSelection,
    GlobalFilters,
  },
  props: {
    data: { type: Object, required: true },
    selectedData: { type: Array, required: true },
  },
  data() {
    return {
      projectId: null,
      selectColoredCol: false,
      selectDataset: false,
      filtersMenu: false,
    };
  },
  created() {
    this.projectId = this.$store.state.ProjectPage.projectId;
  },
  methods: {
    dataSelection(selection) {
      // Update the selected samples for all widgets
      this.$emit("dataSelection", selection);
    },
    coloredColSelect(index) {
      // Update the selected colored column
      this.$store.commit("setColoredColumnIndex", index);
      this.selectColoredCol = false;
    },
  },
  computed: {
    coloredColumnIndex() {
      return this.$store.state.StatisticalAnalysis.coloredColumnIndex;
    },
  },
};
</script>

<style lang="scss" scoped>
#Header {
  height: 60px;
  width: 100%;
  position: fixed;
  top: 0px;
  z-index: 1;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 50px;

  background-color: var(--greyLight);
  border-bottom: solid #a8a8a8 2px;

  button {
    height: 60%;
  }

  img {
    margin-left: 15px;
    padding-top: 5px;
  }

  #logoAndName {
    display: flex;
    align-items: center;
    gap: 10px;
    // flex: 1;

    #debiaiMenuLogo {
      margin-right: 10px;
    }

    #projectName {
      font-size: 18px;
      font-weight: bold;
      color: #a8a8a8;

      a {
        color: rgb(53, 53, 53);
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }
    }
  }

  #filtersAndSelectedData {
    padding: 0px 20px;
    display: flex;
    align-items: center;
    gap: 20px;
  }

  #addWidgetButton {
    // flex: 1;
    margin-right: 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
    color: var(--primary);
    font-weight: bold;
    border: solid var(--primary) 2px;
    border: none;

    text-decoration: none;
    font-size: 1.2em;

    svg {
      padding-bottom: 2px;
      fill: var(--primary);
      margin-left: 3px;
      transform: rotate(45deg);
    }
  }

  #filtersMenu {
    svg {
      padding: 0px 5px 0px 8px;
    }
  }
}

#coloredColumn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  // flex-direction: column-reverse;
  gap: 15px;
  font-size: 1em;
  padding: 0px 10px;
  color: var(--fontColorLight);

  button {
    padding-left: 15px;
    padding-right: 15px;
    min-width: 50px;
    svg {
      // Rotate
      transform: rotate(45deg);
    }
  }
}
</style>
