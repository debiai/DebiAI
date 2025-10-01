<template>
  <div class="computation-status">
    <!-- Ongoing Computation -->
    <div
      class="ongoing"
      v-if="exploration.state === 'ongoing'"
    >
      <!-- Progress bar & time + samples left -->
      <div
        style="
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
          gap: 20px;
        "
      >
        <!-- Progress bar -->
        <div class="progressBar">
          <div
            class="progress"
            :style="{
              width:
                project.metrics.nbSamples > 0
                  ? (exploration.current_sample / project.metrics.nbSamples) * 100 + '%'
                  : '0%',
            }"
          ></div>
        </div>

        <!-- Time & samples left -->
        <div style="display: flex; flex-direction: column; width: 300px">
          <div class="samplesLeft aligned centered gapped">
            <inline-svg
              :src="require('@/assets/svg/data.svg')"
              width="20"
              height="20"
            />
            <span> Sample {{ exploration.current_sample }} / {{ project.metrics.nbSamples }} </span>
          </div>
          <div class="timeLeft aligned centered gapped">
            <inline-svg
              :src="require('@/assets/svg/time.svg')"
              width="20"
              height="20"
            />
            <span>
              {{ $services.nbSecondsToTime(exploration.remaining_time) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Ongoing text & control -->
      <div
        style="
          display: flex;
          justify-content: flex-end;
          align-items: center;
          width: 100%;
          gap: 10px;
        "
      >
        <span>Exploration is ongoing</span>
        <button
          @click="cancelExplorationComputation"
          :disabled="cancellationLoading"
        >
          Cancel
        </button>
      </div>
    </div>
    <!-- Error Computation -->
    <div
      class="error"
      v-else-if="exploration.state === 'error'"
    >
      <span>Exploration computation failed</span>
    </div>
    <!-- Completed Computation -->
    <div
      class="completed"
      v-else-if="exploration.state === 'completed'"
    >
      <h3>Exploration computation completed ✔️</h3>
      <!-- Finished at -->
      <div class="finishedAt">
        <inline-svg
          :src="require('@/assets/svg/time.svg')"
          width="20"
          height="20"
        />
        <span>
          Duration:
          {{ $services.timeSpentBetween(exploration.started_at, exploration.finished_at) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ComputationStatus",
  data() {
    return {
      cancellationLoading: false,
    };
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
    cancelExplorationComputation(event) {
      event.stopPropagation();

      if (this.cancellationLoading) return;
      this.cancellationLoading = true;
      this.$explorationDialog
        .cancelRealCombinationsComputation(this.exploration.id)
        .then(() => {
          this.$store.commit("sendMessage", {
            title: "success",
            msg: "Computation cancelled successfully",
          });
          this.$emit("cancelled");
        })
        .catch((e) => {
          console.log(e);
          this.$store.commit("sendMessage", {
            title: "error",
            msg: "An error occurred while cancelling the computation",
          });
        })
        .finally(() => {
          this.cancellationLoading = false;
        });
    },
  },
  computed: {},
};
</script>

<style scoped lang="scss">
.computation-status {
  width: 100%;

  .ongoing,
  .error {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
    gap: 1rem;
    width: 100%;
  }

  .completed {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
    width: 100%;

    h3 {
      color: green;
    }

    div {
      display: flex;
      align-items: center;
      gap: 0.2rem;
    }
  }

  .progressBar {
    width: 100%;
    height: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
    overflow: hidden;

    .progress {
      width: 0;
      height: 100%;
      background-color: #4caf50;
      transition: width 0.3s ease-in-out;
    }
  }
}
</style>
