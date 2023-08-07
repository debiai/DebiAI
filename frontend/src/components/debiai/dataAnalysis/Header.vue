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

    <!-- Filters panel button -->
    <button @click="filtersMenu = true">
      <span
        class="badge"
        v-if="$store.state.StatisticalAnalysis.filters.length"
        >{{ $store.state.StatisticalAnalysis.filters.length }}</span
      >
      <inline-svg
        :src="require('@/assets/svg/filter.svg')"
        width="10"
        height="10"
        fill="white"
        style="margin-right: 3px"
      />
      <u>Global filters</u>
    </button>

    <!-- Selected data info -->
    <SelectedDataInfo
      :data="data"
      :selectedData="selectedData"
      v-on:dataSelection="dataSelection"
    />

    <!-- Colored column info -->
    <div
      id="coloredColumn"
      v-if="coloredColumnIndex !== null"
    >
      Colored col :
      <Column
        :column="data.columns.find((c) => c.index == coloredColumnIndex)"
        :colorSelection="false"
        v-on:selected="selectColoredCol = true"
      />
      <!-- <u>{{ data.columns[coloredColumnIndex].label }}</u> -->
    </div>
    <div
      id="coloredColumn"
      v-else
    >
      <button @click="selectColoredCol = true">Select a colored column</button>
    </div>

    <!-- Add widget button -->
    <button
      id="addWidgetButton"
      @click="$emit('addWidget')"
    >
      <inline-svg
        :src="require('@/assets/svg/bar_plot.svg')"
        width="15"
        height="15"
        fill="white"
        style="margin-right: 3px"
      />
      <u>+ Add a widget</u>
    </button>
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
  justify-content: space-between;
  align-items: center;

  background-color: #f6f6f6;
  border-bottom: solid #a8a8a8 2px;

  button {
    height: 60%;
  }

  img {
    margin-left: 10px;
  }

  #addWidgetButton {
    margin-right: 10px;
    display: flex;
    gap: 5px;
    align-items: center;
  }
}

#coloredColumn {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}
#coloredColumn u {
  margin-left: 3px;
  border: solid white 1px;
  border-radius: 5px;
  padding: 2px;
}
</style>
