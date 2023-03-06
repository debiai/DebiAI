<template>
  <div id="axiesRangeSelection">
    <!-- Title -->
    <h3 style="padding-bottom: 20px">
      Set the plot X and Y axis ranges
      <button
        class="red"
        @click="$emit('cancel')"
        style="margin-left: 50px"
      >
        Cancel
      </button>
    </h3>
    <div
      class="dataGroup"
      style="flex-direction: column; gap: 15px"
    >
      <!-- X axis -->
      <div class="data">
        <span class="name">X axis</span>

        <div
          class="value"
          style="flex: 1; gap: 10px"
        >
          <!-- Auto checkbox -->
          <div class="data">
            <span class="name">Auto</span>
            <div
              class="value"
              style="background: var(--blankDark)"
            >
              <input
                type="checkbox"
                :id="'axisXAutoCbxPointPlot' + index"
                class="customCbx"
                v-model="XAuto"
                style="display: none"
              />
              <label
                :for="'axisXAutoCbxPointPlot' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>

          <div style="display: flex; flex-direction: column">
            <!-- Values -->
            <div class="data">
              <span
                class="name"
                style="width: 30px"
                >Min</span
              >
              <div class="value">
                <input
                  type="number"
                  v-model="XMin"
                  :disabled="XAuto"
                />
              </div>
            </div>
            <div class="data">
              <span
                class="name"
                style="width: 30px"
                >Max</span
              >
              <div class="value">
                <input
                  type="number"
                  v-model="XMax"
                  :disabled="XAuto"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Y axis -->
      <div class="data">
        <span class="name">Y axis</span>

        <div
          class="value"
          style="flex: 1; gap: 10px"
        >
          <!-- Auto checkbox -->
          <div class="data">
            <span class="name">Auto</span>
            <div
              class="value"
              style="background: var(--blankDark)"
            >
              <input
                type="checkbox"
                :id="'axisYAutoCbxPointPlot' + index"
                class="customCbx"
                v-model="YAuto"
                style="display: none"
              />
              <label
                :for="'axisYAutoCbxPointPlot' + index"
                class="toggle"
              >
                <span></span>
              </label>
            </div>
          </div>

          <div style="display: flex; flex-direction: column">
            <!-- Values -->
            <div class="data">
              <span
                class="name"
                style="width: 30px"
                >Min</span
              >
              <div class="value">
                <input
                  type="number"
                  v-model="YMin"
                  :disabled="YAuto"
                />
              </div>
            </div>
            <div class="data">
              <span
                class="name"
                style="width: 30px"
              >
                Max</span
              >
              <div class="value">
                <input
                  type="number"
                  v-model="YMax"
                  :disabled="YAuto"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button
      class="blue"
      @click="
        $emit('apply', {
          axisXAuto: XAuto,
          axisYAuto: YAuto,
          axisXMin: parseFloat(XMin),
          axisXMax: parseFloat(XMax),
          axisYMin: parseFloat(YMin),
          axisYMax: parseFloat(YMax),
        })
      "
      style="margin-top: 20px"
      :disabled="canApply !== true"
    >
      Apply
    </button>
    <div
      class="error"
      v-if="canApply !== true"
      style="margin-top: 10px"
    >
      {{ canApply }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    index: { type: String, required: true },
    axisXAuto: { type: Boolean, default: true },
    axisXMin: { type: Number, default: 0 },
    axisXMax: { type: Number, default: 1 },
    axisYAuto: { type: Boolean, default: true },
    axisYMin: { type: Number, default: 0 },
    axisYMax: { type: Number, default: 1 },
  },
  data() {
    return {
      XAuto: this.axisXAuto,
      XMin: this.axisXMin,
      XMax: this.axisXMax,
      YAuto: this.axisYAuto,
      YMin: this.axisYMin,
      YMax: this.axisYMax,
    };
  },
  computed: {
    canApply() {
      if (!this.XAuto) {
        if (isNaN(this.XMin) || this.XMin === "") return "The X axis minimum value is not a number";
        if (isNaN(this.XMax) || this.XMin === "") return "The X axis maximum value is not a number";
        if (this.XMin >= this.XMax)
          return "The X axis minimum value must be less than the maximum value";
      }
      if (!this.YAuto) {
        if (isNaN(this.YMin) || this.XMin === "") return "The Y axis minimum value is not a number";
        if (isNaN(this.YMax) || this.XMin === "") return "The Y axis maximum value is not a number";
        if (this.YMin >= this.YMax)
          return "The Y axis minimum value must be less than the maximum value";
      }
      return true;
    },
  },
};
</script>

<style scoped>
.error {
  position: absolute;
}
</style>
