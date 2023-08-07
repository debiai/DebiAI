<template>
  <div id="intervals">
    <!-- Add values modal -->
    <modal
      v-if="addIntervalPanel"
      @close="addIntervalPanel = false"
    >
      <h4 class="aligned">
        Add an interval filter on the
        <div
          id="columnLabel"
          class="margedSide"
        >
          {{ filter.column.label }}
        </div>
        column
        <button
          class="red"
          @click="addIntervalPanel = false"
          style="margin-left: 80px"
        >
          Cancel
        </button>
      </h4>
      <br />
      <input
        :type="filter.column.typeText == 'Class' ? 'text' : 'number'"
        v-model="newMin"
        placeholder="More than"
      />
      and
      <input
        :type="filter.column.typeText == 'Class' ? 'text' : 'number'"
        v-model="newMax"
        placeholder="Less than"
      />
      <br />
      <br />

      <!-- #controls -->
      <div class="aligned centered">
        <button
          @click="addInterval(false)"
          :disabled="!intervalValid"
        >
          Add
        </button>
        <button
          @click="addInterval(true)"
          :disabled="!intervalValid"
        >
          Add and close
        </button>
      </div>
    </modal>

    <Interval
      class="interval"
      v-for="(interval, i) in filter.intervals"
      :key="i"
      :isLast="i == filter.intervals.length - 1"
      :filter="interval"
      :readOnly="readOnly"
      v-on:remove="removeInterval(i)"
    />
    <button
      @click="addIntervalPanel = true"
      v-if="!readOnly"
    >
      Add interval
    </button>
  </div>
</template>

<script>
import Interval from "./Interval";

export default {
  name: "Intervals",
  components: { Interval },
  props: {
    filter: { type: Object, required: true },
    readOnly: { type: Boolean, default: false },
  },
  data() {
    return {
      addIntervalPanel: false,
      newMin: null,
      newMax: null,
    };
  },
  methods: {
    addInterval(closeAfter) {
      this.newMin = parseFloat(this.newMin);
      this.newMax = parseFloat(this.newMax);

      if (isNaN(this.newMin)) this.newMin = null;
      if (isNaN(this.newMax)) this.newMax = null;

      let interval = {
        min: this.newMin,
        max: this.newMax,
      };

      this.$store.commit("addIntervalToFilter", {
        interval,
        filterId: this.filter.id,
      });
      this.$emit("intervalAdded", { interval, id: this.filter.id });
      if (closeAfter) this.addIntervalPanel = false;
    },
    removeInterval(i) {
      this.$store.commit("removeIntervalFromFilter", {
        filterId: this.filter.id,
        intervalIndex: i,
      });
      this.$emit("intervalRemoved", { intervalIndex: i, id: this.filter.id });
    },
  },
  computed: {
    intervalValid() {
      if (
        (this.newMin === null || this.newMin === "") &&
        (this.newMax === null || this.newMax === "")
      )
        return false;

      if (this.filter.column.typeText !== "Class" && this.newMin !== null && this.newMax !== null)
        if (parseFloat(this.newMin) > parseFloat(this.newMax)) return false;
      return true;
    },
  },
};
</script>

<style scoped>
#intervals {
  display: flex;
  margin: 0 20px 0 20px;
  justify-content: center;
  flex-direction: column;
  min-width: 300px;
}
.interval {
  padding: 5px;
}
</style>
