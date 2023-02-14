<template>
  <div id="analysis">
    <!-- Start analysis -->
    <div class="param">
      <button
        id="startAnalysisBtn"
        @click="startAnalysis(false)"
        @mousedown.middle="startAnalysis(true)"
        :disabled="disabled"
      >
        Start analysis
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    disabled: { type: Boolean, default: false },
  },
  data: () => {
    return {};
  },

  methods: {
    startAnalysis(newTab) {
      this.$emit("startAnalysis", { newTab });
    },
  },
  computed: {},
};
</script>

<style scoped>
#analysis {
  padding: 10px;
  height: 18vh;
  display: flex;
  justify-content: center;
}

#parameters {
  flex: 1;
  display: flex;
  justify-content: space-evenly;
}

.param {
  display: flex;
  width: 400px;
  flex-direction: column;
  padding: 10px;
  box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.2);
  background-color: white;
  border-radius: 10px;
  margin: 5px;
}
.param .data {
  flex: 1;
}
.param .value {
  flex: 1;
}
.dataGroup {
  flex-direction: column;
}
.dataGroup .data + .data {
  padding-top: 3px;
}
.value.only {
  height: 30px;
  border-radius: 10px;
}
#startAnalysisBtn {
  height: 100%;
  font-size: 1.2em;
}
</style>
