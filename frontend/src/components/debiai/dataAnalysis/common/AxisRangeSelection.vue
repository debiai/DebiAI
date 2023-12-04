<template>
  <div id="AxisRangeSelection">
    <!-- Title -->
    <h3 style="padding-bottom: 10px; display: flex; justify-content: space-between">
      Set the plot X and Y axis ranges
      <button
        class="red"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </h3>

    <div
      class="tip"
      style="margin-bottom: 20px"
    >
      Tip: You can also use the mouse and drag the plot axis to manually <br />
      adjust the axis position and range.
    </div>

    <!-- Axis range form -->
    <div
      class="dataGroup"
      style="flex-direction: column; gap: 15px"
    >
      <!-- X axis -->
      <div class="data">
        <span class="name">X axis</span>

        <div
          class="value"
          style="flex: 1"
        >
          <!-- Auto checkbox -->
          <div>
            <span>Auto</span>
            <div>
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

          <!-- Value Min -->
          <div>
            <span>Min</span>
            <div>
              <input
                type="number"
                v-model="XMin"
                :disabled="XAuto"
              />
            </div>
          </div>

          <!-- Value Max -->
          <div>
            <span>Max</span>
            <div style="padding-right: 10px">
              <input
                type="number"
                v-model="XMax"
                :disabled="XAuto"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Y axis -->
      <div class="data">
        <span class="name">Y axis</span>

        <div
          class="value"
          style="flex: 1"
        >
          <!-- Auto checkbox -->
          <div>
            <span>Auto</span>
            <div>
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

          <!-- Values -->
          <div>
            <span>Min</span>
            <div>
              <input
                type="number"
                v-model="YMin"
                :disabled="YAuto"
              />
            </div>
          </div>
          <div>
            <span> Max</span>
            <div style="padding-right: 10px">
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

    <!-- Apply button -->
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
        if (isNaN(this.XMax) || this.XMax === "") return "The X axis maximum value is not a number";
        if (Number(this.XMin) >= Number(this.XMax))
          return "The X axis minimum value must be less than the maximum value";
      }
      if (!this.YAuto) {
        if (isNaN(this.YMin) || this.XMin === "") return "The Y axis minimum value is not a number";
        if (isNaN(this.YMax) || this.XMax === "") return "The Y axis maximum value is not a number";
        if (Number(this.YMin) >= Number(this.YMax))
          return "The Y axis minimum value must be less than the maximum value";
      }
      return true;
    },
  },
};
</script>

<style lang="scss" scoped>
input {
  width: 90px;
}
.error {
  position: absolute;
}

.value {
  display: flex;
  justify-content: space-around !important;
  gap: 10px;

  & > div {
    display: flex;
    align-items: center;
    gap: 5px;
  }
}
</style>
