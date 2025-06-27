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
      :exploration="exploration"
      :project="project"
      @cancelled="$emit('refresh')"
    />

    <!-- actions -->
    <div class="actions">
      <div
        class="nbCombinations"
        v-if="exploration.state === 'completed'"
      >
        <b>{{ exploration.real_combinations }}</b> combinations
      </div>
      <button
        @click.stop="onStart"
        v-if="exploration.state === 'completed'"
      >
        Start the exploration analysis
      </button>
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
    onStart() {
      // Go back to the exploration page to start an analysis immediately
      this.$router.push({
        path:
          "/dataprovider/" +
          this.$store.state.ProjectPage.dataProviderId +
          "/project/" +
          this.$store.state.ProjectPage.projectId +
          "/exploration/" +
          this.exploration.id,
        query: {
          projectId: this.$store.state.ProjectPage.projectId,
          dataProviderId: this.$store.state.ProjectPage.dataProviderId,
          explorationId: this.exploration.id,
          startAnalysis: true,
        },
      });
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
