<template>
  <div
    id="filterList"
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
          :src="require('@/assets/svg/data.svg')"
          width="20"
          height="20"
          style="margin-left: 5px"
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
</template>

<script>
import FilterGenericData from "./filterTypes/FilterGenericData";
import Values from "./filterTypes/Values";
import Intervals from "./filterTypes/Intervals";

export default {
  components: {
    FilterGenericData,
    Values,
    Intervals,
  },
  props: {
    data: { type: Object, required: true },
    filters: { type: Array, required: true },
  },
  methods: {
    removeFilter(filterId) {
      this.$store.commit("removeFilter", filterId);
    },
    invertFilter(filterId) {
      this.$store.commit("invertFilter", filterId);
    },
  },
  computed: {
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
#filterList {
  margin-top: 20px;
  justify-content: space-around;
}
#filterList #allData {
  flex-direction: row;
}
#filterList .widget {
  flex-direction: row;
  align-items: center;
  /* box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5); */
  /* margin-bottom: 10px; */
}
#filterList .widget .widgetName {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  text-align: center;
  margin: 15px;
}
#filterList .widget .widgetFilters {
  flex: 1;
}

.filter {
  display: flex;
  align-items: center;
}
.filterData {
  flex: 1;
}
</style>
