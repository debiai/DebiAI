<template>
  <div id="globalFilters">
    <!-- Column selection modal for creating a new filter -->
    <modal
      v-if="filterColumnSelection"
      @close="filterColumnSelection = false"
    >
      <ColumnSelection
        title="Select a column to filter"
        :data="data"
        :validateRequired="false"
        :validColumnsProperties="validColumnsProperties"
        v-on:cancel="filterColumnSelection = false"
        v-on:colSelect="selectFilterColumn"
      />
    </modal>

    <!-- Header -->
    <div
      id="title"
      style="display: flex"
    >
      <h2>
        <inline-svg
          :src="require('@/assets/svg/filter.svg')"
          width="18"
          height="18"
          style="margin-right: 3px"
        />
        Filters
      </h2>
      <span style="flex: 1"></span>

      <!-- Clear filters btn -->
      <button
        class="red"
        @click="clearAll"
      >
        Clear all filters
      </button>
      <!-- Close btn -->
      <button
        class="red"
        @click="$emit('cancel')"
      >
        Close
      </button>
    </div>

    <!-- Filters -->
    <FilterList
      :data="data"
      :filters="filters"
    />

    <!-- Controls -->
    <div id="controls">
      <!-- Add a value filter btn -->
      <button
        @click="
          filterSelectionType = 'values';
          filterColumnSelection = true;
        "
      >
        Add a value filter
      </button>
      <!-- Add an interval filter btn -->
      <button
        @click="
          filterSelectionType = 'intervals';
          filterColumnSelection = true;
        "
      >
        Add an interval filter
      </button>
      <DocumentationBlock>
        <b>Value filter:</b> filter the data by selecting a column and one or more value.
        <br />
        <br />
        <b>Interval filter:</b> filter the data by selecting a column and one or more interval.
        <br />
        An interval is a range of values between two values.
      </DocumentationBlock>
    </div>
  </div>
</template>

<script>
// Component
import ColumnSelection from "../common/ColumnSelection";
import FilterList from "./FilterList.vue";

export default {
  components: {
    ColumnSelection,
    FilterList,
  },
  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      filterColumnSelection: false,
      filterSelectionType: null,

      validColumnsProperties: {
        types: ["Class", "Num", "Bool"],
      },
    };
  },
  methods: {
    clearAll() {
      this.$store.commit("clearAllFilters");
    },

    // Filter creation
    selectFilterColumn(colId) {
      // Add a new empty filter to the store
      const filter = { columnIndex: colId };

      if (this.filterSelectionType == "intervals") {
        filter.type = "intervals";
        filter.intervals = [];
      } else if (this.filterSelectionType == "values") {
        filter.type = "values";
        filter.values = [];
      } else {
        console.error("Unknown filter type: " + this.filterSelectionType);
        return;
      }

      this.$store.commit("addFilters", {
        filters: [filter],
        from: {
          widgetType: "Custom",
          widgetName: "Custom",
          widgetIndex: 0,
        },
      });

      this.filterColumnSelection = false;
    },
  },
  computed: {
    filters() {
      // We are reading the filters from the store in real time
      return this.$store.state.StatisticalAnalysis.filters;
    },
  },
};
</script>

<style scoped>
#globalFilters {
  color: black;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-width: 60vw;
  min-height: 70vh;
  max-height: 85vh;
  max-width: 85vw;
}
#controls {
  padding-top: 20px;
  display: flex;
  align-items: center;
}
</style>
