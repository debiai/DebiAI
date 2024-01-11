<template>
  <div id="column">
    <!-- Name display -->
    <button
      :class="(selected ? 'name selected ' : 'name ') + (column.name.length > 20 ? 'long' : '')"
      @click="select"
      :title="selected ? 'Unselect ' + column.name : 'Select ' + column.name"
    >
      {{ column.name }}
    </button>

    <!-- Number of uniques values display -->
    <div
      class="nbUniqueValues"
      title="Number of uniques values"
      v-if="!metric"
    >
      {{ column.nbUniqueValues }}
    </div>

    <!-- Type display -->
    <div
      :class="'type ' + column.type"
      title="Column type"
    >
      {{ column.type }}
    </div>

    <!-- Aggregation button -->
    <button
      class="nbUniqueAggregations"
      @click="openAggregationPanel"
      v-if="!metric"
    >
      {{ column.nbUniqueAggregations }}
      <inline-svg
        :src="require('@/assets/svg/aggregation.svg')"
        width="18"
        height="18"
        style="margin-left: 3px"
      />
    </button>

    <!-- Metrics button -->
    <button
      class="nbMetrics"
      @click="openMetricsPanel"
      v-if="!metric"
    >
      {{ column.nbMetrics }}
      <inline-svg
        :src="require('@/assets/svg/gear.svg')"
        width="18"
        height="18"
        style="margin-left: 3px"
      />
    </button>
  </div>
</template>

<script>
export default {
  props: {
    column: { type: Object, required: true },
    selected: { type: Boolean, default: true },
    disabled: { type: Boolean, default: false },
    metric: { type: Boolean, default: false },
  },
  methods: {
    select() {
      this.$emit("selected", this.column.index);
    },
    selectAsColor() {
      this.$store.commit("setColoredColumnIndex", this.column.index);
    },
    openAggregationPanel() {},
    openMetricsPanel() {},
  },
};
</script>

<style lang="scss" scoped>
#column {
  display: flex;
  margin: 5px;
  transition: all 0.3s;
  background-color: white;
  padding: 2px;
  border-radius: 4px;

  /* Name (button) */
  .name {
    width: 200px;
    justify-content: center;
    align-items: center;

    border: none;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: "...";

    color: var(--fontColorLight);

    &.selected {
      background-color: var(--secondary);
      color: white;
    }
  }

  .long {
    font-size: 0.75em;
  }

  /* Nb unique values */
  .nbUniqueValues {
    min-width: 40px;
    padding: 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: solid 2px transparent;
  }

  /* Type  */
  .type {
    display: flex;
    justify-content: center;
    align-items: center;

    min-width: 40px;
    margin: 5px;
    padding-left: 7px;
    padding-right: 7px;
    border-radius: 5px;

    color: black;

    &.number {
      border: solid var(--number) 2px;
      color: var(--number);
    }
    &.text {
      border: solid var(--class) 2px;
      color: var(--class);
    }

    &.auto {
      border: solid var(--class) 2px;
      color: var(--class);
    }
  }

  /* Aggregation button */
  .nbUniqueAggregations {
    min-width: 60px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    border: none;
  }
  /* Aggregation button */
  .nbMetrics {
    min-width: 60px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    border: none;
  }
}
</style>
