<template>
  <div id="Footer">
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
    <!-- Selection selection modal -->
    <modal
      v-if="selectDataset"
      @close="selectDataset = false"
    >
      <SelectionSelection @cancel="selectDataset = false" />
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

    <div id="leftBtns">
      <button @click="selectDataset = !selectDataset">
        <inline-svg
          :src="require('../../../../../assets/svg/loupe.svg')"
          width="10"
          height="10"
          fill="white"
          style="margin-right: 3px"
        />
        <u>Selections</u>
      </button>
      <button @click="filtersMenu = true">
        <span
          class="badge"
          v-if="$store.state.StatisticalAnalysis.filters.length"
          >{{ $store.state.StatisticalAnalysis.filters.length }}</span
        >
        <inline-svg
          :src="require('../../../../../assets/svg/filter.svg')"
          width="10"
          height="10"
          fill="white"
          style="margin-right: 3px"
        />
        <u>Global filters</u>
      </button>
    </div>

    <SelectedDataInfo
      :data="data"
      :selectedData="selectedData"
      v-on:dataSelection="dataSelection"
    />

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
    <div id="exportControls">
      <!-- <button disabled>Export data</button>
      <button disabled>Export plots</button>
      <button disabled>Sample analysis</button> -->
    </div>
  </div>
</template>

<script>
import SelectionSelection from "./SelectionSelection";
import SelectedDataInfo from "./SelectedDataInfo";
import Column from "../common/Column";
import ColumnSelection from "../common/ColumnSelection";
import GlobalFilters from "../dataFilters/GlobalFilters";

export default {
  components: {
    SelectionSelection,
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

<style scoped>
#Footer {
  height: 30px;
  background-color: var(--primaryDark);
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;

  display: flex;
  justify-content: space-between;
  align-items: center;
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

#exportControls {
  display: flex;
  align-items: center;
  margin-right: 70px;
}
#exportControls button + button {
  margin-left: 5px;
}
</style>
