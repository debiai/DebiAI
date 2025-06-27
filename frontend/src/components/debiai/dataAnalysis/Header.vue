<template>
  <div id="Header">
    <!-- Colored column selection modal -->
    <modal
      v-if="selectColoredCol"
      @close="selectColoredCol = false"
    >
      <ColumnSelection
        title="Select the workspace colored column"
        :validColumnsProperties="validColoredColumnProperties"
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
        id="debiaiLogo"
        to="/"
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
          >{{
            $store.state.ProjectPage.projectName
              ? $store.state.ProjectPage.projectName
              : $store.state.ProjectPage.projectId
          }}</router-link
        >
        /
        <span v-if="data.mode === 'exploration'">
          <router-link
            :to="
              '/dataprovider/' +
              $store.state.ProjectPage.dataProviderId +
              '/project/' +
              $store.state.ProjectPage.projectId +
              '/exploration'
            "
            >Explorations</router-link
          >
          /
          <router-link
            :to="
              '/dataprovider/' +
              $store.state.ProjectPage.dataProviderId +
              '/project/' +
              $store.state.ProjectPage.projectId +
              '/exploration/' +
              data.explorationId
            "
            >{{ data.explorationName }}</router-link
          >
        </span>
        <span v-else>
          {{ data.mode ? $services.uppercaseFirstLetter(data.mode) : "Analysis" }}
        </span>
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
    </button>

    <!-- Colored column info -->
    <div
      id="coloredColumn"
      v-if="coloredColumnIndex !== null && coloredColumn"
    >
      Color
      <button
        @click="selectColoredCol = true"
        class="blue"
        title="Change the analysis colored column"
      >
        {{ coloredColumn.label }}
      </button>
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
      <!-- Selected data info -->
      <SelectedDataInfo :data="data" />

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
import ColumnSelection from "./common/ColumnSelection";
import GlobalFilters from "./dataFilters/GlobalFilters";

export default {
  components: {
    SelectedDataInfo,
    ColumnSelection,
    GlobalFilters,
  },
  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      projectId: null,
      selectColoredCol: false,
      selectDataset: false,
      filtersMenu: false,
      validColoredColumnProperties: {
        types: ["Class", "Num", "Bool"],
      },
    };
  },
  created() {
    this.projectId = this.$store.state.ProjectPage.projectId;
  },
  methods: {
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
    coloredColumn() {
      if (this.coloredColumnIndex === null) return null;

      const coloredColumn = this.data.getColumn(this.coloredColumnIndex);
      if (coloredColumn) return coloredColumn;
      else {
        this.$store.commit("setColoredColumnIndex", null);
        return null;
      }
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
  z-index: 2;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;

  background-color: var(--greyLight);
  border-bottom: var(--greyDark) 2px solid;

  #logoAndName {
    display: flex;
    align-items: center;
    gap: 10px;
    // flex: 1;

    #debiaiLogo {
      margin: 5px 10px 0px 15px;
    }

    #projectName {
      font-size: 18px;
      font-weight: bold;
      color: var(--fontColorLight);
      white-space: nowrap;

      a {
        color: var(--fontColor);
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
    white-space: nowrap;

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
  gap: 15px;
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

@media screen and (max-width: 1000px) {
  // Hide the logo
  #logoAndName {
    padding-left: 10px;
    #debiaiLogo {
      display: none;
    }
  }
}
</style>
