<template>
  <div
    id="filter"
    :class="filter.inverted ? 'inverted' : ''"
  >
    <!-- title -->
    <div id="title">
      <!-- column Name -->
      <div
        id="columnLabel"
        :class="'aligned centered ' + (filter.type === 'intervals' ? 'intervalCol' : 'valueCol')"
        title="Column name"
      >
        <span v-if="filter.column && filter.column.label">
          {{ filter.column.label }}
        </span>
        <span v-else>
          Column not found
          <!-- TODO Prevent this from happening -->
        </span>
      </div>
    </div>

    <!-- inverted filter message -->
    <span
      id="invertedFilterMessage"
      v-if="filter.inverted"
      >The inversion of :
    </span>

    <!-- Specific filter -->
    <div id="slot">
      <slot />
    </div>

    <!-- Filter effect -->
    <div
      id="filterEffect"
      class="aligned centered margedSide gapped"
      v-if="filtersEffects && filtersEffects[filter.id] !== undefined"
    >
      <inline-svg
        :src="require('@/assets/svg/data.svg')"
        width="20"
        height="20"
      />
      {{ filtersEffects[filter.id] }}
    </div>

    <!-- Filter invert -->
    <button
      id="invert"
      :class="'aligned centered margedSide ' + (filter.inverted ? 'warning' : 'white')"
      title="Invert the filter"
      @click="$emit('invertFilter', filter.id)"
      v-if="!readOnly"
    >
      {{ filter.inverted ? "Filter inverted" : "Invert the filter" }}
      <inline-svg
        :src="require('@/assets/svg/invert.svg')"
        class="marged"
        width="15"
        height="15"
      />
    </button>

    <!-- Remove filter btn -->
    <button
      class="red margedSide"
      @click="$emit('removeFilter', filter.id)"
      title="Remove the filter"
      v-if="!readOnly"
    >
      <inline-svg
        :src="require('@/assets/svg/close.svg')"
        width="15"
        height="15"
      />
    </button>
  </div>
</template>

<script>
export default {
  name: "Intervals",
  props: {
    filter: { type: Object, required: true },
    readOnly: { type: Boolean, default: false },
  },
  computed: {
    filtersEffects() {
      return this.$store.state.StatisticalAnalysis.filtersEffects;
    },
  },
};
</script>

<style scoped>
#filter {
  flex: 1;
  display: flex;
  align-items: center;
  flex-direction: row;
  padding: 10px;
  transition: all 0.3s ease-in-out;
}
#filter.inverted {
  background-color: rgb(223, 223, 223);
  border-radius: 10px;
}

#title {
  min-width: 170px;
}
#invertedFilterMessage {
  display: flex;
  align-items: center;
  padding-left: 30px;
  font-weight: bold;
}

#slot {
  flex: 1;
}

#invert.white {
  color: black;
}
</style>

<style>
#columnLabel {
  background-color: var(--primary);
  color: white;
  font-weight: bold;
  text-align: center;
  padding: 5px;
}
#columnLabel.valueCol {
  background-color: var(--secondary);
}
</style>
