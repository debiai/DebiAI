<template>
  <div id="filter" :class="filter.inverted ? 'inverted' : ''">
    <!-- title -->
    <div id="title">
      <!-- column Name -->
      <div
        id="columnLabel"
        :class="
          'aligned centered ' +
          (filter.type === 'intervals' ? 'intervalCol' : 'valueCol')
        "
      >
        {{ filter.column.label }}
      </div>
    </div>

    <!-- inerted filter message -->
    <span id="invertedFilterMessage" v-if="filter.inverted"
      >The invertion of :
    </span>

    <!-- Specific filter -->
    <div id="slot">
      <slot />
    </div>

    <!-- Filter effect -->
    <div
      id="fitlerEffect"
      class="aligned centered margedSide"
      v-if="filtersEffecs && filtersEffecs[filter.id] !== undefined"
    >
      <span>
        {{ filtersEffecs[filter.id] }}
      </span>
      <inline-svg
        class="margedSide"
        :src="require('../../../../assets/svg/data.svg')"
        width="20"
        height="20"
      />
    </div>
    <!-- Filter invert -->
    <button
      id="invert"
      :class="
        'aligned centered margedSide ' + (filter.inverted ? 'warning' : 'white')
      "
      title="Invert the filter"
      @click="$emit('invertFilter', filter.id)"
    >
      {{ filter.inverted ? "Filter inverted" : "Invert the filter" }}
      <inline-svg
        :src="require('../../../../assets/svg/invert.svg')"
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
    >
      x
    </button>
  </div>
</template>

<script>
export default {
  name: "Intervals",
  props: { filter: { type: Object, required: true } },
  computed: {
    filtersEffecs() {
      return this.$store.state.SatisticalAnasysis.filtersEffecs;
    },
  },
};
</script>

<style scoped>
#filter {
  flex: 1;
  display: flex;
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
  border-radius: 5px;
  padding: 5px;
}
#columnLabel.valueCol {
  background-color: var(--secondary);
}
</style>