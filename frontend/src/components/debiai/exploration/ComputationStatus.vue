<template>
  <div class="computation-status">
    <!-- Progress bar & time + samples left -->
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%">
      <!-- Progress bar -->
      <div class="progressBar">
        <div
          class="progress"
          :style="{
            width:
              project.nbSamples > 0
                ? (exploration.current_sample / project.nbSamples) * 100 + '%'
                : '0%',
          }"
        ></div>
      </div>

      <!-- Time & samples left -->
      <div style="display: flex; flex-direction: column; width: 300px">
        <div class="samplesLeft">
          <inline-svg
            :src="require('@/assets/svg/data.svg')"
            width="20"
            height="20"
          />
          <span> Sample {{ exploration.current_sample }} / {{ project.nbSamples }} </span>
        </div>
        <div class="timeLeft">
          <inline-svg
            :src="require('@/assets/svg/time.svg')"
            width="20"
            height="20"
          />
          <span>
            {{ $services.timeStampToTime(exploration.remaining_time * 1000) }}
          </span>
        </div>
      </div>
    </div>
    <!-- Ongoing text & control -->
    <div
      style="display: flex; justify-content: flex-end; align-items: center; width: 100%; gap: 10px"
    >
      <span>Exploration is ongoing</span>
      <button
        @click="cancelExplorationComputation"
        :disabled="exploration.state !== 'ongoing' || cancellationLoading"
      >
        Cancel
      </button>
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
    cancelExplorationComputation() {
      if (this.cancellationLoading) return;
      this.cancellationLoading = true;
      this.$explorationDialog
        .cancelRealCombinationsComputation(this.project.id, this.exploration.id)
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
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  gap: 1rem;

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
