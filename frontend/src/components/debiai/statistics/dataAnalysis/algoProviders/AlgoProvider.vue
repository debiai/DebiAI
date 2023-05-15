<template>
  <div class="algoProvider">
    <!-- Info about the algoProvider (url, name, status) -->
    <div
      :class="'algoProviderInfo item ' + (algoProvider.status ? 'selectable' : '')"
      @click="displayAlgorithms = !displayAlgorithms"
    >
      <div class="info">
        <div class="head">
          <b>{{ algoProvider.name }}</b>
        </div>
        <div class="data">
          <div>{{ algoProvider.url }}</div>
        </div>
      </div>

      <!-- Status -->
      <AvailableTag :available="algoProvider.status" />

      <!-- Number of algorithms -->
      <div class="nbAlgo">
        <div
          v-if="algoProvider.status"
          class="aligned"
          style="gap: 0.4rem"
        >
          <inline-svg
            :src="require('@/assets/svg/algorithm.svg')"
            width="23"
            height="23"
          />
          {{ algoProvider.algorithms.length }}
        </div>
      </div>

      <!-- Actions -->
      <div class="controls">
        <button
          class="red"
          @click="
            (e) => {
              e.stopPropagation();
              $emit('deleteAlgoProvider');
            }
          "
        >
          Delete
        </button>
      </div>
    </div>

    <!-- Algorithms of this provider: -->
    <transition name="fade">
      <div
        class="algorithms itemList"
        v-if="displayAlgorithms && algoProvider.algorithms"
      >
        <h4 v-if="algoProvider.algorithms.length === 0">No Algorithms provided</h4>
        <Algorithm
          v-for="algo in algoProvider.algorithms"
          :key="algo.id"
          :algorithm="algo"
          @deleteAlgo="deleteAlgo(algo.name)"
          @useAlgo="$emit('useAlgo', algo)"
        />
      </div>
    </transition>
  </div>
</template>

<script>
import Algorithm from "./Algorithm";
export default {
  name: "AlgoProviders",
  components: { Algorithm },
  props: {
    algoProvider: { type: Object, required: true },
  },
  data() {
    return { displayAlgorithms: false };
  },
  methods: {},
};
</script>

<style scoped>
.algoProvider {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.algoProviderInfo {
  display: flex;
  justify-content: space-between;
}
.algoProvider .info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.algoProvider .data {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 0.5rem;
  color: #666;
}

.algoProvider .controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.3rem;
}
</style>
