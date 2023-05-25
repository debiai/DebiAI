<template>
  <div id="experiments">
    <!-- Info -->
    <div
      id="info"
      class="aligned spaced"
    >
      <div
        id="title"
        :title="'Id: ' + algorithm.id"
      >
        <span> Experiments of the algorithm: </span>
        <inline-svg
          :src="require('@/assets/svg/algorithm.svg')"
          width="20"
          height="20"
          style="margin: 0 5px 0 15px"
        />
        <span id="algoName">
          {{
            algorithm.name !== null && algorithm.name !== undefined ? algorithm.name : algorithm.id
          }}
        </span>
        <span style="padding: 0 10px"> from </span>
        <span>{{ algoProvider.name }}</span>
      </div>

      <button
        class="red"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </div>
    <div id="description">
      {{ algorithm.description }}
    </div>

    <div id="content">
      <transition-group name="fade">
        <div
          v-for="experiment in experiments"
          :key="experiment.id"
          class="experiment"
        >
          <div class="top">
            <h5 class="experiment-title">
              Experiment {{ experiment.nb }}
              <!-- Display Inputs -->
              <DocumentationBlock
                :followCursor="true"
                v-if="experiment.inputs.length > 0"
              >
                Inputs:
                <div class="inputs">
                  <div
                    class="input"
                    v-for="input in experiment.inputs"
                    :key="input.name"
                  >
                    <div class="name">{{ input.name }}</div>
                    <div class="value">{{ input.value.toString() }}</div>
                  </div>
                </div>
              </DocumentationBlock>
            </h5>

            <button
              class="red"
              @click="deleteExperiment(experiment)"
            >
              x
            </button>
          </div>
          <div class="results">
            <div
              class="result"
              v-for="result in experiment.results"
              :key="result.name"
            >
              <div class="name">{{ result.name }}</div>
              <div class="value">{{ result.value.toString() }}</div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "Experiments",
  props: {
    algorithm: { type: Object, required: true },
    algoProvider: { type: Object, required: true },
    data: { type: Object, required: true },
  },
  data() {
    return {
      experiments: [],
    };
  },
  mounted() {
    this.getExperiments();
  },
  methods: {
    getExperiments() {
      this.experiments = this.$store.getters.getAlgoExperiments(
        this.algoProvider.name,
        this.algorithm.id
      );
      this.experiments.reverse();
    },
    deleteExperiment(experiment) {
      this.$store.commit("deleteExperiment", experiment.id);
      this.getExperiments();
    },
  },
  computed: {},
};
</script>

<style scoped>
#experiments {
  width: 75vw;
  height: 75vh;
  display: flex;
  flex-direction: column;
}

#info {
  font-size: 1.3em;
}
#info #title {
  display: flex;
  align-items: center;
}
#info #algoName {
  font-weight: bold;
  color: #636363;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 2px 5px;
}
#description {
  margin: 10px 0 10px 0;
  text-align: left;
  color: #898989;
}

#content {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding-top: 20px;
}
#content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow: auto;
  flex: 1;
}

#content .experiment {
  display: flex;
  flex-direction: column;

  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 3px;
  margin-bottom: 10px;
}
#content .experiment .experiment-title {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  margin-bottom: 5px;
  font-size: 0.9em;
  color: #909090;
}

.experiment .top {
  padding-bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.experiment .top button {
  padding: 0 5px 0 5px;
  font-size: 0.8em;
}
.experiment .results,
.experiment .inputs {
  display: flex;
  gap: 10px;
}
.experiment .inputs {
  flex-direction: column;
}

.experiment .results .result,
.experiment .inputs .input {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 3px 7px 3px 7px;
  gap: 15px;
}
.experiment .results .result .name,
.experiment .inputs .input .name {
  white-space: nowrap;
}

.experiment .results .result .value,
.experiment .inputs .input .value {
  border: 1px solid #ccc;
  padding: 2px 7px 2px 7px;
  border-radius: 4px;
  max-width: 250px;
  max-height: 50px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
