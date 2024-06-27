<template>
  <div>
    <div
      class="status available"
      :style="{ color: availableColor }"
      v-if="available"
    >
      ✓ Available
    </div>
    <div
      class="status notAvailable"
      :style="{ color: notAvailableColor }"
      v-else
    >
      ❌ Not available
    </div>
  </div>
</template>

<script>
export default {
  name: "AvailableTag",
  props: {
    available: { type: Boolean, required: true },
    availableColor: { type: String, default: "var(--success)" },
    notAvailableColor: { type: String, default: "var(--danger)" },
  },
};
</script>

<style scoped>
/* Status */
.status {
  padding: 0.2rem 0.5rem;
  font-weight: bold;
}
</style>
