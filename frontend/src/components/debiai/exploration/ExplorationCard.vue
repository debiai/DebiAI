<template>
  <div
    class="item selectable exploration-card"
    @click="onEdit(false)"
    @middle-click="onEdit(true)"
  >
    <h3>{{ exploration.name }}</h3>
    <div class="description">
      {{ exploration.description }}
    </div>

    <!-- Ongoing exploration display -->
    <ComputationStatus
      v-if="exploration.state === 'ongoing'"
      :exploration="exploration"
      :project="project"
      @cancelled="$emit('refresh')"
    />

    <!-- actions -->
    <div class="actions">
      <button
        class="red"
        @click.stop="onDelete"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script>
import ComputationStatus from "./ComputationStatus.vue";

export default {
  name: "ExplorationCard",
  components: {
    ComputationStatus,
  },
  props: {
    exploration: {
      type: Object,
      required: true,
    },
    project: {
      type: Object,
      required: true,
    },
  },
  methods: {
    onEdit(isMiddleClick) {
      this.$emit("edit", {
        explorationId: this.exploration.id,
        isMiddleClick,
      });
    },
    onDelete() {
      this.$emit("delete", this.exploration.id);
    },
  },
};
</script>

<style scoped lang="scss">
.item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  text-align: left;
  width: 95%;
  margin: 0px;
}

h2 {
  margin: 0;
}

.description {
  margin: 5px 0;
  color: var(--fontColorLight);
  white-space: pre-wrap;
}

.actions {
  width: 100%;
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
