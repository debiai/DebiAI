<template>
  <div :class="'algoProvider item ' + (algoProvider.status ? 'selectable' : '')">
    <!-- Info (name, url, type)-->
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

    <!-- Actions -->
    <div class="controls">
      <!-- <button @click="getAlgoProviders">Retry</button> -->
      <button
        class="red"
        @click="$emit('deleteAlgoProvider')"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlgoProviders",
  components: {},
  props: {
    algoProvider: { type: Object, required: true },
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
.algoProvider {
  min-width: 400px;
  display: flex;
  padding: 0.8rem;
  margin: 0.5rem 0;
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
