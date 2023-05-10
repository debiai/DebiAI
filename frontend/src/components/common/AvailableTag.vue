<template>
  <div>
    <div
      class="status available"
      v-if="available"
    >
      ✓ Available
    </div>
    <div
      class="status notavailable"
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
  },
};
</script>

<style scoped>
/* Status */
.status {
  padding: 0.2rem 0.5rem;
  font-size: 0.9em;
  font-weight: bold;
  border-radius: 0.5rem;
  border: 2px solid;
}
.status.available {
  color: var(--success);
  border-color: var(--success);
}
.status.notavailable {
  color: var(--danger);
  border-color: var(--danger);
}
</style>
