<template>
  <div id="Filters">
    <!-- Column selection modal for creating a new filter -->
    <modal
      v-if="filterColumnSelection"
      @close="filterColumnSelection = false"
    >
      <ColumnSelection
        title="Select a column to filter"
        :data="data"
        :validateRequiered="false"
        v-on:cancel="filterColumnSelection = false"
        v-on:colSelect="selectFilterColumn"
      />
    </modal>

    <!-- request creation modal -->
    <modal
      v-if="requestCreation"
      @close="requestCreation = false"
    >
      <RequestCreation @cancel="requestCreation = false" />
    </modal>

    <!-- Request selection modal -->
    <modal
      v-if="requestSelection"
      @close="requestSelection = false"
    >
      <Requests
        @close="requestSelection = false"
        :selectionMode="true"
        @requestSelected="requestSelected"
      />
    </modal>

    <!-- Header -->
    <div
      id="title"
      style="display: flex"
    >
      <h2>
        <inline-svg
          :src="require('../../../../../assets/svg/filter.svg')"
          width="18"
          height="18"
          style="margin-right: 3px"
        />
        Filters
      </h2>
      <span style="flex: 1"></span>
      <!-- Load filters btn -->
      <button
        @click="requestSelection = true"
        disabled
        title="Available in a futur update"
      >
        <!-- TODO, revert in the filters update -->
        <inline-svg
          :src="require('../../../../../assets/svg/import.svg')"
          width="10"
          height="10"
          fill="lightgrey"
        />
        Load filters from a request
      </button>
      <!-- Save request btn -->
      <button
        class="green"
        :disabled="true || filters.length == 0"
        @click="requestCreation = true"
        title="Available in a futur update"
      >
        <!-- TODO, revert the always disapled in the filters update -->
        <inline-svg
          :src="require('../../../../../assets/svg/save.svg')"
          width="13"
          height="13"
          fill="white"
        />
        Save as a request
      </button>
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
    <div
      id="filters"
      class="itemList"
    >
      <!-- All data -->
      <div
        id="allData"
        class="item spaced card"
      >
        <h3>All data</h3>
        <div class="aligned">
          {{ data.nbLines }}
          <inline-svg
            :src="require('../../../../../assets/svg/data.svg')"
            width="20"
            height="20"
          />
        </div>
      </div>

      <div
        v-if="filters.length == 0"
        class="item"
      >
        No filters
      </div>

      <!-- Filters for each widgets-->
      <transition-group name="fade">
        <div
          class="widget card"
          v-for="(widget, i) in Object.keys(groupedFilters)"
          :key="widget"
        >
          <h4 class="widgetName">{{ i + 1 }} - {{ groupedFilters[widget][0].from.widgetName }}</h4>
          <div class="widgetFilters">
            <transition-group name="fade">
              <div
                class="filter item"
                v-for="filter in groupedFilters[widget]"
                :key="filter.id"
              >
                <!-- Value filters -->
                <FilterGenericData
                  :filter="filter"
                  v-on:removeFilter="removeFilter"
                  v-on:invertFilter="invertFilter"
                  v-if="filter.type === 'values' || filter.type === 'intervals'"
                >
                  <Values
                    :filter="filter"
                    v-if="filter.type === 'values'"
                  />
                  <Intervals
                    :filter="filter"
                    v-else-if="filter.type === 'intervals'"
                  />
                </FilterGenericData>
              </div>
            </transition-group>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- Controls -->
    <div id="controls">
      <!-- Add a value filter btn -->
      <button
        @click="
          filterSelectionType = 'values';
          filterColumnSelection = true;
        "
      >
        Filter values
      </button>
      <!-- Add an interval filter btn -->
      <button
        @click="
          filterSelectionType = 'intervals';
          filterColumnSelection = true;
        "
      >
        Filter intervals
      </button>
    </div>
  </div>
</template>

<script>
// Component
import ColumnSelection from "../common/ColumnSelection";
import FilterGenericData from "../../../common/filters/FilterGenericData.vue";
import Values from "../../../common/filters/Values";
import Intervals from "../../../common/filters/Intervals";
import RequestCreation from "./RequestCreation";
import Requests from "../../../project/requests/Requests.vue";

export default {
  components: {
    ColumnSelection,
    FilterGenericData,
    Values,
    Intervals,
    RequestCreation,
    Requests,
  },
  props: {
    data: { type: Object, required: true },
  },
  data() {
    return {
      filterColumnSelection: false,
      filterSelectionType: null,
      requestCreation: false,
      requestSelection: false,
    };
  },
  methods: {
    clearAll() {
      this.$store.commit("clearAllFilters");
    },
    removeFilter(filterId) {
      this.$store.commit("removeFilter", filterId);
    },
    invertFilter(filterId) {
      this.$store.commit("invertFilter", filterId);
    },

    // Filter creation
    selectFilterColumn(colId) {
      this.filterColumnSelection = false;

      // Add a new epty filter to the store
      let filters;
      if (this.filterSelectionType == "intervals")
        filters = [
          {
            type: "intervals",
            columnIndex: colId,
            intervals: [],
          },
        ];
      else if (this.filterSelectionType == "values")
        filters = [
          {
            type: "values",
            columnIndex: colId,
            values: [],
          },
        ];
      if (filters)
        this.$store.commit("addFilters", {
          filters,
          from: {
            widgetType: "Custom",
            widgetName: "Custom",
            widgetIndex: 0,
          },
        });
    },

    // Filter import
    requestSelected(request) {
      // Add the column to the request filters
      request.filters.forEach((filter) => {
        filter.column = this.data.columns.find((c) => c.label === filter.columnLabel);
        if (filter.column) filter.columnIndex = filter.column.index;
      });

      // Check if all the filters have found a column
      let filtersWithNoColumns = request.filters.filter((filter) => filter.columnIndex == null);
      if (filtersWithNoColumns.length > 0) {
        this.$store.commit("sendMessage", {
          title: "error",
          msg:
            "No column found for the filter(s) : " +
            filtersWithNoColumns.map((f) => f.columnLabel).join(", "),
        });
      }
      // Remove the filters with no column index
      request.filters = request.filters.filter((filter) => filter.columnIndex !== undefined);

      // Add the filter to the store
      this.$store.commit("addFilters", {
        filters: request.filters,
        from: {
          widgetType: "Imported",
          widgetName: request.name,
          widgetIndex: request.id,
        },
      });

      this.requestSelection = false;
    },
  },
  computed: {
    filters() {
      // Get the filters from the store & find the column of each filters
      return this.$store.state.SatisticalAnasysis.filters.map((filter) => {
        filter.column = this.data.columns[filter.columnIndex];
        return filter;
      });
    },
    groupedFilters() {
      // Group the filters by widget
      return this.filters.reduce((acc, filter) => {
        if (!acc[filter.from.widgetIndex]) acc[filter.from.widgetIndex] = [];
        acc[filter.from.widgetIndex].push(filter);
        return acc;
      }, {});
    },
  },
};
</script>

<style scoped>
#Filters {
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
#filters {
  margin-top: 20px;
  justify-content: space-around;
}
#filters #allData {
  flex-direction: row;
}
#filters .widget {
  flex-direction: row;
  align-items: center;
  /* box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5); */
  /* margin-bottom: 10px; */
}
#filters .widget .widgetName {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  text-align: center;
  margin: 15px;
}
#filters .widget .widgetFilters {
  flex: 1;
}

.filter {
  display: flex;
  align-items: center;
}
.filterData {
  flex: 1;
}
#controls {
  padding-top: 20px;
}
</style>
