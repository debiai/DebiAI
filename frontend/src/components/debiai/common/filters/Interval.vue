<template>
  <div class="interval aligned">
    <!-- interval filters -->
    <!-- More than -->
    <div v-if="filter.min !== null">
      More than
      <span
        class="born"
        :title="filter.min"
      >
        {{ $services.prettyNumber(filter.min) }}
      </span>
    </div>

    <!-- Less than -->
    <div v-if="filter.min !== null && filter.max !== null">and</div>
    <div v-if="filter.max !== null">
      Less than
      <span
        class="born"
        :title="filter.max"
      >
        {{ $services.prettyNumber(filter.max) }}
      </span>
      <span v-if="!isLast"> or </span>
    </div>

    <!-- Delete infternal btn -->
    <button
      class="red"
      @click="$emit('remove')"
    >
      x
    </button>
  </div>
</template>

<script>
export default {
  name: "Interval",
  props: {
    filter: { type: Object, required: true },
    isLast: { type: Boolean, default: true },
  },
};
</script>

<style scoped>
.interval {
  color: gray;
  padding: 0px;
}
.interval button {
  transform: scale(0);
  margin-left: 10px;
}
.interval:hover button {
  transform: scale(1);
}

.born {
  color: black;
  background-color: white;
  border-radius: 10px;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);

  padding: 5px;
  margin: 0 5px 0 5px;
}
div + div {
  padding-left: 6px;
}
</style>
