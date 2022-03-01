<template>
  <div id="RequestCreation">
    <!-- page title & cancel btn -->
    <div class="aligned spaced">
      <h2>Requests creation</h2>
      <button class="red" @click="$emit('close')">Cancel</button>
    </div>

    <!-- new request name & desc -->
    <div id="header" class="card">
      <div class="group">
        <label for="name">Request name</label>
        <input type="text" id="name" v-model="requestName" v-focus required />
      </div>
      <div class="group">
        <label for="name">Description</label>
        <textarea id="description" v-model="requestDescription" />
      </div>
    </div>

    <!-- Display filters -->
    <div id="filtersCreation" class="itemList">
      <div class="filter item" v-if="!filters.length">No filters</div>

      <transition-group name="scale">
        <div class="filter item" v-for="filter in filters" :key="filter.id">
          <FilterGenericData
            :filter="filter"
            v-on:removeFilter="removeFilter"
            v-on:invertFilter="invertFilter"
          >
            <!-- Value filters -->
            <Values
              v-if="filter.type === 'values'"
              :filter="filter"
              @valueAdded="addValueToFilter"
              @valueRemoved="removeValueFromFilter"
            />
            <!-- intervals filters -->
            <Intervals
              v-else-if="filter.type === 'intervals'"
              :filter="filter"
              @intervalAdded="addIntervalToFilter"
              @intervalRemoved="removeIntervalFromFilter"
            />
          </FilterGenericData>
        </div>
      </transition-group>
    </div>

    <!-- Controls -->
    <div id="footer" class="card">
      <div>
        <!-- Column selection Modals for creating a new filter -->
        <modal v-if="filterColumnSelection">
          <ColumnSelection
            title="Select a column to apply a filter on"
            v-on:cancel="filterColumnSelection = false"
            v-on:colSelect="selectFilterColumn"
          />
        </modal>
        <!-- Add a value filter btn -->
        <button
          @click="
            filterSelectionType = 'values';
            filterColumnSelection = true;
          "
        >
          + Add a value filter
        </button>
        <!-- Add an interval filter btn -->
        <button
          @click="
            filterSelectionType = 'intervals';
            filterColumnSelection = true;
          "
        >
          + Add an interval filter
        </button>
      </div>

      <!-- Save request btn -->
      <button @click="saveRequest" class="green" :disabled="!requestCanBeSaved">
        <inline-svg
          :src="require('../../../../assets/svg/save.svg')"
          width="13"
          height="13"
          fill="white"
        />
        Save request
      </button>
    </div>
  </div>
</template>

<script>
import FilterGenericData from "../../common/filters/FilterGenericData.vue";
import Intervals from "../../common/filters/Intervals.vue";
import Values from "../../common/filters/Values.vue";

import ColumnSelection from "./ColumnSelection.vue";

export default {
  components: { FilterGenericData, Intervals, Values, ColumnSelection },
  data() {
    return {
      requestName: "My Request",
      requestDescription: "",

      // Filters
      filters: [],

      // settings
      filterColumnSelection: false,
      filterSelectionType: "values",
    };
  },
  methods: {
    saveRequest() {
      let projectId = this.$store.state.ProjectPage.projectId;
      this.$backendDialog
        .addRequest(
          projectId,
          this.requestName,
          this.requestDescription,
          this.filters
        )
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Request created",
          });
          this.$emit("newRequest");
        });
    },
    removeFilter(filterId) {
      this.filters = this.filters.filter((f) => f.id !== filterId);
    },
    invertFilter(filterId) {
      let filterToInvert = this.filters.find((f) => f.id === filterId);
      if (filterToInvert) filterToInvert.inverted = !filterToInvert.inverted;
    },
    selectFilterColumn(columnLabel) {
      // Add a filter on the selected column
      this.filterColumnSelection = false;
      let col = this.columns.find((c) => c.name === columnLabel);
      if (!col) return;

      let filter = {
        id: this.$services.uuid(),
        type: this.filterSelectionType,
        columnLabel: columnLabel,
        column: {
          label: col.name,
          typeText: col.type === "number" ? "Number" : "Class",
        },
        inverted: false,
      };

      if (this.filterSelectionType == "intervals") filter.intervals = [];
      else if (this.filterSelectionType == "values") filter.values = [];
      else return;

      this.filters.push(filter);
    },

    // Values filters
    addValueToFilter({ value, id }) {
      let filter = this.filters.find((f) => f.id === id);
      if (!filter) return;
      filter.values.push(value);
    },
    removeValueFromFilter({ value, id }) {
      let filter = this.filters.find((f) => f.id === id);
      if (!filter) return;
      let valIndex = filter.values.findIndex((v) => v === value);
      if (valIndex === -1) return;
      filter.values.splice(valIndex, 1);
    },

    // Itervals filters
    addIntervalToFilter({ interval, id }) {
      let filter = this.filters.find((f) => f.id === id);
      if (!filter) return;
      filter.intervals.push(interval);
    },
    removeIntervalFromFilter({ intervalIndex, id }) {
      let filter = this.filters.find((f) => f.id === id);
      if (!filter) return;
      filter.intervals.splice(intervalIndex, 1);
    },
  },
  computed: {
    columns() {
      return this.$store.state.ProjectPage.columns;
    },
    requestCanBeSaved() {
      return this.requestName.length > 0 && this.filters.length > 0;
    },
  },
  directives: {
    // Auto focus for the inputs
    focus: { inserted: (el) => el.focus() },
  },
};
</script>

<style scoped>
#RequestCreation {
  height: 80vh;
  width: 80vw;
}
#header {
  display: flex;
  flex-direction: row;
  padding: 10px;
}
#header > div {
  padding-left: 20px;
}
.group {
  display: flex;
  align-items: center;
  justify-content: center;
}
label {
  margin-right: 10px;
}

#footer {
  flex-direction: row;
  justify-content: space-between;
  padding: 10px;
}
</style>