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
        v-on:cancel="filterColumnSelection = false"
        v-on:colSelect="selectFilterColumn"
      />
    </modal>

    <!-- request creation modal -->
    <!-- <modal
      v-if="requestCreation"
      @close="requestCreation = false"
    >
      <RequestCreation @cancel="requestCreation = false" />
    </modal> -->

    <!-- Request selection modal -->
    <!-- <modal
      v-if="requestSelection"
      @close="requestSelection = false"
    >
      <Requests
        @close="requestSelection = false"
        :selectionMode="true"
        @requestSelected="requestSelected"
      />
    </modal> -->

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
      <!-- Load filters btn -->
      <!-- TODO, revert in the filters update -->
      <!-- <button
        @click="requestSelection = true"
        title="Available in a futur update"
      >
        <inline-svg
          :src="require('@/assets/svg/import.svg')"
          width="10"
          height="10"
          fill="lightgrey"
        />
        Load filters from a request
      </button> -->
      <!-- Save request btn -->
      <!-- TODO, revert the always disapled in the filters update -->
      <!-- <button
        class="green"
        :disabled="filters.length == 0"
        @click="requestCreation = true"
        title="Available in a futur update"
      >
        <inline-svg
          :src="require('@/assets/svg/save.svg')"
          width="13"
          height="13"
          fill="white"
        />
        Save as a request
      </button> -->

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
import RequestCreation from "./RequestCreation";
import FilterList from "./FilterList.vue";

export default {
  components: {
    ColumnSelection,
    RequestCreation,
    // Requests,
    FilterList,
  },
  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      filterColumnSelection: false,
      filterSelectionType: null,
      // requestCreation: false,
      // requestSelection: false,
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
    // Filter import
    // requestSelected(request) {
    //   // Add the column to the request filters
    //   request.filters.forEach((filter) => {
    //     filter.column = this.data.columns.find((c) => c.label === filter.columnLabel);
    //     if (filter.column) filter.columnIndex = filter.column.index;
    //   });

    //   // Check if all the filters have found a column
    //   let filtersWithNoColumns = request.filters.filter((filter) => filter.columnIndex == null);
    //   if (filtersWithNoColumns.length > 0) {
    //     this.$store.commit("sendMessage", {
    //       title: "error",
    //       msg:
    //         "No column found for the filter(s) : " +
    //         filtersWithNoColumns.map((f) => f.columnLabel).join(", "),
    //     });
    //   }
    //   // Remove the filters with no column index
    //   request.filters = request.filters.filter((filter) => filter.columnIndex !== undefined);

    //   // Add the filter to the store
    //   this.$store.commit("addFilters", {
    //     filters: request.filters,
    //     from: {
    //       widgetType: "Imported",
    //       widgetName: request.name,
    //       widgetIndex: request.id,
    //     },
    //   });

    //   // this.requestSelection = false;
    // },
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
